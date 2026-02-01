from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import json


DEFAULT_RULES: Dict[str, List[str]] = {
    "Images": [".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".svg", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".json", ".yml", ".yaml", ".md", ".sql"],
    "Executables": [".exe", ".msi", ".bat", ".cmd", ".ps1", ".apk", ".dmg"],
}


@dataclass(frozen=True)
class Rules:
    mapping: Dict[str, List[str]]

    def folder_for_extension(self, ext: str) -> str:
        ext = ext.lower()
        for folder, exts in self.mapping.items():
            if ext in (e.lower() for e in exts):
                return folder
        return "Other"

    @staticmethod
    def load(path: Optional[Path]) -> "Rules":
        if path is None:
            return Rules(DEFAULT_RULES)
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("rules JSON must be an object {folder: [ext, ...], ...}")
        normalized: Dict[str, List[str]] = {}
        for folder, exts in data.items():
            if not isinstance(folder, str) or not isinstance(exts, list):
                raise ValueError("rules JSON must be {str: list[str]}")
            normalized[folder] = [str(x).lower() if str(x).startswith(".") else f".{str(x).lower()}" for x in exts]
        return Rules(normalized)
