---
name: stitch-design-pro
description: "Generates production-grade, highly cohesive DESIGN.md files and tailored prompts for Google Stitch (stitch.withgoogle.com) to eliminate AI-generated slop and enforce design tokens."
version: 1.0.0
author: Open Community
---

# Stitch Design Pro (SKILL.md)

AI-native Design System Generator and Guardian for **Google Stitch** (`stitch.withgoogle.com`).
Eliminates fragmented, generic, "AI-slop" interfaces by synthesizing rigorous, production-grade `DESIGN.md` tokens and injecting them into every Stitch canvas prompt.

## Capabilities
1. **Interactive Design System Discovery**: Asks 4 targeted questions to craft the exact Design DNA (industry archetype, 60-30-10 palette, 8pt grid, WCAG AA contrast).
2. **Deep UI/UX Intelligence Integration**: Seamlessly leverages `ui-ux-pro-max` search engine when installed locally, with built-in zero-dependency fallbacks for 20+ industries.
3. **Stitch Prompt Enhancer**: Generates prompt wrappers that bind Stitch's Gemini models to strict token constraints.

## When to Use This Skill
- User wants to create a new project or screen on Google Stitch (`stitch.withgoogle.com`).
- User complains about inconsistent styling, weird colors, or "AI slop" across generated screens.
- User wants a single source of truth (`DESIGN.md`) for their app UI.

---

## Instructions for AI Agents

### Step 1: Discover or Infer Project Requirements
Identify the following core parameters from the user's prompt or conversation history:
- **Product Domain**: (e.g. Fintech, Healthcare, E-Commerce, SaaS, Social, Fitness)
- **Target Platform**: `mobile` (default) or `web`
- **Visual Tone**: Minimalist, Dark OLED, Enterprise Trust, Playful Vibrant, etc.
- **Brand Primary Color**: (Hex code or mood direction)

If the user has not specified details, run the CLI tool in interactive mode or run with inferred parameters:
```bash
python3 generator.py "<query>" -p "<ProjectName>" --platform <mobile|web> -o DESIGN.md --prompt-for "<Screen Description>"
```

### Step 2: Ensure Strict Negative Constraints
Every generated `DESIGN.md` MUST include the anti-slop rules:
- ❌ **No Arbitrary Gradients**: Solid canvas and surface tokens only.
- ❌ **No Mixed Icon Families**: Strict Lucide/Feather outline 2px stroke.
- ❌ **No Heavy Drop Shadows**: Use 1px borders (`#E2E8F0` or `#334155`) or subtle 2px blur elevation.
- ❌ **Touch Target Rule**: All interactive buttons strictly `48px` height.

### Step 3: Handoff to Stitch
Guide the user to:
1. Upload or paste `DESIGN.md` into their Google Stitch canvas project.
2. Use the generated `PROMPT_DESIGN.md` to create individual screens sequentially while preserving token inheritance.
