from pathlib import Path

_this_file = Path(__file__).resolve()

DIR_REPO = _this_file.parent.parent.resolve()

DIR_SRC = DIR_REPO / "src"
DIR_TEMPLATES = DIR_SRC / "templates"
DIR_SCRIPTS = DIR_REPO / "scripts"
DIR_LOCALIZATION = DIR_SRC / "localization"
FILE_VOCABULARIES = DIR_LOCALIZATION / "vocabularies.py"
