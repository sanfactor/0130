from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BaseCollector(ABC):
    def __init__(self):
        self.base_url: str = ""
        
    @abstractmethod
    async def get_token_info(self, token_address: str) -> Dict:
        pass
    
    @abstractmethod
    async def get_price_history(self, token_address: str) -> List[Dict]:
        pass
    
    @abstractmethod
    async def get_liquidity_info(self, token_address: str) -> Dict:
        pass
