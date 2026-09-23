from dataclasses import dataclass


@dataclass
class Stats:
    served_local: int = 0
    served_from_catalog: int = 0

    catalog_reads: int = 0

    evictions: int = 0

    local: int = 0
    bytes: int = 0

    catalog: int = 0