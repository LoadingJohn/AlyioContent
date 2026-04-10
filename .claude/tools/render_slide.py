#!/usr/bin/env python3
import argparse
import json
import os
import sys


def load_font(size):
    from PIL import ImageFont
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def parse_color(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 6:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return (0, 0, 0)


def color_with_alpha(color_hex, alpha_float):
    r, g, b = parse_color(color_hex)
    return (r, g, b, int(255 * alpha_float))


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_centered_wrapped(draw, text, font, canvas_size, y_start, color, margin=80):
    max_w = canvas_size - margin * 2
    lines = wrap_text(text, font, max_w, draw)
    bbox = draw.textbbox((0, 0), "A", font=font)
    line_h = (bbox[3] - bbox[1]) + 8
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (canvas_size - w) // 2
        draw.text((x, y), line, font=font, fill=color)
        y += line_h
    return y


def draw_left_wrapped(draw, text, font, x, y_start, max_width, color):
    lines = wrap_text(text, font, max_width, draw)
    bbox = draw.textbbox((0, 0), "A", font=font)
    line_h = (bbox[3] - bbox[1]) + 8
    y = y_start
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += line_h
    return y


def render_hook_stat(img, draw, spec, copy, size):
    bg = parse_color(spec["bg_color"])
    img.paste(bg, [0, 0, size, size])

    accent = parse_color(spec["accent_color"])
    text_color = parse_color(spec["text_color"])
    text_alpha = color_with_alpha(spec["text_color"], 0.8)

    label_font = load_font(22)
    label = copy.get("label", "").upper()
    bbox = draw.textbbox((0, 0), label, font=label_font)
    lw = bbox[2] - bbox[0]
    draw.text(((size - lw) // 2, 60), label, font=label_font, fill=accent)

    headline_font = load_font(84)
    draw_centered_wrapped(draw, copy.get("headline", ""), headline_font, size, 300, text_color)

    sub_font = load_font(36)
    draw_centered_wrapped(draw, copy.get("subtext", ""), sub_font, size, 650, text_alpha)


def render_step_by_step(img, draw, spec, copy, size):
    bg = parse_color(spec["bg_color"])
    img.paste(bg, [0, 0, size, size])

    accent = parse_color(spec["accent_color"])
    text_color = parse_color(spec["text_color"])
    text_alpha = color_with_alpha(spec["text_color"], 0.8)
    muted = color_with_alpha(spec.get("text_color", "#888888"), 0.5)

    step_num = str(copy.get("step_number", spec.get("step_number", "1")))
    step_total = str(copy.get("step_total", spec.get("step_total", "1")))

    num_font = load_font(120)
    draw.text((80, 80), step_num, font=num_font, fill=accent)

    prog_font = load_font(24)
    prog_text = f"Step {step_num} of {step_total}"
    bbox = draw.textbbox((0, 0), step_num, font=num_font)
    prog_y = 80 + (bbox[3] - bbox[1]) + 8
    draw.text((80, prog_y), prog_text, font=prog_font, fill=muted)

    hl_font = load_font(56)
    max_w = size - 80 - 80
    draw_left_wrapped(draw, copy.get("headline", ""), hl_font, 80, 400, max_w, text_color)

    sub_font = load_font(32)
    draw_left_wrapped(draw, copy.get("subtext", ""), sub_font, 80, 520, max_w, text_alpha)


def render_comparison(img, draw, spec, copy, size):
    from PIL import Image as PILImage
    from PIL import ImageDraw as PILImageDraw

    bg = parse_color(spec["bg_color"])
    img.paste(bg, [0, 0, size, size])

    accent_rgb = parse_color(spec["accent_color"])
    text_color = parse_color(spec["text_color"])
    text_alpha = color_with_alpha(spec["text_color"], 0.8)

    overlay = PILImage.new("RGBA", (size, size), (0, 0, 0, 0))
    ov_draw = PILImageDraw.Draw(overlay)

    left_tint = (*accent_rgb, int(255 * 0.1))
    ov_draw.rectangle([0, 0, size // 2, size], fill=left_tint)

    r2 = min(255, 255 - accent_rgb[0] + 30)
    g2 = min(255, 255 - accent_rgb[1] + 30)
    b2 = min(255, 255 - accent_rgb[2] + 30)
    right_tint = (r2, g2, b2, int(255 * 0.1))
    ov_draw.rectangle([size // 2, 0, size, size], fill=right_tint)

    rgba_img = img.convert("RGBA")
    rgba_img = PILImage.alpha_composite(rgba_img, overlay)
    img.paste(rgba_img.convert(img.mode))

    draw.line([(size // 2, 0), (size // 2, size)], fill=parse_color(spec["accent_color"]), width=2)

    badge_font = load_font(28)
    badge_text = "VS"
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    bx = size // 2 - bw // 2
    by = size // 2 - bh // 2
    pad = 12
    draw.ellipse([bx - pad, by - pad, bx + bw + pad, by + bh + pad], fill=parse_color(spec["accent_color"]))
    draw.text((bx, by), badge_text, font=badge_font, fill=(255, 255, 255))

    hl_font = load_font(40)
    bbox = draw.textbbox((0, 0), copy.get("headline", ""), font=hl_font)
    hw = bbox[2] - bbox[0]
    draw.text(((size - hw) // 2, 60), copy.get("headline", ""), font=hl_font, fill=text_color)

    panel_x = 80
    panel_w = size // 2 - 80 - 20
    label_font = load_font(32)
    body_font = load_font(26)

    draw_left_wrapped(draw, copy.get("left_label", ""), label_font, panel_x, 160, panel_w, text_color)
    draw_left_wrapped(draw, copy.get("left_body", ""), body_font, panel_x, 220, panel_w, text_alpha)

    right_x = size // 2 + 40
    draw_left_wrapped(draw, copy.get("right_label", ""), label_font, right_x, 160, panel_w, text_color)
    draw_left_wrapped(draw, copy.get("right_body", ""), body_font, right_x, 220, panel_w, text_alpha)

    sub_font = load_font(28)
    bbox = draw.textbbox((0, 0), copy.get("subtext", ""), font=sub_font)
    sw = bbox[2] - bbox[0]
    draw.text(((size - sw) // 2, size - 80), copy.get("subtext", ""), font=sub_font, fill=text_alpha)


def render_listicle_teaser(img, draw, spec, copy, size):
    import re
    bg = parse_color(spec["bg_color"])
    img.paste(bg, [0, 0, size, size])

    accent = parse_color(spec["accent_color"])
    text_color = parse_color(spec["text_color"])
    text_alpha = color_with_alpha(spec["text_color"], 0.8)

    headline = copy.get("headline", "")
    numbers = re.findall(r"\d+", headline)
    count_str = numbers[0] if numbers else ""

    count_font = load_font(160)
    hl_font = load_font(44)
    sub_font = load_font(32)

    y = size // 2 - 140
    if count_str:
        bbox = draw.textbbox((0, 0), count_str, font=count_font)
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        draw.text(((size - cw) // 2, y), count_str, font=count_font, fill=accent)
        y += ch + 16

    y = draw_centered_wrapped(draw, headline, hl_font, size, y, text_color)
    draw_centered_wrapped(draw, copy.get("subtext", ""), sub_font, size, y + 12, text_alpha)


def render_listicle_item(img, draw, spec, copy, size):
    bg = parse_color(spec["bg_color"])
    img.paste(bg, [0, 0, size, size])

    accent = parse_color(spec["accent_color"])
    text_color = parse_color(spec["text_color"])
    text_alpha = color_with_alpha(spec["text_color"], 0.8)

    rank = str(copy.get("rank", "1"))
    rank_font = load_font(120)
    draw.text((80, 80), rank, font=rank_font, fill=accent)

    max_w = size - 80 - 80
    hl_font = load_font(56)
    draw_left_wrapped(draw, copy.get("headline", ""), hl_font, 80, 400, max_w, text_color)

    sub_font = load_font(32)
    draw_left_wrapped(draw, copy.get("subtext", ""), sub_font, 80, 520, max_w, text_alpha)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--copy", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--size", type=int, default=1080)
    args = parser.parse_args()

    try:
        spec = json.loads(args.spec)
        copy = json.loads(args.copy)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        sys.exit(1)

    size = args.size
    bg_color = parse_color(spec.get("bg_color", "#000000"))
    img = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    layout = spec.get("layout", "")
    try:
        if layout == "hook-stat":
            render_hook_stat(img, draw, spec, copy, size)
        elif layout == "step-by-step":
            render_step_by_step(img, draw, spec, copy, size)
        elif layout == "comparison":
            render_comparison(img, draw, spec, copy, size)
        elif layout == "listicle":
            mode = copy.get("mode", "teaser")
            if mode == "teaser":
                render_listicle_teaser(img, draw, spec, copy, size)
            else:
                render_listicle_item(img, draw, spec, copy, size)
        else:
            print(f"Unknown layout: {layout}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Render error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        out_dir = os.path.dirname(args.out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        img.save(args.out, "PNG")
    except Exception as e:
        print(f"Failed to save image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
