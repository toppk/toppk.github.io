"""Load the generated public portfolio for the Pages build."""

import json
from pathlib import Path
import re
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "pages/projects.json"
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
STATUSES = {"incubating", "active", "maintenance", "dormant", "archived"}
TYPES = {"application", "service", "library", "documentation", "research"}
TAG = re.compile(r"^[a-z][a-z0-9-]*$")


def load_projects():
    with CATALOG.open(encoding="utf-8") as source:
        document = json.load(source)
    if document.get("schema") != 1:
        raise ValueError("Unsupported public catalog schema")
    projects = document["project"]
    seen = set()
    for project in projects:
        name = project["name"]
        if not NAME.fullmatch(name) or name in seen:
            raise ValueError(f"Invalid or duplicate project name: {name}")
        seen.add(name)
        for key in ("repo_description", "branding_description", "category", "symbol"):
            if not isinstance(project[key], str) or not project[key].strip():
                raise ValueError(f"{name}: {key} must be nonempty text")
        if project["role"] not in {"lead", "contribution"}:
            raise ValueError(f"{name}: invalid role")
        if type(project.get("published")) is not bool:
            raise ValueError(f"{name}: published must be true or false")
        if project.get("status") not in STATUSES:
            raise ValueError(f"{name}: invalid status")
        if project.get("type") not in TYPES:
            raise ValueError(f"{name}: invalid type")
        tags = project.get("tags")
        if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not TAG.fullmatch(tag) for tag in tags) or len(tags) != len(set(tags)):
            raise ValueError(f"{name}: tags must be unique lowercase slugs")
        if not isinstance(project["pages_enabled"], bool):
            raise ValueError(f"{name}: pages_enabled must be true or false")
        site_url = project.get("site_url")
        if project["published"] or site_url:
            if not isinstance(site_url, str):
                raise ValueError(f"{name}: published projects need site_url")
            parsed = urlparse(site_url)
            if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                raise ValueError(f"{name}: site_url must be a public HTTPS URL")
        if project["repo_description"].lstrip().casefold().startswith("private:"):
            raise ValueError(f"{name}: private description in public catalog")
    return projects
