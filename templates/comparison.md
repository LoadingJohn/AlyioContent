# Template: comparison

## Purpose
Show two contrasting approaches side by side. Reader leaves knowing which to prefer and why.

## Visual Layout
- Canvas split vertically 50/50: left panel vs right panel
- Left: Option A label + body (typically the common/less-optimal approach)
- Right: Option B label + body (typically the better approach)
- Centre divider: "VS" badge
- Top: headline naming what is being compared

## Copy Contract
- headline: Names the comparison. Max 8 words. Example: "Pulling guard vs shooting for takedowns"
- subtext: The key insight — what makes one better. Max 25 words.
- left_label: Option A name, 3-5 words
- left_body: Option A description, 10-15 words
- right_label: Option B name, 3-5 words
- right_body: Option B description, 10-15 words
- cta: null

Note: left_label, left_body, right_label, right_body go inside the copy object in slides.json.

## Render Guidance
- render_type: "programmatic" for text-only comparison
- render_type: "gemini" if comparison has a strong visual metaphor (two postures, two objects, two environments)

## render_spec Fields
{
  "layout": "comparison",
  "bg_color": "#ffffff",
  "text_color": "#0d1117",
  "accent_color": "#ff4757",
  "label": null,
  "step_number": null,
  "step_total": null
}
