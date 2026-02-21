#!/usr/bin/env python3
"""
ai_update.py — Local AI Content Assistant
Uses Ollama (phi3:mini) running locally to generate and update website content.

Usage:
    python ai_update.py "update my bio to talk about being a CS student interested in AI"
    python ai_update.py "rewrite services to focus on data science consulting"
    python ai_update.py "change my title to Machine Learning Engineer"
"""

import json
import pathlib
import sys
import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT_FILE = ROOT / "content.json"
MODEL = "phi3:mini"
OLLAMA_URL = "http://localhost:11434/api/generate"


def call_ollama(prompt: str) -> str:
    """Send a prompt to the local Ollama model via HTTP API."""
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 1024},
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "").strip()
    except urllib.error.URLError:
        print("❌ Can't connect to Ollama. Make sure it's running:")
        print("   ollama serve")
        sys.exit(1)
    except TimeoutError:
        print("❌ Ollama took too long. Try a simpler request.")
        sys.exit(1)


def extract_json(text: str) -> dict | None:
    """Try to extract a JSON object from LLM response text."""
    # Strip markdown code fences if present
    cleaned = text.strip()
    if "```" in cleaned:
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    # Find the JSON object boundaries
    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1
    if start == -1 or end == 0:
        return None

    try:
        return json.loads(cleaned[start:end])
    except json.JSONDecodeError:
        return None


def main() -> None:
    if len(sys.argv) < 2:
        print("╔══════════════════════════════════════════════════╗")
        print("║   🤖  AI Website Content Assistant (Ollama)     ║")
        print("╚══════════════════════════════════════════════════╝")
        print()
        print("Usage: python ai_update.py \"<your request>\"")
        print()
        print("Examples:")
        print('  python ai_update.py "change my name to John Smith"')
        print('  python ai_update.py "update bio to talk about data science"')
        print('  python ai_update.py "rewrite services for cybersecurity"')
        print('  python ai_update.py "change email to john@example.com"')
        sys.exit(0)

    user_request = " ".join(sys.argv[1:])

    # Load current content
    data = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))

    print("╔══════════════════════════════════════════════════╗")
    print("║   🤖  AI Website Content Assistant (Ollama)     ║")
    print("╚══════════════════════════════════════════════════╝")
    print()
    print(f"  Model:   {MODEL}")
    print(f"  Request: {user_request}")
    print()
    print("  ⏳ Generating with local AI (this may take a minute)...")
    print()

    # Keep the prompt short and focused for faster CPU inference
    prompt = (
        "You are a JSON editor. Here is a JSON object:\n\n"
        + json.dumps(data, indent=2)
        + "\n\nApply this change: \""
        + user_request
        + '"\n\nReturn ONLY the updated JSON. No explanation.'
    )

    response = call_ollama(prompt)
    updated_data = extract_json(response)

    if updated_data is None:
        print("  ⚠️  Couldn't parse AI response. Raw output:")
        print()
        print(response)
        print()
        print("  Try a simpler request, e.g.: \"change the name to John Smith\"")
        sys.exit(1)

    # Show changes
    print("  ✅ Changes detected:")
    print()

    changes_found = False
    for key in data:
        if key == "services":
            for i, (old_s, new_s) in enumerate(
                zip(data.get("services", []), updated_data.get("services", []))
            ):
                if old_s != new_s:
                    print(f"    📋 Service {i+1} ({new_s.get('title', '?')}): updated")
                    changes_found = True
            if len(updated_data.get("services", [])) != len(data.get("services", [])):
                print(f"    📋 Services count: {len(data['services'])} → {len(updated_data.get('services', []))}")
                changes_found = True
        elif key == "contact":
            for ck in set(list(data.get("contact", {}).keys()) + list(updated_data.get("contact", {}).keys())):
                old_v = data.get("contact", {}).get(ck, "")
                new_v = updated_data.get("contact", {}).get(ck, "")
                if old_v != new_v:
                    print(f"    📇 {ck}: \"{old_v}\" → \"{new_v}\"")
                    changes_found = True
        else:
            old_v = str(data.get(key, ""))
            new_v = str(updated_data.get(key, ""))
            if old_v != new_v:
                print(f"    ✏️  {key}: \"{old_v[:50]}...\" → \"{new_v[:50]}...\"")
                changes_found = True

    if not changes_found:
        print("    (no changes detected)")
        return

    # Ask for confirmation
    print()
    confirm = input("  Apply these changes? (y/n): ").strip().lower()
    if confirm != "y":
        print("  ❌ Changes discarded.")
        return

    # Save
    CONTENT_FILE.write_text(
        json.dumps(updated_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print()
    print(f"  💾 Saved to {CONTENT_FILE.name}")

    # Rebuild site
    print("  🔨 Rebuilding site...")
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "build_site.py")], check=True)

    print()
    print("  🚀 Done! To deploy, run:")
    print('     git add -A; git commit -m "AI-updated content"; git push origin main')
    print()


if __name__ == "__main__":
    main()
