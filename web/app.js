"use strict";
// Prototype: a trust assistant inside Property Finder search. Static, no build, no network except data/*.json.
// All third-party text is inserted with textContent (via h()), never innerHTML.

/** @typedef {{id:string, offering:string, url:string, title:string, price_aed:number, size_sqft:number, furnished:string, cheques:number|null, available_from:string|null, agency:string, is_verified:boolean, has_permit_link:boolean, transactions:{date:string, amount:number, size_sqft:number}[], bedrooms:number, bathrooms:number}} Listing */
/** @typedef {{rule_id:string, severity:string, title:string, reason:string, ask_agent:string|null}} Flag */
/** @typedef {{listing:Listing, verdict:{listing_id:string, status:string, flags:Flag[], duplicate_group:string|null, agent_questions:string[]}}} Card */
/** @typedef {{listing_id:string, available:boolean|null, confirmed_price_aed:number|null, terms:string, viewing_slots:string[]}} Reply */
/** @typedef {{group_id:string, listing_ids:string[], price_min_aed:number, price_max_aed:number, agencies:number, keep_id:string}} Group */

/** @type {{generated:string, groups:Group[], cards:Card[], replies:Reply[]}} */
let DATA = { generated: "", groups: [], cards: [], replies: [] };
/** Extra question text, kept in page memory only. @type {Record<string,string>} */
const extraQuestions = {};

const OUT_KEY = "pfa_outcomes";
const INTRO_KEY = "pfa_intro_seen";
const MODE_KEY = "pfa_mode";

// ---------- helpers ----------

/**
 * Build an element. Strings in children become text nodes (safe).
 * @param {string} tag
 * @param {Record<string, any>} [attrs]
 * @param {(Node|string|null|false)[]} [kids]
 * @returns {HTMLElement}
 */
function h(tag, attrs = {}, kids = []) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (v !== null && v !== undefined && v !== false) el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids) if (kid) el.append(kid);
  return el;
}

/** @param {string} key @param {any} fallback */
function load(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; }
}
/** @param {string} key @param {any} value */
function save(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode: stay in memory */ }
}

/** @returns {Record<string, {state:string, reason:string, reply:Reply|null, slot?:string}>} */
const outcomes = () => load(OUT_KEY, {});

/** @param {number} n @param {string} offering */
function money(n, offering) {
  if (offering === "sale") {
    return n >= 1e6 ? "AED " + (n / 1e6).toFixed(2).replace(/\.?0+$/, "") + "M" : "AED " + n.toLocaleString("en-US");
  }
  return "AED " + n.toLocaleString("en-US");
}
/** @param {Listing} l */
function priceEl(l) {
  return h("div", { class: "price" }, [money(l.price_aed, l.offering), l.offering === "rent" ? h("small", {}, [" /year"]) : null]);
}

/** @param {string} msg */
function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { t.hidden = true; }, 2800);
}

const byId = (/** @type {string} */ id) => DATA.cards.find((c) => c.listing.id === id);
const replyFor = (/** @type {string} */ id) => DATA.replies.find((r) => r.listing_id === id) || null;
const groupOf = (/** @type {Card} */ c) => DATA.groups.find((g) => g.group_id === c.verdict.duplicate_group) || null;

/**
 * Status after any reply the person has already collected.
 * @param {Card} c
 * @returns {"shortlist"|"check"|"hidden"}
 */
function effectiveStatus(c) {
  const o = outcomes()[c.listing.id];
  if (o && o.state === "shortlist") return "shortlist";
  if (o && o.state === "removed") return "hidden";
  return /** @type {any} */ (c.verdict.status);
}

/** Why a card is hidden, in a few words. @param {Card} c */
function hiddenLabel(c) {
  const o = outcomes()[c.listing.id];
  if (o && o.state === "removed") return "Removed: " + o.reason;
  const f = c.verdict.flags.find((x) => x.severity === "block") || c.verdict.flags[0];
  return "Hidden: " + (f ? f.title : "likely misleading");
}

/** Top flag by severity. @param {Card} c */
function topFlag(c) {
  const order = ["block", "warn", "info"];
  return [...c.verdict.flags].sort((a, b) => order.indexOf(a.severity) - order.indexOf(b.severity))[0] || null;
}

/** Non-keep members of a duplicate group are folded under the keep card. @param {Card} c */
function isFolded(c) {
  const g = groupOf(c);
  return !!g && g.keep_id !== c.listing.id && !!byId(g.keep_id);
}

// ---------- routing ----------

/** @returns {{path:string[], q:URLSearchParams}} */
function parseHash() {
  const raw = location.hash.replace(/^#\/?/, "");
  const [p, qs] = raw.split("?");
  return { path: p.split("/").filter(Boolean), q: new URLSearchParams(qs || "") };
}
/** @param {URLSearchParams} q */
function currentMode(q) {
  const m = q.get("mode") || load(MODE_KEY, "rent");
  save(MODE_KEY, m);
  return m === "sale" ? "sale" : "rent";
}

function route() {
  const { path, q } = parseHash();
  const screen = document.getElementById("screen");
  screen.replaceChildren();
  window.scrollTo(0, 0);
  const [name, id] = path;
  let view;
  if (name === "listing" && byId(id)) view = renderListing(byId(id));
  else if (name === "ask" && byId(id)) view = renderAsk(byId(id));
  else if (name === "agent" && byId(id)) view = renderAgent(byId(id));
  else if (name === "shortlist") view = renderShortlist();
  else view = renderResults(currentMode(q), q.get("hidden") === "1");
  screen.append(view);
  const onShort = name === "shortlist";
  document.getElementById("tab-search").classList.toggle("on", !onShort);
  document.getElementById("tab-short").classList.toggle("on", onShort);
  document.getElementById("tab-count").textContent = String(DATA.cards.filter((c) => effectiveStatus(c) === "shortlist").length);
}

// ---------- shared pieces ----------

/** @param {Card} c */
function statusChip(c) {
  const s = effectiveStatus(c);
  if (s === "shortlist") return h("span", { class: "chip green" }, ["Short list"]);
  if (s === "check") return h("span", { class: "chip amber" }, ["Assistant will check"]);
  return h("span", { class: "chip grey" }, [hiddenLabel(c)]);
}

/** @param {Listing} l */
function photoBox(l) {
  return h("a", { class: "photo", href: l.url, target: "_blank", rel: "noopener noreferrer" }, ["Photos on Property Finder"]);
}

/** @param {Card} c @param {boolean} [withGroup] */
function renderCard(c, withGroup = true) {
  const l = c.listing;
  const f = topFlag(c);
  const o = outcomes()[l.id];
  const card = h("div", { class: "card" + (effectiveStatus(c) === "hidden" ? " hidden-card" : "") }, [
    photoBox(l),
    priceEl(l),
    h("div", { class: "title" }, [l.title]),
    h("div", { class: "muted" }, [`${l.size_sqft.toLocaleString("en-US")} sqft · ${l.bedrooms} bed · ${l.bathrooms} bath`]),
    h("div", { class: "row" }, [
      statusChip(c),
      l.is_verified ? h("span", { class: "badge" }, ["Verified"]) : null,
      h("span", { class: "muted small" }, [l.agency]),
    ]),
    f ? h("div", { class: "flagline" }, [f.title]) : null,
    o && o.state === "shortlist" ? h("div", { class: "flagline" }, ["Confirmed by agent"]) : null,
    h("div", { class: "row" }, [h("a", { href: `#/listing/${encodeURIComponent(l.id)}` }, ["Details and checks"])]),
  ]);
  const g = withGroup ? groupOf(c) : null;
  if (g && g.keep_id === l.id) card.append(dupBlock(g));
  return card;
}

/** @param {Group} g */
function dupBlock(g) {
  const others = g.listing_ids.map(byId).filter((c) => c && c.listing.id !== g.keep_id);
  const list = h("ul", { hidden: true }, others.map((c) =>
    h("li", {}, [`${money(c.listing.price_aed, c.listing.offering)} · ${c.listing.agency} `, h("a", { href: `#/listing/${encodeURIComponent(c.listing.id)}` }, ["view"])])));
  const btn = h("button", { type: "button", onclick: () => { list.hidden = !list.hidden; } },
    [(() => {
      const off = others[0] ? others[0].listing.offering : "rent";
      const n = g.listing_ids.length;
      const price = g.price_min_aed === g.price_max_aed
        ? `all at ${money(g.price_min_aed, off)}`
        : `at ${money(g.price_min_aed, off)}–${money(g.price_max_aed, off).replace("AED ", "")}`;
      return `Same flat listed ${n} times by ${g.agencies} agencies, ${price}`;
    })()]);
  return h("div", { class: "dup" }, [btn, list]);
}

/** @param {string} href @param {string} [text] */
const backLink = (href, text = "‹ Back") => h("a", { class: "back", href }, [text]);

// ---------- screens ----------

/** @param {"rent"|"sale"} mode @param {boolean} showHidden */
function renderResults(mode, showHidden) {
  const cards = DATA.cards.filter((c) => c.listing.offering === mode);
  const shown = cards.filter((c) => !isFolded(c));
  const short = shown.filter((c) => effectiveStatus(c) === "shortlist");
  const check = shown.filter((c) => effectiveStatus(c) === "check");
  const hidden = cards.filter((c) => effectiveStatus(c) === "hidden");
  const hiddenCount = hidden.length;

  const sw = h("div", { class: "switch" }, [
    h("a", { href: "#/results?mode=rent", class: mode === "rent" ? "on" : "" }, ["Rent"]),
    h("a", { href: "#/results?mode=sale", class: mode === "sale" ? "on" : "" }, ["Buy"]),
  ]);
  const whyHref = `#/results?mode=${mode}${showHidden ? "" : "&hidden=1"}`;
  const bar = h("div", { class: "bar" }, [
    "Your assistant checked ", h("b", {}, [String(cards.length)]), " listings: ",
    h("b", {}, [`${short.length} on your short list`]), " · ",
    h("b", {}, [`${check.length} to confirm with the agent`]), " · ",
    h("b", {}, [`${hiddenCount} hidden`]), ". ",
    h("a", { class: "why", href: whyHref }, [showHidden ? "Hide them again" : "Why hidden?"]),
  ]);

  const view = h("div", { class: "pad" }, [h("h1", {}, ["Princess Tower, Dubai Marina · 2 bed"]), h("div", { class: "muted" }, [mode === "rent" ? "For rent" : "For sale"]), sw, bar]);
  if (!shown.length) view.append(h("p", { class: "muted" }, ["No listings in this mode."]));
  for (const c of [...short, ...check]) view.append(renderCard(c));
  if (showHidden) {
    view.append(h("h2", { id: "hidden-h" }, [`Hidden (${hiddenCount})`]));
    for (const c of hidden) {
      const card = renderCard(c, false);
      card.append(...hiddenWhy(c));
      view.append(card);
    }
    setTimeout(() => { const el = document.getElementById("hidden-h"); if (el) el.scrollIntoView(); }, 0);
  }
  return view;
}

/** Evidence and the way back, for a hidden card. @param {Card} c @returns {HTMLElement[]} */
function hiddenWhy(c) {
  const o = outcomes()[c.listing.id];
  if (o && o.state === "removed") {
    return [h("p", { class: "small" }, [h("b", {}, ["Removed. "]), o.reason + "."]), h("p", { class: "small muted" }, ["Removed after the agent's reply."])];
  }
  const out = [];
  const g = groupOf(c);
  const keep = g && g.keep_id !== c.listing.id ? byId(g.keep_id) : null;
  if (g && keep) {
    const off = c.listing.offering;
    const spread = g.price_min_aed === g.price_max_aed
      ? `all at ${money(g.price_min_aed, off)}`
      : `prices ${money(g.price_min_aed, off)} to ${money(g.price_max_aed, off).replace("AED ", "")}`;
    out.push(h("p", { class: "small" }, [
      h("b", {}, ["Duplicate. "]), "Same flat as ",
      h("a", { href: `#/listing/${encodeURIComponent(keep.listing.id)}` }, [`${keep.listing.title} at ${money(keep.listing.price_aed, off)}`]),
      `. Listed ${g.listing_ids.length} times by ${g.agencies} agencies, ${spread}.`,
    ]));
    out.push(h("p", { class: "small muted" }, ["Shown again if the agent confirms it's a different unit."]));
  }
  for (const f of c.verdict.flags.filter((x) => x.severity !== "info" && !(keep && x.rule_id === "R2"))) {
    out.push(h("p", { class: "small" }, [h("b", {}, [f.title + ". "]), f.reason]));
  }
  if (!keep) out.push(h("p", { class: "small muted" }, ["Shown again if the agent confirms the details."]));
  return out;
}

/** @param {Card} c */
function renderListing(c) {
  const l = c.listing;
  const view = h("div", { class: "pad" }, [
    backLink("#/results?mode=" + (l.offering === "sale" ? "sale" : "rent"), "‹ Results"),
    photoBox(l),
    priceEl(l),
    h("h1", {}, [l.title]),
    h("div", { class: "row" }, [statusChip(c), l.is_verified ? h("span", { class: "badge" }, ["Verified"]) : null]),
  ]);
  const facts = [
    ["Size", `${l.size_sqft.toLocaleString("en-US")} sqft`],
    ["Beds / baths", `${l.bedrooms} / ${l.bathrooms}`],
    ["Furnished", l.furnished],
    l.offering === "rent" && l.cheques ? ["Cheques", String(l.cheques)] : null,
    l.available_from ? ["Available from", l.available_from] : null,
    ["Agency", l.agency],
    ["Permit link", l.has_permit_link ? "Shown" : "Missing"],
  ].filter(Boolean);
  const dl = h("dl", { class: "facts" });
  for (const [k, v] of facts) dl.append(h("dt", {}, [k]), h("dd", {}, [v]));
  view.append(dl);

  const panel = h("div", { class: "panel" }, [h("h2", {}, ["Before you call"])]);
  if (!c.verdict.flags.length) panel.append(h("p", {}, ["The assistant found nothing odd."]));
  for (const f of c.verdict.flags) {
    panel.append(h("div", { class: "flag " + f.severity }, [h("span", { class: "chip" }, [f.title]), h("div", { class: "small" }, [f.reason])]));
  }
  if (l.offering === "rent" && l.transactions.length) {
    const t = h("table");
    t.append(h("tr", {}, [h("th", {}, ["Registered rent, same size"]), h("th", {}, ["AED / year"])]));
    for (const x of l.transactions.slice(0, 5)) t.append(h("tr", {}, [h("td", {}, [x.date]), h("td", {}, [x.amount.toLocaleString("en-US")])]));
    t.append(h("tr", {}, [h("td", {}, [h("b", {}, ["This listing"])]), h("td", {}, [h("b", {}, [l.price_aed.toLocaleString("en-US")])])]));
    panel.append(h("h2", {}, ["Price vs recent deals"]), t);
  }
  view.append(panel);
  view.append(h("div", { class: "actions" }, [
    h("a", { class: "btn primary", href: `#/ask/${encodeURIComponent(l.id)}` }, ["Ask the agent for me"]),
    h("button", { class: "btn secondary", type: "button", onclick: () => toast("In the real app this opens the call — prototype only") }, ["Call the agent yourself"]),
  ]));
  view.append(h("p", { class: "muted small" }, ["Call directly if you already know this building and just need a viewing time."]));
  return view;
}

/** @param {Card} c */
function renderAsk(c) {
  const l = c.listing;
  const view = h("div", { class: "pad" }, [backLink(`#/listing/${encodeURIComponent(l.id)}`), h("h1", {}, ["Ask the agent for me"]), h("div", { class: "muted" }, [l.title + " · " + money(l.price_aed, l.offering)])]);
  const body = h("div");
  view.append(body);
  const existing = outcomes()[l.id];
  if (existing) showReply(body, c, existing.reply, false);
  else showForm(body, c);
  view.append(h("p", {}, [h("a", { href: `#/agent/${encodeURIComponent(l.id)}` }, ["See what the agent receives →"])]));
  return view;
}

/** @param {HTMLElement} body @param {Card} c */
function showForm(body, c) {
  const id = c.listing.id;
  const base = [...c.verdict.agent_questions];
  if (!base.length) base.push("Is this still available?");
  const boxes = base.map((q) => h("input", { type: "checkbox", checked: true }));
  const checks = h("div", { class: "msg" }, [
    h("div", { class: "small muted" }, [`Message to ${c.listing.agency}, sent on your behalf:`]),
    ...base.map((q, i) => h("label", {}, [boxes[i], h("span", {}, [q])])),
  ]);
  const extra = h("textarea", { rows: "2", placeholder: "Anything else you want to ask? (optional)" });
  extra.value = extraQuestions[id] || "";
  extra.addEventListener("input", () => { extraQuestions[id] = extra.value; });
  const send = h("button", { class: "btn primary", type: "button", onclick: () => {
    const picked = base.filter((_, i) => boxes[i].checked);
    if (!picked.length && !extra.value.trim()) { toast("Tick at least one question, or write your own."); return; }
    body.replaceChildren(h("div", { class: "spinner" }, ["Sent. Waiting for the agent…"]));
    setTimeout(() => showReply(body, c, replyFor(id), true), 1500);
  } }, ["Send to agent"]);
  body.replaceChildren(checks, extra, send, h("p", { class: "muted small" }, ["The agent stays in the deal: you can call or message them any time."]));
}

/**
 * Decide the outcome of a reply.
 * @param {Card} c @param {Reply|null} r
 * @returns {{state:"shortlist"|"removed"|"wait", reason:string}}
 */
function decide(c, r) {
  if (!r || r.available === null) return { state: "wait", reason: "" };
  if (!r.available) return { state: "removed", reason: "agent says it is no longer available" };
  const p = c.listing.price_aed;
  if (r.confirmed_price_aed !== null && r.confirmed_price_aed > p) {
    return { state: "removed", reason: `real price is ${money(r.confirmed_price_aed, c.listing.offering)}, higher than the ${money(p, c.listing.offering)} listed` };
  }
  return { state: "shortlist", reason: "" };
}

/** Store the decided outcome of a reply, as the searcher side reads it. @param {Card} c @param {Reply|null} r */
function saveOutcome(c, r) {
  const d = decide(c, r);
  if (d.state === "wait") return;
  const all = outcomes();
  all[c.listing.id] = { state: d.state, reason: d.reason, reply: r };
  save(OUT_KEY, all);
  document.getElementById("tab-count").textContent = String(DATA.cards.filter((x) => effectiveStatus(x) === "shortlist").length);
}

/** @param {HTMLElement} body @param {Card} c @param {Reply|null} r @param {boolean} fresh */
function showReply(body, c, r, fresh) {
  const l = c.listing;
  const d = decide(c, r);
  if (fresh) saveOutcome(c, r);
  const kids = [h("span", { class: "demo" }, ["Demo: agent reply is mocked"])];
  if (d.state === "wait") {
    kids.push(h("div", { class: "outcome wait" }, ["Agent hasn't replied yet — we'll notify you in the app"]));
  } else {
    const price = r.confirmed_price_aed !== null ? money(r.confirmed_price_aed, l.offering) : "not stated";
    kids.push(h("div", { class: "reply" }, [
      h("div", {}, [h("b", {}, ["Still available: "]), r.available ? "Yes" : "No"]),
      h("div", {}, [h("b", {}, ["Real price: "]), price]),
      r.terms ? h("div", {}, [h("b", {}, ["Terms: "]), r.terms]) : null,
    ]));
    if (d.state === "shortlist") {
      kids.push(h("div", { class: "outcome ok" }, ["Added to your short list"]));
      const saved = outcomes()[l.id];
      if (r.viewing_slots.length) {
        kids.push(h("div", { class: "small muted" }, ["Book a viewing:"]));
        kids.push(h("div", {}, r.viewing_slots.map((s) => h("button", { class: "btn slot " + (saved && saved.slot === s ? "primary" : "secondary"), type: "button", onclick: () => bookSlot(c, s) }, [s]))));
      }
      kids.push(h("a", { href: "#/shortlist" }, ["See your short list"]));
    } else {
      kids.push(h("div", { class: "outcome no" }, ["Removed: " + d.reason]));
      kids.push(h("a", { href: "#/results?mode=" + (l.offering === "sale" ? "sale" : "rent") }, ["Back to results"]));
    }
  }
  body.replaceChildren(...kids);
}

/** @param {Card} c @param {string} slot */
function bookSlot(c, slot) {
  const all = outcomes();
  if (all[c.listing.id]) { all[c.listing.id].slot = slot; save(OUT_KEY, all); }
  toast("Viewing requested for " + slot + " (demo). The agent will confirm in the app.");
  route();
}

/**
 * The listing agent's side: what they receive, and one-tap answers that feed the searcher side.
 * Searcher details are mocked.
 * @param {Card} c
 */
function renderAgent(c) {
  const l = c.listing;
  const id = encodeURIComponent(l.id);
  const rent = l.offering === "rent";
  const perYear = rent ? " /year" : "";
  const questions = c.verdict.agent_questions.length ? c.verdict.agent_questions : ["Is this still available?"];
  const windows = ["Weekdays after 6pm", "Saturday 10am to 1pm"];
  const mock = replyFor(l.id);
  const slots = mock && mock.viewing_slots.length ? mock.viewing_slots : ["Thu 6:00pm", "Sat 11:00am"];
  /** Slots the agent offers. @type {Set<string>} */
  const offered = new Set(slots);

  const view = h("div", { class: "pad" }, [
    h("div", { class: "agentbar" }, ["Agent's view"]),
    backLink(`#/ask/${id}`, "‹ Back to the searcher's view"),
    h("h1", {}, ["New pre-qualified lead"]),
    h("span", { class: "demo" }, ["Demo: searcher details are mocked"]),
  ]);

  const rows = [
    ["Listing", l.title],
    ["Listed price", money(l.price_aed, l.offering) + perYear],
    ["Budget", "Up to " + money(l.price_aed, l.offering) + perYear],
    ["Move-in", l.available_from ? "From " + l.available_from : "Within 30 days"],
    rent ? ["Cheques", `Can pay in ${l.cheques || 4}`] : ["Payment", "Mortgage pre-approved"],
    ["Household", "2 adults"],
    ["Viewing windows", windows.join(" or ")],
  ];
  const dl = h("dl", { class: "facts" });
  for (const [k, v] of rows) dl.append(h("dt", {}, [k]), h("dd", {}, [v]));
  view.append(h("div", { class: "card" }, [h("b", {}, ["Searcher requirements"]), dl]));
  view.append(h("h2", {}, ["Questions sent to you"]), h("ul", {}, questions.map((q) => h("li", {}, [q]))));

  const body = h("div");
  const draw = () => {
    const o = outcomes()[l.id];
    body.replaceChildren(...(o ? [outcomeNote(o)] : []));
  };
  /** @param {boolean} available @param {number|null} price */
  const answer = (available, price) => {
    /** @type {Reply} */
    const r = { listing_id: l.id, available, confirmed_price_aed: price, terms: "", viewing_slots: available ? [...offered] : [] };
    saveOutcome(c, r);
    toast("Answer sent. The searcher sees it now (demo).");
    draw();
  };

  const chips = h("div", {}, slots.map((s) => {
    const b = h("button", { type: "button", class: "btn slot primary", onclick: () => {
      if (offered.has(s)) offered.delete(s); else offered.add(s);
      b.className = "btn slot " + (offered.has(s) ? "primary" : "secondary");
    } }, [s]);
    return b;
  }));
  const priceIn = h("input", { type: "number", class: "numin", min: "1", placeholder: "New price in AED" });
  const priceRow = h("div", { class: "row", hidden: true }, [
    priceIn,
    h("button", { type: "button", class: "btn primary", onclick: () => {
      const n = Number(priceIn.value);
      if (!(n > 0)) { toast("Enter the new price."); return; }
      answer(true, n);
    } }, ["Confirm"]),
  ]);
  view.append(
    h("h2", {}, ["Answer in one tap"]),
    h("div", { class: "small muted" }, ["Viewing slots you offer (tap to switch off):"]), chips,
    h("div", { class: "actions" }, [
      h("button", { type: "button", class: "btn primary", onclick: () => answer(true, l.price_aed) }, ["Available at this price"]),
      h("button", { type: "button", class: "btn secondary", onclick: () => answer(false, null) }, ["Gone / let"]),
      h("button", { type: "button", class: "btn secondary", onclick: () => { priceRow.hidden = !priceRow.hidden; } }, ["Price changed"]),
    ]),
    priceRow, body,
    h("div", { class: "panel" }, [
      h("b", {}, ["What this saves you"]),
      h("p", { class: "small" }, ["Budget, dates and cheques already answered · no viewing for a searcher over budget · one tap instead of a call."]),
      h("p", { class: "small muted" }, ["A “Gone” answer hides the listing for this searcher only. Please also take the ad down."]),
    ]),
    h("p", {}, [h("a", { href: `#/listing/${id}` }, ["See this listing as the searcher →"])]),
  );
  draw();
  return view;
}

/** @param {{state:string, reason:string}} o */
function outcomeNote(o) {
  return o.state === "shortlist"
    ? h("div", { class: "outcome ok" }, ["Sent. The searcher has it on their short list."])
    : h("div", { class: "outcome no" }, ["Sent. Listing removed for the searcher (" + o.reason + ")."]);
}

function renderShortlist() {
  const items = DATA.cards.filter((c) => effectiveStatus(c) === "shortlist" && !isFolded(c));
  const view = h("div", { class: "pad" }, [h("h1", {}, ["Your short list"]), h("div", { class: "muted" }, [`${items.length} listings you can trust`])]);
  if (!items.length) view.append(h("p", {}, ["Nothing here yet. Open a listing and tap “Ask the agent for me”."]));
  for (const c of items) {
    const o = outcomes()[c.listing.id];
    const card = renderCard(c);
    const r = o && o.reply;
    if (r) {
      card.append(h("div", { class: "reply small" }, [
        h("div", {}, [h("b", {}, ["Confirmed: "]), "available" + (r.confirmed_price_aed !== null ? ` at ${money(r.confirmed_price_aed, c.listing.offering)}` : "")]),
        r.terms ? h("div", {}, [r.terms]) : null,
        o.slot ? h("div", {}, [h("b", {}, ["Viewing requested: "]), o.slot]) : null,
      ]));
    } else {
      card.append(h("div", { class: "small muted" }, ["Passed every check. Not yet confirmed with the agent."]));
    }
    view.append(card);
  }
  view.append(h("div", { class: "sync" }, [
    h("b", {}, ["Continue on your phone"]),
    h("div", { class: "qr", role: "img", "aria-label": "QR code placeholder" }),
    h("div", { class: "small" }, ["Your short list and agent replies sync to the Property Finder app; replies arrive as notifications."]),
  ]));
  return view;
}

// ---------- intro sheet and boot ----------

function showIntro() {
  if (load(INTRO_KEY, false)) return;
  const sheet = document.getElementById("sheet");
  const close = () => { sheet.hidden = true; save(INTRO_KEY, true); };
  sheet.replaceChildren(h("div", { class: "inner" }, [
    h("h1", {}, ["Your search assistant"]),
    h("p", {}, ["It hides listings that look fake or misleading, tells you why, and asks agents the right questions for you."]),
    h("p", { class: "muted small" }, ["Demo: agent replies are mocked. Listings are real Princess Tower listings, checked on " + (DATA.generated || "an earlier date") + "."]),
    h("button", { class: "btn primary", type: "button", onclick: close }, ["Got it"]),
  ]));
  sheet.hidden = false;
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(url + " " + res.status);
  return res.json();
}

async function boot() {
  try { DATA = await fetchJson("data/listings.json"); }
  catch { DATA = await fetchJson("data/fixture.json"); }
  window.addEventListener("hashchange", route);
  route();
  showIntro();
}

boot().catch((e) => {
  document.getElementById("screen").replaceChildren(h("p", { class: "pad" }, ["Could not load listings data. " + e.message]));
});
