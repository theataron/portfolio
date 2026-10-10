# Portfolio

Static multi-page site. No build step needed to view it. Open `index.html` in a browser.

## Pages

| File | What's on it |
|---|---|
| `index.html` | Intro, the facts strip, the shelf, four work cards, Things I built, About and the work experience timeline |
| `airhint.html` | AirHint case study: revenue model, paid search, SEO, traffic analysis, CRO, CRM |
| `publicis.html` | Publicis Instagram relaunch case study |
| `synetech.html` | Synetech LinkedIn content strategy case study |
| `research.html` | MSc thesis, AI recommendations and product choice |
| `research-booking.html` | BSc research, website nudges on booking sites |
| `content.html` | Post examples |
| `skills.html` | Skills with proof, and the searchable tools list |
| `about.html` | Volunteering, outside work, quotes, contact |

Every page carries the same sidebar, a light and dark switch, and ends with "Want to browse
more?" links plus a Connect button.

## Files

```
index.html  airhint.html  publicis.html  research.html
content.html  skills.html  about.html
style.css                     all styling, shared
_build/build.py               regenerates the pages (ignored by GitHub Pages)
assets/
  aron.jpg                    profile photo
  signature.png               signature, white strokes on transparent
  cv.pdf                      CV, linked from every page
  thesis-chart.jpg
  publicis-instagram-report.pdf
  publicis/                   pages pulled out of the report deck
  work/                       Instagram post images and the Rokonszavak logo
```

The four original Instagram downloads in `assets/work` with long numeric filenames are unused and can be deleted. When the CV changes, replace `assets/cv.pdf` and keep the filename.

## Editing

`_build/build.py` holds the page content and generates all seven HTML files, so the sidebar and footer stay identical everywhere. Changing the HTML by hand works too, but a later run of the script would overwrite it. GitHub Pages ignores folders starting with an underscore, so `_build` never gets published.

## Publishing to GitHub Pages

The repository name decides the URL. A repo named `<username>.github.io` is served at the
root of that address; any other name is served from a sub-path.

| Repo name | Live at |
|---|---|
| `theataron.github.io` | `https://theataron.github.io` |
| `portfolio` | `https://theataron.github.io/portfolio/` |

Steps:

1. Create a repository on github.com named `theataron.github.io`, public.
2. Drag in every file and folder except `_build`.
3. Settings, then Pages, set Source to the `main` branch, root folder.
4. Live within a minute or two.

`_build` can be committed safely if you prefer. GitHub Pages ignores folders whose name
starts with an underscore, so it is never published either way.

### Using your own domain instead

Buy a domain, add a file called `CNAME` at the root of the repo containing nothing but the
domain, then point the domain's DNS at GitHub:

- four `A` records on the apex: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- one `CNAME` record on `www` pointing at `theataron.github.io`

Then in Settings, Pages, enter the domain and tick Enforce HTTPS once the certificate is issued.

## Numbers used on the page

Both figure sets come from the same Publicis report and measure different things:

- **Per post, Q4 2024 vs Jan–Apr 2025:** +57% views, +16% likes, +388% shares, +105% saves, 18 comments against 0.
- **Monthly totals, Dec 2024 to Apr 2025:** views 8,926 to 31,386, interactions 197 to 590, profile visits 478 to 1,117, followers 1,288 to 1,409.
- **Engagement rate:** 4.31%, highest of the five agency accounts tracked. Next highest 3.16%.
- **Best post:** White Lotus, 3,799 views, 135 likes, 11 shares, 11 saves.

## Sources cited

- "You cannot wish for an easy life and a good character" — Alex Hormozi.
- "No one knows enough to be a pessimist" — Wayne Dyer.
- "Be curious, not judgmental" — from Ted Lasso, which credits Walt Whitman, who never wrote it.
- The hundred days of rejection tasks — Jia Jiang's project, built on Jason Comely's Rejection Therapy game.
