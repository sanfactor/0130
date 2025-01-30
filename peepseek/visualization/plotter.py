import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List
import io

class MemecoinPlotter:
    def __init__(self):
        plt.style.use('default')
    
    def plot_price_trends(self, price_data: Dict) -> bytes:
        plt.figure(figsize=(12, 6))
        
        for source, data in price_data.items():
            if data and data.get('price_history'):
                df = pd.DataFrame(data['price_history'])
                plt.plot(df['timestamp'], df['price'], label=source.capitalize())
        
        plt.title('Price Trends Across Data Sources')
        plt.xlabel('Timestamp')
        plt.ylabel('Price (USDC)')
        plt.legend()
        plt.grid(True)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        return buf.getvalue()
    
    def plot_liquidity_comparison(self, liquidity_data: Dict) -> bytes:
        plt.figure(figsize=(10, 6))
        
        sources = list(liquidity_data.keys())
        liquidity_values = [data.get('total_liquidity', 0) for data in liquidity_data.values()]
        
        plt.bar(sources, liquidity_values)
        plt.title('Liquidity Comparison Across Sources')
        plt.xlabel('Data Source')
        plt.ylabel('Total Liquidity (USDC)')
        plt.xticks(rotation=45)
        plt.grid(True, axis='y')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        return buf.getvalue()
    
    def plot_risk_assessment(self, risk_score: float, market_sentiment: float) -> bytes:
        plt.figure(figsize=(12, 6))
        
        # Create a 2-panel plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Risk Score gauge
        risk_colors = ['green', 'yellow', 'red']
        risk_bounds = [0, 0.4, 0.7, 1]
        ax1.set_title('Risk Assessment')
        ax1.barh(['Risk Score'], [risk_score], color='blue')
        ax1.set_xlim(0, 1)
        ax1.axvline(x=0.4, color='yellow', linestyle='--', alpha=0.5)
        ax1.axvline(x=0.7, color='red', linestyle='--', alpha=0.5)
        
        # Market Sentiment gauge
        sentiment_colors = ['red', 'yellow', 'green']
        sentiment_bounds = [-1, -0.5, 0.5, 1]
        ax2.set_title('Market Sentiment')
        ax2.barh(['Sentiment'], [market_sentiment], color='blue')
        ax2.set_xlim(-1, 1)
        ax2.axvline(x=-0.5, color='yellow', linestyle='--', alpha=0.5)
        ax2.axvline(x=0.5, color='yellow', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        return buf.getvalue()
