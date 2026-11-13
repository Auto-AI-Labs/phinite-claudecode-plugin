"""Copy the playbook (the source of truth for docs, templates and tool helpers) into the plugin before a release.

  python3 scripts/sync_playbook.py [--playbook ../phinite-playbook]

Installed plugins can't read files outside their own folder, so the plugin ships copies:
  playbook/*.md                 -> skills/<skill>/references/
  playbook/templates/project/       -> templates/project/        (use case with a Postgres schema)
  playbook/templates/project_nodb/  -> templates/project_nodb/   (use case without a database)
  playbook/kit/tool_common*.py      -> templates/                (helpers bundled into every tool)
"""
import argparse
import pathlib
import shutil

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
REFERENCES = {
    "phinite-design": ["02_GRAPH_DESIGN.md", "03_PROJECT_AND_TOOLS.md", "07_MULTIAGENT_AND_MULTIMODAL.md"],
    "phinite-ship": ["05_BUILD_CHECKLIST.md"],
    "phinite-debug": ["04_TESTING_AND_DEBUGGING.md", "06_LESSONS_LEARNED.md"],
    "phinite-api": ["01_PHINITE_API.md"],  # not 00_AUTH_SETUP.md: copied-cookie sign-in, the plugin uses OAuth
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--playbook", default=str(PLUGIN.parent / "phinite-playbook"))
    playbook = pathlib.Path(parser.parse_args().playbook).resolve()
    for skill, docs in REFERENCES.items():
        target = PLUGIN / "skills" / skill / "references"
        target.mkdir(parents=True, exist_ok=True)
        for doc in docs:
            shutil.copy(playbook / doc, target / doc)
            print("doc     ", f"{skill}/references/{doc}")
    templates = PLUGIN / "templates"
    for name in ("project", "project_nodb"):
        shutil.rmtree(templates / name, ignore_errors=True)
        shutil.copytree(playbook / "templates" / name, templates / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "deploy-out", "phinite_ids.json", "tools"))
        print("template", f"templates/{name}/")
    for helper in ("tool_common.py", "tool_common_nodb.py"):
        shutil.copy(playbook / "kit" / helper, templates / helper)
        print("helpers ", f"templates/{helper}")


if __name__ == "__main__":
    main()
