# toppk.github.io

The source for [toppk.github.io](https://toppk.github.io/), a static directory of selected public projects and contributions. Each listing has a source link and a project-site link.

## Build

Run `python3 tools/build-pages.py` from the repository root. It validates `pages/projects.toml` and writes `dist-pages/`. The GitHub Actions workflow publishes only that generated directory. In repository Pages settings, use **GitHub Actions** as the build source.

## Edit the directory

`pages/projects.toml` is a generated copy of the catalog maintained in the owner's branding workspace. Publish catalog changes from that workspace; edit this repository for layout, styling, and build behavior. `published` controls whether an entry appears on the site. `status` describes the project's lifecycle; `type` is its primary kind; `tags` add searchable topics. `pages_enabled` records GitHub Pages metadata even when the linked site is external. The two descriptions serve different purposes: `repo_description` mirrors GitHub About, and `branding_description` is copy for this site. Keep the catalog public.

The theme is in `pages/theme/`, with site-specific styling and filtering in `pages/home.css` and `pages/home.js`. The [x.bllue.org](https://x.bllue.org/) switchboard is a separate site.
