#!/usr/bin/env python3
import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--model", default="gemini-2.0-flash-exp")
    args = parser.parse_args()

    try:
        prompt_data = json.loads(args.prompt)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        import google.generativeai as genai
    except ImportError:
        print("google-generativeai not installed. Run: pip install google-generativeai", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(2)

    subject = prompt_data.get("subject", "")
    style = prompt_data.get("style", "")
    mood = prompt_data.get("mood", "")
    avoid = prompt_data.get("avoid", "")
    fmt = prompt_data.get("format", "Square 1:1, Instagram carousel")

    prompt_str = f"{subject}. Style: {style}. Mood: {mood}. Format: {fmt}. Do not include: {avoid}."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(args.model)
        response = model.generate_content(
            prompt_str,
            generation_config={"response_mime_type": "image/png"},
        )
    except Exception as e:
        err = str(e)
        if "401" in err or "403" in err or "API key" in err.lower() or "authentication" in err.lower() or "permission" in err.lower():
            print(f"API auth failure: {e}", file=sys.stderr)
            sys.exit(2)
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        image_bytes = None
        if hasattr(response, "candidates") and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    image_bytes = part.inline_data.data
                    break

        if image_bytes is None:
            print("No image data in response", file=sys.stderr)
            sys.exit(1)

        out_dir = os.path.dirname(args.out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(args.out, "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        print(f"Failed to save image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
