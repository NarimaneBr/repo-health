from abc import ABC, abstractmethod
from pathlib import Path
from ..models import AnalysisResult
from ..config import Settings

class BaseAnalyzer(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, root_path: Path, files: list[Path], settings: Settings) -> AnalysisResult:
        pass
