import shutil
from .categories import FILE_CATEGORIES
from .history import HistoryManager
from .models import FileOperation, OrganizationResult
from .scanner import FileScanner

class FileOrganizer:
    def __init__(self):
        self.managed_folders = set(FILE_CATEGORIES) | {"Others"}
        self.scanner = FileScanner(self.managed_folders)
        self.last_directory = None

    @staticmethod
    def unique_destination(destination):
        if not destination.exists():
            return destination
        counter = 1
        while True:
            candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def create_plan(self, directory, recursive=False):
        operations, skipped = [], 0
        for source, category in self.scanner.scan(directory, recursive):
            target_folder = directory / category
            if source.parent.resolve() == target_folder.resolve():
                skipped += 1
                continue
            destination = self.unique_destination(target_folder / source.name)
            operations.append(FileOperation(source, destination))
        return OrganizationResult(operations=operations, skipped=skipped)

    def preview(self, directory, recursive=False):
        return self.create_plan(directory, recursive)

    def organize(self, directory, recursive=False):
        result = self.create_plan(directory, recursive)
        successful = []
        for operation in result.operations:
            try:
                operation.destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(operation.source), str(operation.destination))
                successful.append(operation)
                result.moved += 1
                result.messages.append(f"[MOVED] {operation.source.name} -> {operation.destination.parent.name}/{operation.destination.name}")
            except Exception as exc:
                result.failed += 1
                result.messages.append(f"[FAILED] {operation.source.name}: {exc}")
        if successful:
            HistoryManager(directory).save(successful)
        self.last_directory = directory
        return result

    def undo_last(self):
        if not self.last_directory:
            raise RuntimeError("No previous organization operation is available.")
        history = HistoryManager(self.last_directory)
        records = history.load()
        if not records:
            raise RuntimeError("No organization history was found.")
        restored = 0
        for record in reversed(records):
            source = __import__("pathlib").Path(record["source"])
            destination = __import__("pathlib").Path(record["destination"])
            if not destination.exists():
                continue
            source.parent.mkdir(parents=True, exist_ok=True)
            restore_target = self.unique_destination(source)
            shutil.move(str(destination), str(restore_target))
            restored += 1
        history.clear()
        return restored
