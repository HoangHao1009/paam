import asyncio
import aiohttp

from typing import Union

async def fetch(session: aiohttp.ClientSession, url: str, headers: dict):
    try:
        async with session.get(url, headers=headers) as response:
            return await response.json()
    except aiohttp.ClientError as e:
        raise aiohttp.ClientError(f'ClientError in url: {url} -> {e}')
    except Exception as e:
        raise Exception(f'Unexpected error fetching {url}: {e}')
    
async def fetch_all(urls: list, headers: dict):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, headers) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
    
async def _fetch_by_urls(survey_url: Union[list, str], headers: dict):
    if isinstance(survey_url, str):
        survey_url = [survey_url]
    data = await fetch_all(survey_url, headers)
    return data
