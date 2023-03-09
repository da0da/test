from dataclasses import dataclass


@dataclass
class KLine:
    start_time: float
    open: float
    high: float
    low: float
    close: float
    close_time: float

    @classmethod
    def from_request(cls, data: list):
        return cls(
            float(data[0]),
            float(data[1]),
            float(data[2]),
            float(data[3]),
            float(data[4]),
            float(data[6]),
        )

    @classmethod
    def from_socket(cls, data: dict):
        return cls(
            float(data["t"]),
            float(data["o"]),
            float(data["h"]),
            float(data["l"]),
            float(data["c"]),
            float(data["T"]),
        )
