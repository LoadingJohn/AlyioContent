# Template: step-by-step

## Purpose
Teach a specific technique or process as numbered steps. Each slide = one step.

## Visual Layout
- Background: consistent colour across all step slides in the carousel
- Top: large step number in accent colour + step title bold
- Middle: step description (subtext)
- Bottom strip: "Step N of M" progress indicator

## Copy Contract
- headline: "Step N: [action verb] + [object]". Max 8 words. Example: "Step 2: Break the grip before pulling"
- subtext: What to do and why. Specific. Max 25 words.
- cta: null (except final slide)

## Render Guidance
- render_type: "programmatic"
- Keep bg_color consistent across all step slides

## render_spec Fields
{
  "layout": "step-by-step",
  "bg_color": "#0d1117",
  "text_color": "#ffffff",
  "accent_color": "#00d4aa",
  "label": null,
  "step_number": 2,
  "step_total": 5
}
