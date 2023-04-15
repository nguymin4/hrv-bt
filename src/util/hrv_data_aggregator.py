from dataclasses import dataclass
from datetime import timezone, datetime
from bleak.backends.characteristic import BleakGATTCharacteristic
from .logging import logger


# Specification: https://www.bluetooth.com/specifications/specs/heart-rate-service-1-0/

# IF RR-Interval presents, 4th bit of flag must be 1
HAS_RR_FLAG = 16


def parse_RR(raw: bytearray):
    """
    RR-Interval is represented by 2 bytes in little endian format
    """
    return int.from_bytes(raw, byteorder="little")


@dataclass
class HRVPacket:
    timestamp: int
    HR: int
    RRs: list[int]

    def __init__(self, raw_data: bytearray):
        self.timestamp = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        self.HR = int(raw_data[1])
        self.RRs = [parse_RR(raw_data[2:4])]
        if len(raw_data) > 4:
            self.RRs.append(parse_RR(raw_data[4:6]))


class HRVDataAggregator:
    def __init__(self):
        self.data: list[HRVPacket] = []

    def aggregate(self, characteristics: BleakGATTCharacteristic, raw_data: bytearray):
        flag = raw_data[0]
        if flag == 16:
            packet = HRVPacket(raw_data)
            logger.info(packet)
            self.data.append(packet)
