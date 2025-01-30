import aiohttp
from typing import Dict, List
from .base import BaseCollector

class MetadropCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.base_url = "https://metadrop.com/api"
    
    async def get_token_info(self, token_address: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/tokens/{token_address}")
            if response.status == 200:
                data = await response.json()
                return {
                    'price': data.get('price', 0),
                    'market_cap': data.get('market_cap', 0),
                    'volume': data.get('volume', 0),
                    'liquidity': data.get('liquidity', 0)
                }
            return {}
    
    async def get_price_history(self, token_address: str) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/tokens/{token_address}/history")
            if response.status == 200:
                data = await response.json()
                return data.get('history', [])
            return []
    
    async def get_liquidity_info(self, token_address: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/tokens/{token_address}/liquidity")
            if response.status == 200:
                data = await response.json()
                return {
                    'total_liquidity': data.get('total_liquidity', 0),
                    'buys_24h': data.get('buys_24h', 0),
                    'sells_24h': data.get('sells_24h', 0)
                }
            return {}
