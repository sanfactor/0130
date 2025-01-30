# PeepSeek

Solana memecoin analysis agent using DeepSeek's foundational logic.

## Features
- Real-time memecoin data collection from Jupiter, Metadrop, and Pumpfun
- Price analysis and pattern recognition
- Market sentiment analysis
- Risk assessment

## Installation
```bash
poetry install
```

## Usage
```python
from peepseek import MemecoinAnalyzer

analyzer = MemecoinAnalyzer()
analysis = analyzer.analyze_token("TOKEN_ADDRESS")
print(analysis)
```
