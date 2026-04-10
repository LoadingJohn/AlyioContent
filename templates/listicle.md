# Template: listicle

## Purpose
Present ranked tips, tools, or insights as a numbered list. Two modes: teaser (slide 1 hook) or item (one insight per slide).

## Modes
- teaser: Slide 1 only — shows "N things about X" without revealing items. Creates curiosity gap.
- item: Body slides — one ranked item per slide.

## Visual Layout (teaser mode)
- Large total count centred
- Headline below: "N [things] about [topic] most people miss"
- Subtext: brief framing of why this list matters

## Visual Layout (item mode)
- Large rank number top-left in accent colour
- Headline: the tip or insight
- Subtext: explanation or context

## Copy Contract
- headline: Max 8 words
- subtext: Max 25 words
- rank: integer (item mode) | null (teaser mode)
- mode: "teaser" or "item"
- cta: null

Note: rank and mode go inside the copy object in slides.json.

## Render Guidance
- render_type: "programmatic" always

## render_spec Fields
{
  "layout": "listicle",
  "bg_color": "#1a1a2e",
  "text_color": "#ffffff",
  "accent_color": "#ffd700",
  "label": null,
  "step_number": null,
  "step_total": null
}
