#!/usr/bin/env python3
"""Build the public account-root Pages site from the curated TOML catalog."""

from html import escape
from pathlib import Path
import re
import shutil

from projects import ROOT, load_projects


OUTPUT = ROOT / "dist-pages"
PAGES = ROOT / "pages"


def card(project, index):
    name = escape(project["name"], quote=True)
    category = escape(project["category"], quote=True)
    description = escape(project["branding_description"], quote=True)
    role = escape(project["role"], quote=True)
    project_type = escape(project["type"].capitalize())
    status = escape(project["status"].capitalize())
    tags = "".join(f"<span>{escape(tag)}</span>" for tag in project["tags"])
    symbol = escape(project["symbol"], quote=True)
    url = escape(project["site_url"], quote=True)
    repo = escape(f"https://github.com/toppk/{project['name']}", quote=True)
    search = escape(f"{project['name']} {project['branding_description']} {project['category']} {project['role']} {project['type']} {project['status']} {' '.join(project['tags'])}".lower(), quote=True)
    return f"""
  <article class="project-card" data-category="{category.lower()}" data-search="{search}">
    <div class="project-top"><span class="project-label">{index + 1:02d} / {category}</span><span class="project-symbol" aria-hidden="true">{symbol}</span></div>
    <h4>{name}</h4>
    <p>{description}</p>
    <div class="project-attributes" aria-label="Project type, lifecycle, and topics"><span>{project_type}</span><span>{status}</span>{tags}</div>
    <div class="project-links"><a href="{url}">Visit site ↗</a><a href="{repo}">Source code ↗</a></div>
  </article>"""


def main():
    projects = [project for project in load_projects() if project["published"]]
    template = (PAGES / "index.html").read_text()
    for marker in ("<!-- LEAD_PROJECT_CARDS -->", "<!-- CONTRIBUTION_CARDS -->"):
        if template.count(marker) != 1:
            raise ValueError(f"Expected one {marker} placeholder")
    for role, marker in (("lead", "<!-- LEAD_PROJECT_CARDS -->"), ("contribution", "<!-- CONTRIBUTION_CARDS -->")):
        template = template.replace(marker, "".join(card(project, i) for i, project in enumerate(projects) if project["role"] == role))
    html = (template.replace("{{SITE_COUNT}}", str(len(projects)))
            .replace("{{LEAD_COUNT}}", str(sum(project["role"] == "lead" for project in projects)))
            .replace("{{CONTRIBUTION_COUNT}}", str(sum(project["role"] == "contribution" for project in projects))))
    if re.search(r"172\.16\.25\.|\.local\b|Plex administration|32400", html):
        raise ValueError("Private LAN detail in Pages output")
    shutil.rmtree(OUTPUT, ignore_errors=True)
    OUTPUT.mkdir()
    (OUTPUT / "index.html").write_text(html)
    (OUTPUT / ".nojekyll").write_text("")
    for name in ("home.css", "home.js"):
        shutil.copy2(PAGES / name, OUTPUT / name)
    shutil.copytree(PAGES / "theme", OUTPUT / "theme")
    print(f"Built {len(projects)} public project links in {OUTPUT}")


if __name__ == "__main__":
    main()
