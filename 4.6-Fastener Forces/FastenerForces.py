
import sys
from pathlib import Path

spacing_folder = Path(__file__).resolve().parent.parent / "4.4-Fastener Spacing"
sys.path.append(str(spacing_folder))
from FastenerPattern import Spacing

Spacing(1, 2, 4)
