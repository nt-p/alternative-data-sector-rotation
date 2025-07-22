import subprocess
import sys
from tabnanny import check

scripts = [
    "src/data_collection.py",
    "src/price_data.py",
    "src/preprocessing.py",
    "src/strategy.py",
    "src/analysis.py"
]

if __name__ == "__main__":
    for script in scripts:
        print(f"Running {script}...")
        result = subprocess.run([sys.executable, script], capture_output=True, check=True)
        