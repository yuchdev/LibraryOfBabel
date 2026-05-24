from pydantic import BaseModel, Field

from babel.constants import (
    BORGES_LOG10_SIZE,
    OBSERVABLE_UNIVERSE_PLANCK_VOLUMES_LOG10,
    UNIVERSE_ATOMS_LOG10,
)
from babel.mathlib.logmath import log10_ratio, scientific_from_log10


class LibraryMetrics(BaseModel):
    mode_id: str
    log10_size: float
    mantissa: float
    exponent: int
    log10_smaller_than_borges: float
    log10_larger_than_universe_atoms: float
    log10_larger_than_planck_volumes: float
    notes: list[str] = Field(default_factory=list)


def calculate_metrics(mode_id: str, log10_size: float) -> LibraryMetrics:
    """
    Calculate scientific notation, comparisons with Borges and universe constants.
    """
    mantissa, exponent = scientific_from_log10(log10_size)
    log10_smaller_than_borges = log10_ratio(BORGES_LOG10_SIZE, log10_size)
    log10_larger_than_universe_atoms = log10_ratio(log10_size, UNIVERSE_ATOMS_LOG10)
    log10_larger_than_planck_volumes = log10_ratio(
        log10_size, OBSERVABLE_UNIVERSE_PLANCK_VOLUMES_LOG10
    )
    return LibraryMetrics(
        mode_id=mode_id,
        log10_size=log10_size,
        mantissa=mantissa,
        exponent=exponent,
        log10_smaller_than_borges=log10_smaller_than_borges,
        log10_larger_than_universe_atoms=log10_larger_than_universe_atoms,
        log10_larger_than_planck_volumes=log10_larger_than_planck_volumes,
    )
