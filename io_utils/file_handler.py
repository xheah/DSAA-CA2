from pathlib import Path


class FileHandler:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]

    def read_file(self):
        while True:
            filename = input("Please enter input file: ").strip()
            if not filename:
                print("Please enter a file name.")
                continue
            if not filename.endswith('.txt'):
                print("Please enter a valid txt file.")
                continue
            matches = list(self.project_root.rglob(filename))
            if not matches:
                print(f"File not found: {filename}")
                continue
            if len(matches) > 1:
                # Prefer deterministic behavior if multiple matches exist
                matches.sort()
            return matches[0].read_text(encoding="utf-8")