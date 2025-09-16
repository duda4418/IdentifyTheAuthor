import json
from pathlib import Path

# Root directory (current working dir where script is located)
ROOT = Path(__file__).resolve().parent

# Notebook files to process
notebooks = list(ROOT.glob('*.ipynb'))

INTRO_CELL_SOURCE = [
    "# === Standardized path configuration added automatically ===\n",
    "from pathlib import Path\n",
    "BASE_DIR = Path.cwd()  # project root when running the notebook\n",
    "DATA_DIR = BASE_DIR / 'data'\n",
    "TRAIN_CSV = DATA_DIR / 'train' / 'train.csv'\n",
    "TEST_CSV = DATA_DIR / 'test' / 'test.csv'\n",
    "# You can now use TRAIN_CSV and TEST_CSV instead of hardcoded strings.\n"
]

# Replacement patterns (string based)
REPLACEMENTS = {
    "/kaggle/input/identify-the-author/train/train.csv": "str(TRAIN_CSV)",
    "/kaggle/input/identify-the-author/test/test.csv": "str(TEST_CSV)",
    "data/train/train.csv": "str(TRAIN_CSV)",
    "data/test/test.csv": "str(TEST_CSV)",
}

# Additional mapping for variables assignment lines
LINE_NORMALIZERS = [
    ("train_path =", "train_path = str(TRAIN_CSV)"),
    ("test_path", "test_path  = str(TEST_CSV)"),
    ("TRAIN_PATH =", "TRAIN_PATH = str(TRAIN_CSV)"),
    ("TEST_PATH =", "TEST_PATH  = str(TEST_CSV)"),
    ("TEST_CSV = '/kaggle/input/identify-the-author/test/test.csv'", "TEST_CSV = str(TEST_CSV)  # standardized"),
]

INTRO_MARKER = "# === Standardized path configuration added automatically ==="

modified_files = []

for nb_path in notebooks:
    try:
        with nb_path.open('r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Skipping {nb_path.name}: unable to parse ({e})")
        continue

    changed = False

    # Ensure first cell has the intro config
    has_intro = any(
        cell.get('cell_type') == 'code' and cell.get('source') and any(INTRO_MARKER in line for line in cell['source'])
        for cell in nb.get('cells', [])
    )

    if not has_intro:
        intro_cell = {
            "cell_type": "code",
            "metadata": {},
            "source": INTRO_CELL_SOURCE,
            "execution_count": None,
            "outputs": []
        }
        nb['cells'].insert(0, intro_cell)
        changed = True

    # Walk through code cells and apply replacements
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        src = cell.get('source', [])
        new_src = []
        cell_changed = False
        for line in src:
            new_line = line
            # Simple string replacements
            for old, new in REPLACEMENTS.items():
                if old in new_line:
                    new_line = new_line.replace(old, new)
            # Normalize assignment lines
            for needle, replacement in LINE_NORMALIZERS:
                if needle in new_line:
                    new_line = replacement + ("\n" if not new_line.endswith("\n") else "")
            if new_line != line:
                cell_changed = True
            new_src.append(new_line)
        if cell_changed:
            cell['source'] = new_src
            changed = True

    if changed:
        with nb_path.open('w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=2)
        modified_files.append(nb_path.name)
        print(f"Updated: {nb_path.name}")
    else:
        print(f"No changes needed: {nb_path.name}")

print("\nSummary:")
if modified_files:
    print("Modified notebooks:")
    for name in modified_files:
        print(" -", name)
else:
    print("No notebooks modified.")

