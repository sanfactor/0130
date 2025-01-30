from typing import Dict, List
import asyncio
from ..data_collectors import JupiterCollector, MetadropCollector, PumpfunCollector

class MemecoinAnalyzer:
    def __init__(self, jupiter_collector=None, metadrop_collector=None, pumpfun_collector=None):
        self.collectors = {
            'jupiter': jupiter_collector or JupiterCollector(),
            'metadrop': metadrop_collector or MetadropCollector(),
            'pumpfun': pumpfun_collector or PumpfunCollector()
        }
    
    async def analyze_token(self, token_address: str) -> Dict:
        tasks = []
        for name, collector in self.collectors.items():
            tasks.extend([
                asyncio.create_task(self._fetch_data(collector.get_token_info(token_address), f"{name}_token_info")),
                asyncio.create_task(self._fetch_data(collector.get_price_history(token_address), f"{name}_price_history")),
                asyncio.create_task(self._fetch_data(collector.get_liquidity_info(token_address), f"{name}_liquidity"))
            ])
        
        results = await asyncio.gather(*tasks)
        data = self._process_results(results)
        
        return {
            'price_data': self._analyze_price_data(data),
            'liquidity_data': self._analyze_liquidity_data(data),
            'risk_score': self._calculate_risk_score(data),
            'market_sentiment': self._calculate_market_sentiment(data),
            'recommendations': self._generate_recommendations(data)
        }
    
    async def _fetch_data(self, coro, name: str) -> Dict:
        try:
            result = await coro
            return {name: result}
        except Exception as e:
            return {name: None}
    
    def _process_results(self, results: List[Dict]) -> Dict:
        processed_data = {}
        for result in results:
            processed_data.update(result)
        return processed_data
    
    def _analyze_price_data(self, data: Dict) -> Dict:
        price_data = {}
        for source in self.collectors.keys():
            token_info = data.get(f"{source}_token_info", {})
            price_history = data.get(f"{source}_price_history", [])
            if token_info and price_history:
                price_data[source] = {
                    'current_price': token_info.get('price', 0),
                    'price_history': price_history
                }
        return price_data
    
    def _analyze_liquidity_data(self, data: Dict) -> Dict:
        liquidity_data = {}
        for source in self.collectors.keys():
            liquidity_info = data.get(f"{source}_liquidity", {})
            if liquidity_info:
                liquidity_data[source] = liquidity_info
        return liquidity_data
    
    def _calculate_risk_score(self, data: Dict) -> float:
        risk_score = 0.0
        factors = []
        
        for source in self.collectors.keys():
            liquidity = data.get(f"{source}_liquidity", {}).get('total_liquidity', 0)
            if liquidity < 1000:
                factors.append(0.8)
            elif liquidity < 10000:
                factors.append(0.5)
            else:
                factors.append(0.2)
        
        if factors:
            risk_score = sum(factors) / len(factors)
        
        return min(1.0, max(0.0, risk_score))
    
    def _calculate_market_sentiment(self, data: Dict) -> float:
        sentiment = 0.0
        weights = []
        
        for source in self.collectors.keys():
            price_history = data.get(f"{source}_price_history", [])
            if price_history:
                # Calculate price trend
                if len(price_history) >= 2:
                    start_price = price_history[0].get('price', 0)
                    end_price = price_history[-1].get('price', 0)
                    if start_price > 0:
                        change = (end_price - start_price) / start_price
                        weights.append(min(1.0, max(-1.0, change)))
        
        if weights:
            sentiment = sum(weights) / len(weights)
        
        return min(1.0, max(-1.0, sentiment))
    
    def _generate_recommendations(self, data: Dict) -> List[str]:
        recommendations = []
        risk_score = self._calculate_risk_score(data)
        sentiment = self._calculate_market_sentiment(data)
        
        if risk_score > 0.7:
            recommendations.append("High risk token - Exercise extreme caution")
        elif risk_score > 0.4:
            recommendations.append("Moderate risk token - Trade with caution")
        else:
            recommendations.append("Lower risk token relative to other memecoins")
        
        if sentiment > 0.5:
            recommendations.append("Strong positive market sentiment")
        elif sentiment > 0:
            recommendations.append("Slightly positive market sentiment")
        elif sentiment > -0.5:
            recommendations.append("Slightly negative market sentiment")
        else:
            recommendations.append("Strong negative market sentiment")
        
        return recommendations
