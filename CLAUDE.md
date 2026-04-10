# Claude Instructions

## Branch Strategy
- Always branch from `main`
- Always target `main` for pull requests
- Use short-lived branches per issue only
- Never create long-lived feature branches

## File Management
- Do NOT create documentation files (.md, README, CHANGELOG, etc.) unless explicitly requested
- Do NOT create example files, sample files, or placeholder files
- Only create or modify files directly required by the issue
- If a file is deleted from main, do not recreate it

## Code Standards
- Keep changes minimal and scoped to the issue
- Do not refactor unrelated code
- Do not add comments unless the code is genuinely complex
- Do not make sample code that is not ready for production systems

## Pull Requests
- Keep PR descriptions short and factual
- Do not add lengthy summaries or documentation in PR body
- Always open a pull request after committing changes, do not wait to be asked
- Always include "Closes #[issue-number]" in the PR description so the issue auto-closes on merge
- Target `main` branch for all pull requests

## Planning
- Use plan mode for any task that requires more than 3 steps

## Communication Style
From now on remove all filler words. No 'the', 'is', 'am', 'are'. Direct answer only. Use short 3-5 word sentences. Run tools first, show the result. Do not narrate. Example: Instead 'The solution is to use async', say 'Use async'.

## Content Pipeline

### Trigger
User says: "Create carousel about [topic]"

### Output Location
`posts/YYYY-MM-DD/[topic-slug]/` where YYYY-MM-DD is today's date and topic-slug is the topic lowercased with spaces replaced by hyphens.

### Steps

**Step 1: Research**
Invoke agent `researcher` with:
- topic: the topic string
- lookback_days: 60

Store the returned JSON array as `research_findings`.

**Step 2: Build Slides**
Invoke agent `slide-builder` with:
- research: research_findings
- output_dir: absolute path to `posts/YYYY-MM-DD/topic-slug`
- topic: the topic string

Wait for confirmation that `slides.json` is written and PNGs are rendered.

**Step 3: Critic Loop (max 3 iterations)**

Set `iteration = 1`.

Repeat:
1. Invoke agent `critic` with:
   - slides_json_path: absolute path to `slides.json`
   - iteration: current iteration number
2. Receive critic JSON response. Merge `critic_score` and `critic_notes` from each slide entry back into `slides.json` (write the updated array to disk).
3. If `critic.pass == true` OR `iteration == 3`:
   - Set `finalized: true` on all slides in `slides.json` (write to disk)
   - Break loop
4. Else:
   - Invoke agent `slide-builder` with:
     - research: research_findings
     - output_dir: same path as Step 2
     - topic: the topic string
     - revision_mode: true
     - critic_feedback: the full critic JSON response
   - Increment `iteration` by 1

**Step 4: Generate Caption**
Invoke agent `slide-builder` with:
- caption_mode: true
- slides_json_path: absolute path to `slides.json`
- topic: the topic string
- research: research_findings

This writes `caption.txt` to the output directory.

**Step 5: Report**
Tell the user:
- Output directory path
- Number of slides generated
- Final critic overall_score
- Path to caption.txt

### Pipeline Rules
- Pass only the explicit fields listed above to each agent — never the full session history
- Always pass `research_findings` to slide-builder on every invocation (needed for revision context)
- If any render script exits non-zero: stop the pipeline and report the error immediately
- The orchestrator (not the critic) merges critic scores into slides.json — the critic only reads files
- The critic MUST read each slide PNG image before scoring — visual assessment is required
