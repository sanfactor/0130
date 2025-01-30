import pytest
from unittest.mock import AsyncMock, patch
from peepseek.analysis import MemecoinAnalyzer

@pytest.fixture
def mock_jupiter_collector():
    with patch('peepseek.data_collectors.jupiter.JupiterCollector') as mock:
        instance = mock.return_value
        instance.get_token_info = AsyncMock(return_value={'price': 0.000001, 'market_cap': 100000})
        instance.get_price_history = AsyncMock(return_value=[
            {'timestamp': 1, 'price': 0.0000005},
            {'timestamp': 2, 'price': 0.000001}
        ])
        instance.get_liquidity_info = AsyncMock(return_value={'total_liquidity': 5000})
        yield instance

@pytest.fixture
def mock_metadrop_collector():
    with patch('peepseek.data_collectors.metadrop.MetadropCollector') as mock:
        instance = mock.return_value
        instance.get_token_info = AsyncMock(return_value={'price': 0.0000012, 'market_cap': 120000})
        instance.get_price_history = AsyncMock(return_value=[
            {'timestamp': 1, 'price': 0.0000006},
            {'timestamp': 2, 'price': 0.0000012}
        ])
        instance.get_liquidity_info = AsyncMock(return_value={'total_liquidity': 6000})
        yield instance

@pytest.fixture
def mock_pumpfun_collector():
    with patch('peepseek.data_collectors.pumpfun.PumpfunCollector') as mock:
        instance = mock.return_value
        instance.get_token_info = AsyncMock(return_value={'price': 0.0000011, 'market_cap': 110000})
        instance.get_price_history = AsyncMock(return_value=[
            {'timestamp': 1, 'price': 0.0000005},
            {'timestamp': 2, 'price': 0.0000011}
        ])
        instance.get_liquidity_info = AsyncMock(return_value={'total_liquidity': 5500})
        yield instance

@pytest.mark.asyncio
async def test_memecoin_analyzer(mock_jupiter_collector, mock_metadrop_collector, mock_pumpfun_collector):
    analyzer = MemecoinAnalyzer(
        jupiter_collector=mock_jupiter_collector,
        metadrop_collector=mock_metadrop_collector,
        pumpfun_collector=mock_pumpfun_collector
    )
    token_address = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    
    analysis, visualizations = await analyzer.analyze_token(token_address)
    
    assert isinstance(analysis, dict)
    assert isinstance(visualizations, dict)
    assert 'price_data' in analysis
    assert 'liquidity_data' in analysis
    assert 'risk_score' in analysis
    assert 'market_sentiment' in analysis
    assert 'recommendations' in analysis
    
    assert 'price_trends' in visualizations
    assert 'liquidity_comparison' in visualizations
    assert 'risk_assessment' in visualizations
    assert all(isinstance(v, bytes) for v in visualizations.values())
    
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
    assert len(analysis['recommendations']) >= 2
