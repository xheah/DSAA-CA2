from pathlib import Path


class FileHandler:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self._file_index = None

    def _build_file_index(self):
        data_dir = self.project_root / "data"
        index = {}
        if data_dir.exists():
            for path in data_dir.rglob("*.txt"):
                index.setdefault(path.name, []).append(path)
        self._file_index = index

    def _find_matches(self, filename: str):
        if self._file_index is None:
            self._build_file_index()
        matches = self._file_index.get(filename, [])
        if matches:
            return matches
        # Fallback to full project search only if not found in data/
        return list(self.project_root.rglob(filename))

    def read_file(self):
        while True:
            filename = input("Please enter input file: ").strip()
            if not filename:
                print("Please enter a file name.")
                continue
            if not filename.endswith('.txt'):
                print("Please enter a valid txt file.")
                continue
            matches = self._find_matches(filename)
            if not matches:
                print(f"File not found: {filename}")
                continue
            if len(matches) > 1:
                # Prefer deterministic behavior if multiple matches exist
                matches.sort()
            return matches[0].read_text(encoding="utf-8")
        
    def write_file(self,content):
        while True:
            filename = input('\nPlease enter ouptut file: ').strip()
            if not filename:
                print('\nPlease enter a file name.')
                continue
            if not filename.endswith('.txt'):
                print('\nPlease enter a valid .txt file')
                continue
            if any(char in filename for char in ['<', '>', ':', '"', '|', '?', '*']):
                print("\nInvalid characters in filename.")
                continue
            file_path = self.project_root / 'data' /filename
            file_path.write_text(content, encoding="utf-8")
            return