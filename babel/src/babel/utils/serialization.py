import hashlib
import json
from typing import Any


def stable_hash(obj: Any) -> str:
    """Return stable SHA-256 hash of JSON-serializable object."""
    serialized = json.dumps(obj, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
