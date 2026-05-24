import hashlib
import struct


def deterministic_uint64(seed: str, namespace: str, position: int) -> int:
    """
    Return deterministic uint64 derived from seed + namespace + position.
    Uses SHA-256. Does NOT use Python built-in hash().
    """
    key = f"{seed}|{namespace}|{position}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    value = struct.unpack_from(">Q", digest, 0)[0]
    return value


def deterministic_index(seed: str, namespace: str, position: int, modulo: int) -> int:
    """Return deterministic index in [0, modulo)."""
    return deterministic_uint64(seed, namespace, position) % modulo
