import os
from pathlib import Path

# ==============================================================================
# 🎯 TARGET CONFIGURATION
# Specific folder ka dump banane ke liye yahan folder ka relative path likhein.
# Examples:
#   TARGET_FOLDER = "src"          # Sirf 'src' folder ka dump
#   TARGET_FOLDER = "src/components" # Subfolder ka dump
#   TARGET_FOLDER = "."            # Entire project ka dump (Default)
# ==============================================================================
TARGET_FOLDER = "pylage"

# Unwanted folders/files ko ignore karne ke liye list
IGNORE_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules", ".idea", ".vscode",
    "build", "dist", "text", "documentation", "test_output", "output",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache", ".eggs", ".tox",
    ".coverage", "htmlcov", "docs/_build", "site-packages"
}
IGNORE_FILES = {"dump.txt", "dump_selected.txt", "generate_dump.py", ".DS_Store"}

# Text/code extensions list
ALLOWED_EXTENSIONS = {".py", ".html", ".css", ".js", ".json"}

OUTPUT_FILE = "dump_selected.txt"

def build_tree(start_path: Path, prefix: str = "") -> list[str]:
    """Folder tree structure textual representation banata hai."""
    tree_lines = []
    try:
        entries = sorted(list(start_path.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return tree_lines

    # Filtering ignored items
    entries = [e for e in entries if e.name not in IGNORE_DIRS and e.name not in IGNORE_FILES]

    count = len(entries)
    for i, entry in enumerate(entries):
        is_last = (i == count - 1)
        connector = "└── " if is_last else "├── "
        tree_lines.append(f"{prefix}{connector}{entry.name}")

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            tree_lines.extend(build_tree(entry, prefix + extension))

    return tree_lines

def generate_dump():
    project_root = Path(".").resolve()
    target_path = (project_root / TARGET_FOLDER).resolve()

    # Safety check: Folder exist karta hai ya nahi
    if not target_path.exists() or not target_path.is_dir():
        print(f"❌ Error: Target folder '{TARGET_FOLDER}' nahi mila!")
        return

    print(f"Scanning target directory: {target_path}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # 1. Write Directory Tree
        out.write("=" * 80 + "\n")
        out.write(f"PROJECT DIRECTORY TREE ({target_path.name})\n")
        out.write("=" * 80 + "\n")
        out.write(f"{target_path.name}/\n")

        tree_lines = build_tree(target_path)
        out.write("\n".join(tree_lines))
        out.write("\n\n" + "=" * 80 + "\n")
        out.write("SOURCE CODE DUMP\n")
        out.write("=" * 80 + "\n\n")

        # 2. Iterate and Dump Target Folder Contents
        for current_root, dirs, files in os.walk(target_path):
            # Exclude ignored directories in-place
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file_name in sorted(files):
                if file_name in IGNORE_FILES:
                    continue

                file_path = Path(current_root) / file_name

                # Check extension
                if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
                    continue

                # Relative path hamesha main project root se dikhayega clarity ke liye
                relative_path = file_path.relative_to(project_root)

                out.write(f"\n{'=' * 80}\n")
                out.write(f"FILE: {relative_path}\n")
                out.write(f"{'=' * 80}\n\n")

                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        out.write(f.read())
                    out.write("\n")
                except Exception as e:
                    out.write(f"[ERROR READING FILE: {e}]\n")

    print(f"✅ Success! Dump file created: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_dump()
