from .categories import get_category

class FileScanner:
    def __init__(self, managed_folders):
        self.managed_folders = set(managed_folders)

    def scan(self, directory, recursive=False):
        iterator = directory.rglob("*") if recursive else directory.iterdir()
        for path in iterator:
            if not path.is_file():
                continue
            if any(parent.name in self.managed_folders for parent in path.parents):
                continue
            yield path, get_category(path)
