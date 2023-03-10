import asyncio
from asyncio import tasks

from binance import AsyncClient, BinanceSocketManager

from settings.config import config
from src.binance.kline import KLine
from src.binance.pair import Pair
from src.binance.pair_updater import PairUpdater
from src.binance.pairs import Pairs


class BinanceManager:
    _client: AsyncClient
    _binance_socket_manager: BinanceSocketManager
    _pairs: Pairs
    _semaphore: asyncio.Semaphore

    def __init__(self, client: AsyncClient) -> None:
        self._client = client
        self._binance_socket_manager = BinanceSocketManager(client)
        self._pairs = Pairs()
        self._semaphore = asyncio.Semaphore(5)

    @property
    def bsm(self) -> BinanceSocketManager:
        return self._binance_socket_manager

    @property
    def pairs(self):
        return self._pairs

    @classmethod
    async def create(cls):
        client: AsyncClient = await AsyncClient.create()
        return BinanceManager(client)

    async def _load_klines(self, pair: Pair) -> None:
        async with self._semaphore:
            klines_raw = await self._client.futures_klines(symbol=pair.name, interval=config.INTERVAL, limit=config.LIMIT)
            for kline_raw in klines_raw:
                kline = KLine.from_request(kline_raw)
                pair.add_kline(kline)
            tasks.create_task(PairUpdater().create_pair_socket(pair, self._binance_socket_manager))

    async def load_pairs_data(self) -> None:
        exchange_info = (await self._client.futures_exchange_info()).get("symbols")

        tasks_list = []
        for pair_data in exchange_info:
            pair_name = pair_data["symbol"]
            if pair_name not in ["BTCUSDT", "ETHUSDT"]:
                continue
            pair = Pair.create_from_raw_data(pair_name, pair_data)
            tasks_list.append(self._load_klines(pair))
            self._pairs.add_pair(pair)
        await asyncio.gather(*tasks_list)
