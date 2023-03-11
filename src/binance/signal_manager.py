import asyncio

from src.binance.binance_manager import BinanceManager


class SignalManager:
    _bm: BinanceManager

    def __init__(self, bm: BinanceManager) -> None:
        self._bm = bm

    @classmethod
    async def create(cls):
        bm = await BinanceManager.create()
        await bm.load_pairs_data()
        return cls(bm)

    async def watch_pairs(self) -> None:
        while True:
            pairs = self._bm.pairs

            btc = pairs.get_pair("BTCUSDT")
            eth = pairs.get_pair("ETHUSDT")

            last_kline_btc = btc.get_klines[-1]
            last_kline_eth = eth.get_klines[-1]

            up_btc_change = (last_kline_btc.high - last_kline_btc.open) / last_kline_btc.open
            down_btc_change = (last_kline_btc.low - last_kline_btc.open) / last_kline_btc.open
            up_eth_change = (last_kline_eth.high - last_kline_eth.open) / last_kline_eth.open
            down_eth_change = (last_kline_eth.low - last_kline_eth.open) / last_kline_eth.open

            if (up_eth_change - up_btc_change) * 100 > 1:
                print("ETHUSDT изменился более чем на 1%")
            if (down_eth_change - down_btc_change) * 100 < 1:
                print("ETHUSDT изменился более чем на -1%")

            await asyncio.sleep(0.1)
