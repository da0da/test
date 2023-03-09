from src.binance.kline import KLine


class KLines:
    _klines: list[KLine]

    def __init__(self) -> None:
        self._klines = []

    def __getitem__(self, key: int) -> KLine:
        return self._klines[key]

    def __setitem__(self, key: int, value: KLine) -> None:
        self._klines[key] = value

    def __delitem__(self, key: int) -> None:
        del self._klines[key]

    def add(self, kline: KLine) -> None:
        self._klines.append(kline)

    def remove_kline(self, position: int) -> None:
        del self._klines[position]
