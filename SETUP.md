# Profile installation and remaining inputs

This is a standalone profile package. The neighboring Peoplix project was not modified.

## Inspection

On 6 November 2026, the public GitHub API returned 404 for the README of `erenseret56-del/erenseret56-del`. It was not available for inspection. The similarly named [erenseret-del repository](https://github.com/erenseret56-del/erenseret-del) contains only `# erenseret-del`. Do not rename or overwrite that repository as part of this setup.

The hero uses a self-contained animated SVG with a JARVIS-inspired infinity core. It has no character artwork, external video, JavaScript, or WebGL dependency.

Verified project sources:

- [Jarvis package.json](https://github.com/erenseret56-del/Jarvis-/blob/main/package.json): React, TypeScript, Three.js and Vite.
- [Synthora README](https://github.com/erenseret56-del/synthora): React, TypeScript, Supabase and a Python backend. A [related workspace](https://github.com/erenseret56-del/Synthora-work) also exists; both are linked, without claiming which is canonical.
- Local `Peoplix-main/package.json` and `backend/package.json`: React, TypeScript, Tailwind CSS, Node.js, Fastify and MongoDB. Express is part of your confirmed general toolkit, not claimed as Peoplix's framework.
- You supplied `https://peoplix.ai` and `https://stackweb.net` and confirmed experience with the requested toolkit through development tools and work at Peoplix.

## Install

1. Use a **public** repository named exactly `erenseret56-del` under your `erenseret56-del` account. If it already exists privately, inspect its contents before merging these files. Do not overwrite an existing README without retaining it in Git history.
2. Add this package's `README.md`, `assets/`, `.github/workflows/snake.yml`, and optionally `scripts/` and this guide to its root. Commit normally on its default branch. Do not put this inside the Peoplix repository.
3. In repository **Settings → Actions → General**, enable Actions and permit the actions used by the workflow. The workflow requests job-level `contents: write` for the built-in `GITHUB_TOKEN`; no PAT or custom secret is required. Organization policies may limit that permission.
4. In **Actions → Generate contribution snake → Run workflow**, start the first run. The workflow creates `output` if absent, or adds a commit to it while preserving history and unrelated files. Generated snake filenames are refreshed. GitHub Pages is not required.
5. Confirm all three images are present on `output`. README animation URLs intentionally target those future generated files and will not resolve before the first successful run.

The daily schedule is 00:17 UTC / 05:47 India time, subject to GitHub scheduling delays. Scheduled workflows must be on the default branch and may be disabled by GitHub after inactivity. Re-enable them in Actions if necessary. Branch rules must allow the workflow to write to `output`; no force push is needed.

## Updating hero motion

The current hero is `assets/jarvis-infinity.svg`: an animated SVG with rotating HUD rings, a holographic infinity core, energy pulses, and particle movement. It is designed for GitHub's image rendering limits and loops without JavaScript.

To change the motion or colours, edit `assets/jarvis-infinity.svg`. SVG project cards can be rebuilt with `python scripts/build-cards.py`; keep their accessible descriptions in the README in sync.

## Inputs still needed

| Item | Needed |
| --- | --- |
| Reference | Original screenshot, if matching its precise composition is desired |
| Hero artwork | Optional custom infinity-core variant, if you want a different animation treatment |
| ASTER | Repository URL, demo URL and actual project stack |
| Peoplix | Repository URL, or confirmation it should remain private/unlinked |
| Synthora | Preferred primary repository and live demo URL, if any |
| Jarvis | Live demo URL, if any |
| PRIME FLEX | Repository URL, confirmed demo URL and actual project stack |
| Learning | Specific current learning topics; not inferred from the toolkit |
| Contact | Email, LinkedIn and other personal social links you want public |

Your Stackweb site lists a Prime Flex project, but the exact demo should be confirmed before adding it here. No social link on the business website is assumed to be your personal account.

## Rendering and services

GitHub controls the page background and font. The navy surfaces and monospace styling live inside local images; the document uses supported Markdown, HTML images, tables, anchor links and picture sources. There is no README JavaScript or custom CSS. Cards stack vertically; the toolkit wraps icons into short rows. Text equivalents accompany images.

Account statistics, top languages and contribution activity are local, dated snapshots of real public GitHub data. Refresh them with `python scripts/build-stats.py` and commit the changed assets. This uses the public GitHub REST API and public contribution calendar, not invented metrics. Public API rate limits apply. The activity card shows GitHub's intensity levels, not inferred contribution counts; the parser fails without overwriting the previous assets if the calendar structure changes.

During verification, the public GitHub Readme Stats endpoint returned HTTP 503 and the Activity Graph endpoint returned HTTP 402, so neither is embedded. The remaining icon and streak URLs follow their maintainers' documented formats:

- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats)
- [Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats)
- [Activity Graph](https://github.com/Ashutosh00710/github-readme-activity-graph)
- [Skill Icons](https://github.com/tandpfun/skill-icons)
- [Platane/snk](https://github.com/Platane/snk) for SVG and GIF generation
- [actions-gh-pages](https://github.com/peaceiris/actions-gh-pages) for publication with `keep_files: true` and `force_orphan: false`

These public image services can be rate-limited or unavailable. The profile links to GitHub as a fallback and makes no promise about their uptime. Profile view counts are omitted because a reliable, accurate counter was not established; image-load counters do not measure unique people.

The workflow has not run remotely. Publication and account-level settings require installing this package in the actual profile repository. No repositories, branches or commits were changed remotely.
