import asyncio

from binance import BinanceSocketManager
from binance.enums import FuturesType

from settings.config import config
from src.binance.kline import KLine
from src.binance.pair import Pair


class PairUpdater:
    async def create_pair_socket(self, pair: Pair, bsm: BinanceSocketManager) -> None:
        ts = bsm._get_futures_socket(
            f"{pair.name.lower()}@kline_{config.INTERVAL}", futures_type=FuturesType.USD_M
        )
        async with ts as tscm:
            while True:
                res = (await tscm.recv()).get("data")
                if not res:
                    await asyncio.sleep(0)
                    continue

                pair.update_last_kline(KLine.from_socket(res["k"]))

                await asyncio.sleep(0)
