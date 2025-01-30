import pytest
from unittest.mock import AsyncMock, patch
from peepseek.data_collectors.pumpfun import PumpfunCollector

@pytest.mark.asyncio
async def test_pumpfun_collector():
    collector = PumpfunCollector()
    token_address = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock()
    
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_response)
    mock_session.__aenter__.return_value = mock_session
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        # Test get_token_info
        mock_response.json.return_value = {
            'name': 'Test Token',
            'symbol': 'TEST',
            'price': 0.000001,
            'market_cap': 100000,
            'replies': 42
        }
        token_info = await collector.get_token_info(token_address)
        assert isinstance(token_info, dict)
        assert 'name' in token_info
        assert 'price' in token_info
        
        # Test get_price_history
        mock_response.json.return_value = {
            'history': [
                {'timestamp': 1234567890, 'price': 0.000001},
                {'timestamp': 1234567891, 'price': 0.000002}
            ]
        }
        price_history = await collector.get_price_history(token_address)
        assert isinstance(price_history, list)
        assert len(price_history) == 2
        
        # Test get_liquidity_info
        mock_response.json.return_value = {
            'total_liquidity': 17000,
            'bonding_curve_price': 0.000001
        }
        liquidity_info = await collector.get_liquidity_info(token_address)
        assert isinstance(liquidity_info, dict)
        assert 'total_liquidity' in liquidity_info
        assert 'bonding_curve_price' in liquidity_info
