import asyncio

from src.binance.signal_manager import SignalManager


async def main():
    signal_manager = await SignalManager.create()
    await signal_manager.watch_pairs()

asyncio.run(main())
