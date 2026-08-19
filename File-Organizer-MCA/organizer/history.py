import json
from pathlib import Path

class HistoryManager:
    FILE_NAME = ".file_organizer_history.json"

    def __init__(self, directory):
        self.file = Path(directory) / self.FILE_NAME

    def save(self, operations):
        data = [{"source": str(op.source), "destination": str(op.destination)} for op in operations]
        self.file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self):
        if not self.file.exists():
            return []
        return json.loads(self.file.read_text(encoding="utf-8"))

    def clear(self):
        self.file.unlink(missing_ok=True)
