import asyncio
import click
from bleak import BleakClient
from .util.constants import HEART_RATE__MEASUREMENT_ASSIGNED_NUM
from .util.hrv_data_aggregator import HRVDataAggregator
from .util.logging import logger


async def get_hr_measurement_characteristic(client: BleakClient):
    for characteristic in client.services.characteristics.values():
        if characteristic.uuid.startswith(HEART_RATE__MEASUREMENT_ASSIGNED_NUM):
            return characteristic
    raise Exception("Heart rate measurement characteristic not found")


async def connect(address: str, duration: int):
    logger.info(f"Start listening for bluetooth device at {address}")
    hrv_data_aggregator = HRVDataAggregator()
    async with BleakClient(address) as client:
        characteristic = await get_hr_measurement_characteristic(client)
        logger.info(characteristic)
        await client.start_notify(characteristic, hrv_data_aggregator.aggregate)
        await asyncio.sleep(duration)
        await client.stop_notify(characteristic)
    logger.info("Finished.")


@click.command()
@click.option(
    "--address",
    default="18:45:16:A0:46:36",
    help="Address of bluetooth device e.g 18:45:16:A0:46:36",
)
@click.option(
    "--duration",
    default=60,
    help="Listen to HR measurement data for a certain duration (sec)",
)
def main(address: str, duration: int):
    asyncio.run(connect(address, duration))


if __name__ == "__main__":
    main()
