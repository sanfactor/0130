import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
from peepseek.data_collectors.jupiter import JupiterCollector

@pytest.mark.asyncio
async def test_jupiter_collector():
    collector = JupiterCollector()
    token_address = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock()
    
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_response)
    mock_session.__aenter__.return_value = mock_session
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        mock_response.json.return_value = {"data": {token_address: {"price": "0.000001"}}}
        token_info = await collector.get_token_info(token_address)
        assert isinstance(token_info, dict)
        
        mock_response.json.return_value = {"data": {token_address: [{"price": "0.000001"}]}}
        price_history = await collector.get_price_history(token_address)
        assert isinstance(price_history, list)
        
        mock_response.json.return_value = {"data": {token_address: {"liquidity": "1000"}}}
        liquidity_info = await collector.get_liquidity_info(token_address)
        assert isinstance(liquidity_info, dict)
