from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class FileOperation:
    source: Path
    destination: Path

@dataclass
class OrganizationResult:
    operations: list
    moved: int = 0
    skipped: int = 0
    failed: int = 0
    messages: list = None

    def __post_init__(self):
        if self.messages is None:
            self.messages = []
