import aiohttp
from typing import Dict, List
from .base import BaseCollector

class PumpfunCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.base_url = "https://pump.fun/api"
    
    async def get_token_info(self, token_address: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.base_url}/tokens/{token_address}")
            if response.status == 200:
                data = await response.json()
                return {
                    'name': data.get('name', ''),
                    'symbol': data.get('symbol', ''),
                    'price': data.get('price', 0),
                    'market_cap': data.get('market_cap', 0),
                    'replies': data.get('replies', 0)
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
                    'bonding_curve_price': data.get('bonding_curve_price', 0)
                }
            return {}
