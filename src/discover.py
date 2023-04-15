import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from .logging import logger


# https://www.bluetooth.com/specifications/assigned-numbers/
HEART_RATE_SERVICE_ASSIGNED_NUM = "0000180d"


async def main():
    logger.info("Start scanning for bluetooth devices")
    stop_event = asyncio.Event()

    found_devices = set()

    def filter_device(device: BLEDevice, advertising_data: AdvertisementData):
        matched_uuids = [
            uuid
            for uuid in advertising_data.service_uuids
            if uuid.startswith(HEART_RATE_SERVICE_ASSIGNED_NUM)
        ]
        if matched_uuids and device not in found_devices:
            found_devices.add(device)
            logger.info(f"{device.address} {device.name}")

    async with BleakScanner(filter_device):
        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
