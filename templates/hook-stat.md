# Template: hook-stat

## Purpose
Lead with a bold, specific statistic that reframes the audience's understanding of the topic.

## Visual Layout
- Background: solid colour block (high contrast)
- Top 20%: small category label in caps, muted colour
- Centre 50%: HEADLINE — the stat itself, very large type, 2-3 lines max
- Bottom 30%: SUBTEXT — context that makes the stat meaningful

## Copy Contract
- headline: The stat. Must include a number. Max 8 words. Example: "73% of takedowns happen in the first 30 seconds"
- subtext: Why this matters. Max 25 words. No filler.
- cta: null

## Render Guidance
- render_type: "programmatic"
- Suggested bg_color: "#1a1a2e" (dark navy), "#0d1117" (near-black), "#2d1b69" (deep purple)
- text_color: "#ffffff" or "#f0f0f0"
- accent_color: used for label text

## render_spec Fields
{
  "layout": "hook-stat",
  "bg_color": "#1a1a2e",
  "text_color": "#ffffff",
  "accent_color": "#6c63ff",
  "label": "CATEGORY IN CAPS",
  "step_number": null,
  "step_total": null
}
