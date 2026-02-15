import subprocess
from pathlib import Path
import os

SOURCE_DIR = Path.cwd()
OUTPUT_DIR = SOURCE_DIR / "pdfs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Change this if Chrome is installed elsewhere
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

notebooks = list(SOURCE_DIR.glob("*.ipynb"))

for notebook in notebooks:
    print(f"Processing: {notebook.name}")

    # Step 1: Convert to HTML (with execution to preserve outputs)
    subprocess.run([
        "jupyter", "nbconvert",
        "--to", "html",
        "--execute",
        "--ExecutePreprocessor.timeout=600",
        str(notebook),
        "--output-dir", str(OUTPUT_DIR)
    ])

    html_file = OUTPUT_DIR / notebook.with_suffix(".html").name
    pdf_file = OUTPUT_DIR / notebook.with_suffix(".pdf").name

    # Step 2: Convert HTML to PDF using Chrome headless
    subprocess.run([
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_file}",
        str(html_file)
    ])

    # Remove temporary HTML file
    os.remove(html_file)

print("\n✅ All notebooks converted to PDF successfully with outputs!")
