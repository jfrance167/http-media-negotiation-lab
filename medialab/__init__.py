"""Public bounded teaching interface: parse UTF8 JSON bytes, evaluate native metadata."""

from .contracts import Invalid, parse
from .model import evaluate

__all__ = ["Invalid", "parse", "evaluate"]
