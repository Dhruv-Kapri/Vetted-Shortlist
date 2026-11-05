"""Record the narrated demo video (docs/demo.mp4) and the README GIF (docs/walkthrough.gif).

Needs the prototype served at http://localhost:8765 (`cd web && python3 -m http.server 8765`),
Playwright's Chromium, ffmpeg/ffprobe and macOS `say`. Run:

    uv run --with playwright python scripts/demo_video.py

Each scene has a caption (on screen) and a voiceover (macOS "Daniel"). A scene lasts at least as long
as its voiceover plus a pause, so the screens and the voice stay in step.
"""

from __future__ import annotations

import subprocess
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

from playwright.sync_api import Locator, Page, sync_playwright

ROOT: Path = Path(__file__).resolve().parent.parent
BASE_URL: str = "http://localhost:8765/"
VIEWPORT: dict[str, int] = {"width": 390, "height": 844}
VOICE: str = "Daniel"
VOICE_RATE: int = 180
VOICE_PAD_S: float = 0.5
GIF_FPS: int = 8
GIF_WIDTH: int = 360
GIF_SPEED: float = 1.3  # the GIF plays slightly faster than the video to stay under ~6 MB
GIF_COLORS: int = 32

STALE_RENT_ID: str = "165601648"  # stale "available" date; mocked reply says gone
CONFIRMED_RENT_ID: str = "168365745"  # mocked reply: available, ends on the short list
SALE_ID: str = "169247428"

CURSOR_MS: int = 600
HOVER_S: float = 1.0
SETTLE_S: float = 2.0

INIT_JS: str = """
(() => {
  const mount = () => {
    if (document.getElementById('demo-cursor')) return;
    const cur = document.createElement('div');
    cur.id = 'demo-cursor';
    cur.style.cssText = 'position:fixed;left:0;top:0;width:22px;height:22px;margin:-11px 0 0 -11px;' +
      'border-radius:50%;background:rgba(229,72,77,.55);border:3px solid #e5484d;' +
      'box-shadow:0 0 0 3px rgba(255,255,255,.8);pointer-events:none;z-index:2147483647;' +
      'transition:transform 600ms cubic-bezier(.4,0,.2,1);transform:translate(195px,420px);';
    const cap = document.createElement('div');
    cap.id = 'demo-caption';
    cap.style.cssText = 'position:fixed;left:0;right:0;top:0;padding:10px 14px;background:rgba(17,24,32,.88);' +
      'color:#fff;font:600 16px/1.35 -apple-system,Helvetica,Arial,sans-serif;text-align:center;' +
      'pointer-events:none;z-index:2147483646;height:82px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;';
    const pad = document.createElement('style');
    pad.textContent = '#app{padding-top:82px}';
    document.head.append(pad);
    document.body.append(cap, cur);
    window.__cursor = (x, y) => { cur.style.transform = `translate(${x}px,${y}px)`; };
    window.__caption = (t) => { cap.textContent = t; };
    window.__press = () => {
      cur.animate([{ scale: '1' }, { scale: '.6' }, { scale: '1' }], { duration: 250 });
    };
    if (window.__lastCaption) cap.textContent = window.__lastCaption;
  };
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
"""

# (scene_id, caption, voiceover). Caption is on screen; the voiceover says the same, a little fuller.
SCENES: list[tuple[str, str, str]] = [
    ("results", "The assistant checked 32 listings in Princess Tower: 13 on your short list, 14 to confirm with the agent, 5 hidden.",
     "The assistant checked 32 listings in Princess Tower: 13 on your short list, 14 to confirm with the agent, and 5 hidden."),
    ("why-hidden", "Why hidden? Each hidden listing shows its evidence, and you can say if we got it wrong.",
     "Why hidden? Each hidden listing shows its evidence, here the same flat posted twice. And if we got it wrong, you can tell us."),
    ("doubtful", "A doubtful listing: the available date is months old. Before you call, see the checks and registered rents.",
     "Now a doubtful listing. Its available date is months old. Before you call, you see the checks, and the rents registered for flats this size."),
    ("ask-agent", "Ask the agent for me. The questions are written for you. The reply says it is gone, so it is removed.",
     "Tap, ask the agent for me. The questions are already written. The mocked reply says the flat is gone, so it is removed, with the reason."),
    ("agent-view", "The agent gets a pre-qualified lead and answers in one tap: available, gone or price changed.",
     "The agent gets a pre-qualified lead, with budget, move in date and questions, and answers in one tap: available, gone, or price changed. On a second flat, available means it joins the short list."),
    ("buy", "Buy mode runs the same checks on sales, and asks buyer questions: final price, service charge.",
     "Buy mode runs the same checks against registered sales, and asks buyer questions, like final price and service charge."),
    ("shortlist", "Your short list: confirmed with the agent, or not yet confirmed. To rent, and to buy.",
     "Your short list keeps what is confirmed with the agent apart from what is not yet confirmed, grouped as to rent and to buy."),
    ("closing", "Real listings, mocked agent replies. The agent stays in the deal.",
     "Real listings, mocked agent replies. And the agent stays in the deal."),
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def audio_seconds(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    return float(out.strip())


def make_voice(tmp: Path) -> dict[str, tuple[Path, float]]:
    """Render each scene's voiceover. Returns scene_id -> (wav path, seconds)."""
    clips: dict[str, tuple[Path, float]] = {}
    for sid, _cap, text in SCENES:
        aiff, wav = tmp / f"{sid}.aiff", tmp / f"{sid}.wav"
        run(["say", "-v", VOICE, "-r", str(VOICE_RATE), "-o", str(aiff), text])
        run(["ffmpeg", "-y", "-i", str(aiff), "-ar", "44100", "-ac", "1", str(wav)])
        clips[sid] = (wav, audio_seconds(wav))
    return clips


# ---------- browser helpers ----------


def caption(page: Page, text: str) -> None:
    page.evaluate("t => { window.__lastCaption = t; window.__caption(t); }", text)


def smooth_scroll(page: Page, target_y: float, seconds: float = 1.4) -> None:
    page.evaluate(
        """([y, ms]) => new Promise(res => {
            const from = window.scrollY, t0 = performance.now();
            const max = document.documentElement.scrollHeight - innerHeight;
            const to = Math.max(0, Math.min(y, max));
            const step = (now) => {
              const k = Math.min(1, (now - t0) / ms), e = k < .5 ? 2*k*k : 1 - Math.pow(-2*k + 2, 2) / 2;
              window.scrollTo(0, from + (to - from) * e);
              k < 1 ? requestAnimationFrame(step) : res();
            };
            requestAnimationFrame(step);
        })""",
        [target_y, seconds * 1000],
    )


def scroll_to_show(page: Page, loc: Locator) -> None:
    """Scroll slowly so the element sits in the middle of the free area (below the caption)."""
    box = loc.bounding_box()
    assert box is not None
    mid = box["y"] + box["height"] / 2
    if not (120 < mid < 700):
        smooth_scroll(page, page.evaluate("window.scrollY") + mid - 400)


def hover_on(page: Page, loc: Locator) -> None:
    loc.wait_for(state="visible")
    scroll_to_show(page, loc)
    box = loc.bounding_box()
    assert box is not None
    page.evaluate("([x, y]) => window.__cursor(x, y)", [box["x"] + box["width"] / 2, box["y"] + box["height"] / 2])
    time.sleep(CURSOR_MS / 1000 + HOVER_S)


def click_on(page: Page, loc: Locator, settle: float = SETTLE_S) -> None:
    hover_on(page, loc)
    page.evaluate("window.__press()")
    loc.click()
    time.sleep(settle)


def go(page: Page, hash_: str) -> None:
    page.evaluate("h => { location.hash = h; }", hash_)
    time.sleep(0.8)


def reading_scroll(page: Page, step: float = 330, pause: float = 1.2, max_steps: int = 8) -> None:
    """Scroll down a little at a time until the bottom (or max_steps)."""
    for _ in range(max_steps):
        y: float = page.evaluate("window.scrollY")
        maxy: float = page.evaluate("document.documentElement.scrollHeight - innerHeight")
        if y >= maxy - 5:
            break
        smooth_scroll(page, y + step, 1.3)
        time.sleep(pause)


def tap(page: Page, text: str, exact: bool = True) -> Locator:
    return page.get_by_text(text, exact=exact).first


# ---------- scenes ----------


def scene_results(page: Page) -> None:
    time.sleep(1.5)
    click_on(page, page.get_by_role("button", name="Got it"))
    hover_on(page, tap(page, "Why hidden?"))


def scene_why_hidden(page: Page) -> None:
    click_on(page, tap(page, "Why hidden?"), settle=1.0)
    dup = page.locator(".card", has_text="Duplicate.").first
    scroll_to_show(page, dup)
    hover_on(page, dup.get_by_role("button", name="Not right? Tell us"))


def scene_doubtful(page: Page) -> None:
    go(page, "#/results?mode=rent")
    smooth_scroll(page, 0, 0.6)
    time.sleep(1.0)
    click_on(page, page.locator(f'a[href="#/listing/{STALE_RENT_ID}"]').first)
    reading_scroll(page)


def scene_ask_agent(page: Page) -> None:
    click_on(page, page.get_by_role("link", name="Ask the agent for me"))
    click_on(page, page.get_by_role("button", name="Send to agent"), settle=3.5)
    scroll_to_show(page, page.locator(".outcome").first)
    time.sleep(1.0)


def scene_agent_view(page: Page) -> None:
    click_on(page, page.get_by_text("See what the agent receives"))
    reading_scroll(page, step=360, pause=1.0)
    go(page, f"#/agent/{CONFIRMED_RENT_ID}")
    click_on(page, page.get_by_role("button", name="Available at this price"))
    time.sleep(1.0)


def scene_buy(page: Page) -> None:
    go(page, "#/results?mode=rent")
    time.sleep(1.0)
    click_on(page, page.get_by_role("link", name="Buy", exact=True), settle=1.5)
    click_on(page, page.locator(f'a[href="#/listing/{SALE_ID}"]').first)
    smooth_scroll(page, 380, 1.6)
    time.sleep(1.5)
    click_on(page, page.get_by_role("link", name="Ask the agent for me"), settle=1.5)
    time.sleep(1.0)


def scene_shortlist(page: Page) -> None:
    click_on(page, page.locator("#tab-short"), settle=1.5)
    reading_scroll(page, step=420, pause=1.0, max_steps=2)
    buy = page.get_by_role("heading", name="To buy")
    smooth_scroll(page, page.evaluate("window.scrollY") + (buy.bounding_box() or {"y": 0})["y"] - 100, 2.0)
    time.sleep(1.5)


def scene_closing(page: Page) -> None:
    smooth_scroll(page, 0, 1.2)
    time.sleep(3.0)


ACTIONS: dict[str, Callable[[Page], None]] = {
    "results": scene_results,
    "why-hidden": scene_why_hidden,
    "doubtful": scene_doubtful,
    "ask-agent": scene_ask_agent,
    "agent-view": scene_agent_view,
    "buy": scene_buy,
    "shortlist": scene_shortlist,
    "closing": scene_closing,
}


def record(tmp: Path, clips: dict[str, tuple[Path, float]]) -> tuple[Path, dict[str, tuple[float, float]]]:
    """Drive the prototype. Returns (webm path, scene_id -> (start, end) seconds in the video)."""
    spans: dict[str, tuple[float, float]] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport=VIEWPORT, device_scale_factor=2, is_mobile=True, has_touch=False,
            record_video_dir=str(tmp / "video"), record_video_size=VIEWPORT,
        )
        ctx.add_init_script(INIT_JS)
        page = ctx.new_page()
        t0 = time.monotonic()
        page.goto(BASE_URL + "#/results?mode=rent")
        page.wait_for_selector(".bar")
        page.wait_for_selector("#sheet .btn")
        for sid, cap, _voice in SCENES:
            start = time.monotonic() - t0
            caption(page, cap)
            ACTIONS[sid](page)
            need = clips[sid][1] + VOICE_PAD_S
            left = need - (time.monotonic() - t0 - start)
            if left > 0:
                time.sleep(left)
            spans[sid] = (start, time.monotonic() - t0)
        page.evaluate("localStorage.setItem('pfa_intro_seen', 'true')")
        video = page.video
        ctx.close()
        assert video is not None
        path = Path(video.path())
        browser.close()
    return path, spans


def build_audio(tmp: Path, clips: dict[str, tuple[Path, float]], spans: dict[str, tuple[float, float]], lead: float) -> Path:
    cmd: list[str] = ["ffmpeg", "-y"]
    for sid, _c, _v in SCENES:
        cmd += ["-i", str(clips[sid][0])]
    filters: list[str] = []
    for i, (sid, _c, _v) in enumerate(SCENES):
        ms = int((spans[sid][0] + lead) * 1000)
        filters.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(SCENES)))
    filters.append(f"{mix}amix=inputs={len(SCENES)}:normalize=0:dropout_transition=0[out]")
    out = tmp / "voice.wav"
    cmd += ["-filter_complex", ";".join(filters), "-map", "[out]", str(out)]
    run(cmd)
    return out


def encode(webm: Path, audio: Path, total: float, mp4: Path) -> None:
    run([
        "ffmpeg", "-y", "-i", str(webm), "-i", str(audio),
        "-vf", "fps=25",
        "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-t", f"{total:.2f}", "-movflags", "+faststart", str(mp4),
    ])


def make_gif(mp4: Path, gif: Path) -> None:
    vf = f"setpts=PTS/{GIF_SPEED},fps={GIF_FPS},scale={GIF_WIDTH}:-1:flags=lanczos"
    run([
        "ffmpeg", "-y", "-i", str(mp4), "-an",
        "-vf", f"{vf},split[a][b];[a]palettegen=max_colors={GIF_COLORS}:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
        str(gif),
    ])


def main() -> None:
    docs = ROOT / "docs"
    with tempfile.TemporaryDirectory(prefix="demo_video_") as t:
        tmp = Path(t)
        clips = make_voice(tmp)
        webm, spans = record(tmp, clips)
        total = spans[SCENES[-1][0]][1]
        # Playwright's video starts a little before t0 (page creation); lead is that gap.
        lead = 0.0
        audio = build_audio(tmp, clips, spans, lead)
        encode(webm, audio, total, docs / "demo.mp4")
        make_gif(docs / "demo.mp4", docs / "walkthrough.gif")
    for sid, (a, b) in spans.items():
        print(f"{sid:12s} {a:6.1f} - {b:6.1f}  voice {clips[sid][1]:.1f}s")
    print(f"total {total:.1f}s")


if __name__ == "__main__":
    main()
