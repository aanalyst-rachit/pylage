
import os
import subprocess

# Output filename
OUTPUT_FILE = "pylage_full_project_dump.md"

# Directories/files to ignore
IGNORE_DIRS = {".git", "__pycache__", "venv", ".pytest_cache", "build", "dist", ".egg-info"}

def collect_project_data():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# PyLage — Project Source Code & Test Logs\n\n")

        # 1. Run Tests & Capture Output Log
        out.write("## 1. Test Execution Logs\n\n")
        out.write("```text\n")
        try:
            # pytest run karke output capture karna (agar pytest installed hai)
            result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)
            out.write(result.stdout if result.stdout else result.stderr)
        except Exception:
            try:
                # Fallback to unittest
                result = subprocess.run(["python", "-m", "unittest", "discover"], capture_output=True, text=True)
                out.write(result.stdout if result.stdout else result.stderr)
            except Exception as e:
                out.write(f"Could not run tests automatically: {e}\n")
        out.write("\n```\n\n")

        # 2. Collect Source Code & Test Files
        out.write("## 2. Project Files & Codebase\n\n")
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if file.endswith(".py") and file != os.path.basename(__file__):
                    file_path = os.path.join(root, file)
                    out.write(f"### File: `{file_path}`\n\n")
                    out.write("```python\n")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"# Error reading file: {e}")
                    out.write("\n```\n\n")

    print(f"✅ Master file successfully generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    collect_project_data()