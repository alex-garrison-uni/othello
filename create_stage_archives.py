import zipfile
from pathlib import Path
import os

ARCHIVE_DIR = "stage_archives/"

BASE_ITEMS = [
    "LICENSE.md",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
    "src/othello/__init__.py",
    "src/othello/components.py",
    "src/othello/game_engine.py",
]

STAGE2_ITEMS = BASE_ITEMS + [
    "src/othello/flask_game_engine.py",
    "templates",
]

STAGE3_ITEMS = STAGE2_ITEMS + [
    "src/othello/ai.py",
    "images/diagrams",
    "images/screenshots",
    "README.md",
    "manual.md",
    "manual.docx",
    "tests",
    ".pre-commit-config.yaml",
    ".gitignore",
]

IGNORE = [
    "__pycache__"
]

STAGES = {
    "Stage1": BASE_ITEMS,
    "Stage2": STAGE2_ITEMS,
    "Stage3": STAGE3_ITEMS
}

def get_all_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if not any(ignore in filepath for ignore in IGNORE):
                file_paths.append(filepath)

    return file_paths

def add_path(zip_file, path):
    if Path(path).is_dir():
        for file in get_all_file_paths(path):
            zip_file.write(file)
    else:
        zip_file.write(path)


def make_stage_zip(stage, items):
    target = ARCHIVE_DIR + f"{stage}.zip"

    with zipfile.ZipFile(target, mode="w") as zip_file:
        for item in items:
            add_path(zip_file, item)

for stage, items in STAGES.items():
    make_stage_zip(stage, items)