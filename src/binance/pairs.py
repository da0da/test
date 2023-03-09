from typing import Union

from src.binance.pair import Pair


class Pairs:
    _pairs: list[Pair]

    def __init__(self):
        self._pairs = []

    def count(self) -> int:
        return len(self._pairs)

    def add_pair(self, pair: Pair) -> None:
        self._pairs.append(pair)

    def get_pair(self, pair_name: str) -> Union[Pair, bool]:
        for pair in self._pairs:
            if pair.name == pair_name:
                return pair

        return False

    def __getitem__(self, key: int) -> Pair:
        return self._pairs[key]
