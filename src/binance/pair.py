from src.binance.kline import KLine
from src.binance.klines import KLines


class Pair:
    _name: str
    _base_asset: str
    _margin_asset: str
    _klines: KLines
    _last_signal_time: float
    _price_precision: float
    _quantity_precision: float
    _min_price: float
    _max_price: float

    def __init__(
        self,
        name: str,
        base_asset: str,
        margin_asset: str,
        price_precision: float,
        quantity_precision: float,
        min_price: float,
        max_price: float,
    ) -> None:
        self._name = name
        self._base_asset = base_asset
        self._margin_asset = margin_asset
        self._quantity_precision = quantity_precision
        self._min_price = min_price
        self._max_price = max_price
        self._price_precision = price_precision
        self._last_signal_time = 0
        self._klines = KLines()

    @property
    def price_precision(self) -> float:
        return self._price_precision

    @property
    def name(self) -> str:
        return self._name

    @property
    def get_klines(self) -> KLines:
        return self._klines

    @property
    def get_current_price(self) -> float:
        return self._klines[-1].close

    @property
    def last_signal_time(self) -> float:
        return self._last_signal_time

    def set_klines(self, klines: KLines) -> None:
        self._klines = klines

    def add_kline(self, kline: KLine) -> None:
        self._klines.add(kline)

    def update_last_signal_time(self, time: float) -> None:
        self._last_signal_time = time

    def update_last_kline(self, kline: KLine) -> None:
        if kline.start_time == self._klines[-1].start_time:
            self._klines[-1] = kline
        else:
            del self._klines[0]
            self._klines.add(kline)

    @classmethod
    def create_from_raw_data(cls, pair_name: str, data: dict):
        return cls(
            pair_name,
            data["baseAsset"],
            data["marginAsset"],
            data["pricePrecision"],
            data["quantityPrecision"],
            data["filters"][0]["minPrice"],
            data["filters"][0]["maxPrice"],
        )
