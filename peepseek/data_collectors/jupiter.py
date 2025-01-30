from typing import Dict, List
from .base import BaseCollector

class JupiterCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.base_url = "https://price.jup.ag/v4"
    
    async def get_token_info(self, token_address: str) -> Dict:
        return {}
    
    async def get_price_history(self, token_address: str) -> List[Dict]:
        return []
    
    async def get_liquidity_info(self, token_address: str) -> Dict:
        return {}
