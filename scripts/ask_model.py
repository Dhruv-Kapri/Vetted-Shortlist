"""Ask a model factual questions about this building and UAE renting/buying, save answers verbatim.

The answers are then checked by hand against the listing pages and registered contracts (AI-LOG.md).
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

MODEL: str = "claude-sonnet-5-5"
QUESTIONS: list[str] = [
    "What is the typical yearly rent for a 2-bedroom apartment (about 1,190 sqft) in Princess Tower, Dubai Marina, right now? Give one number range.",
    "What does a 2-bedroom apartment of about 1,190 sqft sell for in Princess Tower, Dubai Marina, right now? Give one number range.",
    "A 2-bedroom in Princess Tower, Dubai Marina is listed at AED 85,000 a year. Is that a good deal or a red flag? One short paragraph.",
    "On Property Finder UAE, what does the 'Verified' badge on a listing mean exactly?",
    "In Dubai, can an agent legally advertise a property online without a permit? What permit, and how can a renter check it?",
    "In Dubai, how much is the security deposit, the agency fee and the Ejari fee for a yearly apartment rental? Give typical numbers.",
    "In Dubai, can a landlord raise the rent at renewal by any amount they like?",
    "When buying a resale apartment in Dubai, what fees does the buyer pay on top of the price? List them with typical amounts.",
    "Is Princess Tower in Dubai Marina the tallest residential building in Dubai today?",
]


def main(out: Path) -> None:
    load_dotenv()
    client = anthropic.Anthropic()
    rows: list[dict[str, str]] = []
    for q in QUESTIONS:
        msg = client.messages.create(model=MODEL, max_tokens=3000, messages=[{"role": "user", "content": q}])
        text = "".join(b.text for b in msg.content if b.type == "text")
        rows.append({"question": q, "answer": text})
        print("Q:", q, "\nA:", text, "\n", flush=True)
    out.write_text(json.dumps({"model": MODEL, "asked_at": datetime.now(UTC).isoformat(), "rows": rows}, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
