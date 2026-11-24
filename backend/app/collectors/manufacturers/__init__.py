from app.collectors.manufacturers.goodsmile import GoodSmileAdapter
from app.collectors.manufacturers import (
    furyu,
    bandai,
    megahouse,
    sega,
    kotobukiya,
    taito,
    hottoys,
)

ADAPTERS = [
    GoodSmileAdapter(),
    *[
        m.Adapter()
        for m in (furyu, bandai, megahouse, sega, kotobukiya, taito, hottoys)
    ],
]
