# THOROUGHBRED EDGE PRO

A high-performance horse racing game theory model based on the three-model convergence framework.

## Overview

THOROUGHBRED EDGE PRO uses advanced game theory and statistical analysis to identify mispriced horses in parimutuel betting pools, with a particular emphasis on undervalued underdogs.

### Three-Model Convergence Framework

1. **Speed Model** - Analyzes raw velocity, track-adjusted speed ratings, and performance metrics
2. **Pace Model** - Evaluates early, middle, and late pace scenarios with energy distribution
3. **Form Model** - Assesses class levels, recent performance, trainer/jockey statistics, and connections

### Game Theory Engine

- Identifies inefficiencies in parimutuel pools
- Calculates expected value vs. actual odds
- Finds overlay opportunities (especially in underdogs)
- Simulates crowd psychology and betting patterns
- Analyzes Kelly Criterion optimal bet sizing

## Key Features

- **Underdog Emphasis**: Specialized algorithms to find mispriced longshots
- **Value Detection**: Game theory-based pool analysis
- **Multi-Factor Analysis**: Speed, pace, and form convergence scoring
- **Track Adjustments**: Surface, distance, and condition normalization
- **Odds Overlay Detection**: Identifies when true probability exceeds implied probability

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from thoroughbred_edge_pro import ThoroughbredEdgePro

# Initialize the system
edge_pro = ThoroughbredEdgePro()

# Analyze a race
analysis = edge_pro.analyze_race(race_data)

# Get value bets (emphasizing underdogs)
value_bets = edge_pro.find_value_bets(analysis, min_overlay=1.15)

# Display results
edge_pro.display_analysis(value_bets)
```

## Model Components

### Speed Model
- Beyer-style speed figures
- Track variant calculations
- Class par adjustments
- Velocity ratings normalized across surfaces

### Pace Model
- Fractional time analysis
- Energy distribution modeling
- Pace pressure scenarios
- Late pace advantage calculations

### Form Model
- Recent race performance (weighted by recency)
- Class level transitions
- Trainer/jockey win percentages
- Days since last race optimization
- Equipment changes impact

### Game Theory Engine
- Parimutuel pool inefficiency detection
- Crowd bias identification
- True probability estimation
- Expected value calculations
- Underdog overlay specialization

## Philosophy

The system is built on the principle that parimutuel pools often misprice horses due to:
1. Public bias toward favorites
2. Undervaluation of complex pace scenarios
3. Misunderstanding of form cycles
4. Recency bias in speed ratings

By combining three independent analytical models and applying game theory, we identify opportunities where true win probability exceeds implied probability from the odds.

## Author

Built for serious handicappers seeking mathematical edges in thoroughbred racing.

## License

MIT License
