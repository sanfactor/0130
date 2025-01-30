import aiohttp
from typing import Dict, List
from .base import BaseCollector

class JupiterCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.base_url = "https://jup.ag/api/v4"
    
    async def get_token_info(self, token_address: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/price?ids={token_address}&vsToken=USDC")
            if response.status == 200:
                data = await response.json()
                return data.get('data', {}).get(token_address, {})
            return {}
    
    async def get_price_history(self, token_address: str) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/price/history?ids={token_address}&vsToken=USDC")
            if response.status == 200:
                data = await response.json()
                return data.get('data', {}).get(token_address, [])
            return []
    
    async def get_liquidity_info(self, token_address: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/market-depth?ids={token_address}&vsToken=USDC")
            if response.status == 200:
                data = await response.json()
                return data.get('data', {}).get(token_address, {})
            return {}
