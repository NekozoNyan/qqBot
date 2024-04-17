import aiohttp
import asyncio

from .log import logger

class ServiceException(Exception):
    'Base of exceptions thrown by the service side'
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @property
    def message(self) -> str:
        return self.args[0]

async def fetch_text(uri: str) -> str:
    async with aiohttp.ClientSession(headers={ 'User-Agent': 'neko' }) as session:
        try:
            async with session.get(uri) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientResponseError as e:
            logger.exception(e)
            raise ServiceException('API 服务目前不可用')

