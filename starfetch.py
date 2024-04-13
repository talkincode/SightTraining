import asyncio


async def main():
    from starfetch.game import AsyncStarFetch

    await AsyncStarFetch().start_game()


if __name__ == "__main__":
    asyncio.run(main())
