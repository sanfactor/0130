import pytest
from unittest.mock import AsyncMock, patch
from peepseek.analysis import MemecoinAnalyzer

@pytest.mark.asyncio
async def test_memecoin_analyzer():
    analyzer = MemecoinAnalyzer()
    token_address = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock()
    
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_response)
    mock_session.__aenter__.return_value = mock_session
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        # Mock Jupiter data
        mock_response.json.side_effect = [
            {'price': 0.000001, 'market_cap': 100000},  # token info
            [{'timestamp': 1, 'price': 0.0000005}, {'timestamp': 2, 'price': 0.000001}],  # price history
            {'total_liquidity': 5000},  # liquidity info
            # Metadrop data
            {'price': 0.0000012, 'market_cap': 120000},
            [{'timestamp': 1, 'price': 0.0000006}, {'timestamp': 2, 'price': 0.0000012}],
            {'total_liquidity': 6000},
            # Pumpfun data
            {'price': 0.0000011, 'market_cap': 110000},
            [{'timestamp': 1, 'price': 0.0000005}, {'timestamp': 2, 'price': 0.0000011}],
            {'total_liquidity': 5500}
        ]
        
        analysis = await analyzer.analyze_token(token_address)
        
        assert isinstance(analysis, dict)
        assert 'price_data' in analysis
        assert 'liquidity_data' in analysis
        assert 'risk_score' in analysis
        assert 'market_sentiment' in analysis
        assert 'recommendations' in analysis
        
        # Verify price data structure
        assert all(source in analysis['price_data'] for source in ['jupiter', 'metadrop', 'pumpfun'])
        for source_data in analysis['price_data'].values():
            assert 'current_price' in source_data
            assert 'price_history' in source_data
        
        # Verify liquidity data structure
        assert all(source in analysis['liquidity_data'] for source in ['jupiter', 'metadrop', 'pumpfun'])
        
        # Verify risk score and sentiment ranges
        assert 0 <= analysis['risk_score'] <= 1
        assert -1 <= analysis['market_sentiment'] <= 1
        
        # Verify recommendations
        assert isinstance(analysis['recommendations'], list)
        assert len(analysis['recommendations']) >= 2  # At least risk and sentiment recommendations
