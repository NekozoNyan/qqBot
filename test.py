import aiohttp
import asyncio

async def fetch_text(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    city = 'your_city_name'
    weather_data = await fetch_text(f'https://wttr.in/{city}?format=1')
    print(weather_data)

asyncio.run(main())
