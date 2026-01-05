"""
THOROUGHBRED EDGE PRO - Game Theory Engine
Identifies inefficiencies in parimutuel pools and finds mispriced horses
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy.stats import norm


class GameTheoryEngine:
    """
    Game theory engine for thoroughbred racing value identification.
    Analyzes parimutuel pools to find mispriced horses with positive expected value.
    Emphasis on undervalued underdogs.
    """

    def __init__(self, track_takeout: float = 0.17):
        """
        Initialize game theory engine.

        Args:
            track_takeout: Track takeout percentage (default 17%)
        """
        self.track_takeout = track_takeout

    def calculate_implied_probability(self, odds: float) -> float:
        """
        Calculate implied probability from odds.

        Args:
            odds: Decimal odds (e.g., 5.0 for 5-1)

        Returns:
            Implied probability (0-1)
        """
        if odds <= 0:
            return 0.0

        # Convert to probability
        implied_prob = 1 / (odds + 1)

        return implied_prob

    def calculate_true_probability(
        self,
        speed_score: float,
        pace_score: float,
        form_score: float,
        field_size: int
    ) -> float:
        """
        Calculate true win probability from model scores.

        Args:
            speed_score: Speed model score (0-100)
            pace_score: Pace model score (0-100)
            form_score: Form model score (0-100)
            field_size: Number of horses in race

        Returns:
            True win probability (0-1)
        """
        # Weighted composite score
        weights = {'speed': 0.35, 'pace': 0.30, 'form': 0.35}

        composite = (
            speed_score * weights['speed'] +
            pace_score * weights['pace'] +
            form_score * weights['form']
        )

        # Convert to probability using logistic function
        # Adjust for field size
        base_prob = 1 / field_size
        max_prob = min(0.70, 3 / field_size)  # Cap at reasonable maximum

        # Sigmoid transformation
        normalized = (composite - 50) / 25  # Center at 50, scale
        prob = base_prob + (max_prob - base_prob) / (1 + np.exp(-normalized))

        return round(min(max(prob, 0.01), 0.95), 4)

    def calculate_expected_value(
        self,
        true_probability: float,
        odds: float
    ) -> float:
        """
        Calculate expected value (EV) of a bet.

        Args:
            true_probability: True win probability
            odds: Decimal odds

        Returns:
            Expected value (positive = profitable)
        """
        implied_prob = self.calculate_implied_probability(odds)

        # EV = (true_prob * payout) - (lose_prob * stake)
        # Payout = odds * stake
        # For $1 bet:
        ev = (true_probability * odds) - (1 - true_probability)

        return round(ev, 4)

    def calculate_overlay_percentage(
        self,
        true_probability: float,
        implied_probability: float
    ) -> float:
        """
        Calculate overlay percentage (how much better true odds are than implied).

        Args:
            true_probability: True win probability
            implied_probability: Implied probability from odds

        Returns:
            Overlay percentage (e.g., 1.25 = 25% overlay)
        """
        if implied_probability <= 0:
            return 0.0

        overlay = true_probability / implied_probability

        return round(overlay, 4)

    def identify_favorite_bias(
        self,
        horses: List[Dict]
    ) -> Dict[str, any]:
        """
        Identify favorite bias in the betting pool.
        Public tends to over-bet favorites and under-bet longshots.

        Args:
            horses: List of horse dictionaries with odds and probabilities

        Returns:
            Dictionary with bias analysis
        """
        if not horses:
            return {'bias': 'Unknown', 'severity': 0}

        # Sort by odds (lowest = favorite)
        sorted_horses = sorted(horses, key=lambda x: x.get('odds', 99))

        # Get favorite and longshots
        favorite = sorted_horses[0] if sorted_horses else None
        longshots = [h for h in horses if h.get('odds', 0) >= 10]

        if not favorite:
            return {'bias': 'Unknown', 'severity': 0}

        fav_implied_prob = self.calculate_implied_probability(favorite.get('odds', 3))
        fav_true_prob = favorite.get('true_probability', 0.3)

        # Calculate bias
        if fav_implied_prob > fav_true_prob * 1.15:
            bias = 'Heavy_Favorite_Bias'
            severity = 80
        elif fav_implied_prob > fav_true_prob * 1.05:
            bias = 'Moderate_Favorite_Bias'
            severity = 60
        else:
            bias = 'Balanced'
            severity = 30

        # Check longshot value
        longshot_overlays = sum(
            1 for h in longshots
            if h.get('true_probability', 0) > self.calculate_implied_probability(h.get('odds', 20))
        )

        return {
            'bias': bias,
            'severity': severity,
            'favorite_overlay': round((fav_implied_prob / fav_true_prob), 2) if fav_true_prob > 0 else 0,
            'longshot_opportunities': longshot_overlays
        }

    def calculate_kelly_criterion(
        self,
        true_probability: float,
        odds: float,
        bankroll: float = 1000,
        fraction: float = 0.25
    ) -> Dict[str, float]:
        """
        Calculate optimal bet size using Kelly Criterion.

        Args:
            true_probability: True win probability
            odds: Decimal odds
            bankroll: Total bankroll
            fraction: Fractional Kelly (0.25 = quarter Kelly, conservative)

        Returns:
            Dictionary with bet sizing recommendations
        """
        # Kelly formula: f = (bp - q) / b
        # where b = odds, p = true probability, q = 1 - p

        b = odds
        p = true_probability
        q = 1 - p

        # Full Kelly
        if b > 0:
            kelly_fraction = (b * p - q) / b
        else:
            kelly_fraction = 0

        # Apply fractional Kelly for safety
        kelly_fraction = kelly_fraction * fraction

        # Calculate bet amount
        if kelly_fraction > 0:
            bet_amount = bankroll * kelly_fraction
            bet_pct = kelly_fraction * 100
        else:
            bet_amount = 0
            bet_pct = 0

        return {
            'bet_amount': round(max(0, bet_amount), 2),
            'bet_percentage': round(max(0, bet_pct), 2),
            'full_kelly': round(kelly_fraction / fraction, 4),
            'recommendation': 'Bet' if bet_amount > 0 else 'Pass'
        }

    def analyze_crowd_psychology(
        self,
        horses: List[Dict],
        field_size: int
    ) -> Dict[str, any]:
        """
        Analyze crowd betting psychology to find inefficiencies.

        Args:
            horses: List of horse dictionaries
            field_size: Number of horses

        Returns:
            Dictionary with crowd psychology analysis
        """
        if not horses:
            return {'inefficiencies': [], 'opportunities': 0}

        inefficiencies = []

        # Calculate total implied probability
        total_implied = sum(
            self.calculate_implied_probability(h.get('odds', 10))
            for h in horses
        )

        # Should sum to ~1.17 (with takeout), but can vary
        if total_implied > 1.25:
            inefficiencies.append('Over-round excessive - strong favorite bias likely')
        elif total_implied < 1.10:
            inefficiencies.append('Under-round - unusual betting pattern')

        # Check for recency bias (horses with recent wins over-bet)
        recent_winners = [
            h for h in horses
            if h.get('last_race_finish', 99) == 1
        ]

        if recent_winners:
            for horse in recent_winners:
                implied = self.calculate_implied_probability(horse.get('odds', 5))
                true = horse.get('true_probability', 0.2)

                if implied > true * 1.20:
                    inefficiencies.append(
                        f"{horse.get('name', 'Unknown')} over-bet due to recency bias"
                    )

        # Check for post position bias (inside posts sometimes over-bet)
        inside_posts = [h for h in horses if h.get('post_position', 5) <= 3]

        if inside_posts:
            inside_avg_overlay = np.mean([
                self.calculate_overlay_percentage(
                    h.get('true_probability', 0.15),
                    self.calculate_implied_probability(h.get('odds', 8))
                )
                for h in inside_posts
            ])

            if inside_avg_overlay < 0.90:
                inefficiencies.append('Inside posts over-bet relative to true chances')

        # Check for trainer/jockey bias
        # Public often over-bets big name trainers
        for horse in horses:
            trainer = horse.get('trainer', '')
            if 'Baffert' in trainer or 'Pletcher' in trainer or 'Brown' in trainer:
                implied = self.calculate_implied_probability(horse.get('odds', 5))
                true = horse.get('true_probability', 0.2)

                if implied > true * 1.15:
                    inefficiencies.append(
                        f"{horse.get('name', 'Unknown')} over-bet due to trainer name recognition"
                    )

        return {
            'inefficiencies': inefficiencies,
            'opportunities': len(inefficiencies),
            'total_implied_probability': round(total_implied, 4)
        }

    def find_value_plays(
        self,
        horses: List[Dict],
        min_overlay: float = 1.15,
        min_odds: float = 3.0,
        max_odds: float = 50.0
    ) -> List[Dict]:
        """
        Find value plays with emphasis on underdogs.

        Args:
            horses: List of horse dictionaries with analysis
            min_overlay: Minimum overlay percentage (1.15 = 15% edge)
            min_odds: Minimum odds to consider
            max_odds: Maximum odds to consider (avoid extreme longshots)

        Returns:
            List of value plays sorted by expected value
        """
        value_plays = []

        for horse in horses:
            odds = horse.get('odds', 99)
            true_prob = horse.get('true_probability', 0.05)

            # Filter by odds range
            if odds < min_odds or odds > max_odds:
                continue

            implied_prob = self.calculate_implied_probability(odds)
            overlay = self.calculate_overlay_percentage(true_prob, implied_prob)
            ev = self.calculate_expected_value(true_prob, odds)

            # Must have positive overlay
            if overlay >= min_overlay and ev > 0:
                # Calculate confidence score
                speed_score = horse.get('speed_score', 50)
                pace_score = horse.get('pace_score', 50)
                form_score = horse.get('form_score', 50)

                # Higher scores = higher confidence
                avg_score = (speed_score + pace_score + form_score) / 3
                confidence = min(100, (avg_score / 70) * 100)

                # Underdog bonus
                underdog_bonus = 0
                if odds >= 8:
                    underdog_bonus = 15
                elif odds >= 5:
                    underdog_bonus = 10

                value_plays.append({
                    'horse': horse.get('name', 'Unknown'),
                    'post': horse.get('post_position', 0),
                    'odds': odds,
                    'true_probability': round(true_prob, 4),
                    'implied_probability': round(implied_prob, 4),
                    'overlay': round((overlay - 1) * 100, 2),  # As percentage
                    'expected_value': round(ev, 4),
                    'confidence': round(confidence + underdog_bonus, 2),
                    'speed_score': speed_score,
                    'pace_score': pace_score,
                    'form_score': form_score,
                    'angles': horse.get('angles', [])
                })

        # Sort by expected value (descending)
        value_plays.sort(key=lambda x: x['expected_value'], reverse=True)

        return value_plays

    def simulate_betting_scenarios(
        self,
        value_plays: List[Dict],
        num_simulations: int = 10000,
        bankroll: float = 1000
    ) -> Dict[str, any]:
        """
        Simulate betting scenarios using Monte Carlo.

        Args:
            value_plays: List of value play dictionaries
            num_simulations: Number of simulations to run
            bankroll: Starting bankroll

        Returns:
            Dictionary with simulation results
        """
        if not value_plays:
            return {'roi': 0, 'win_rate': 0, 'confidence': 0}

        results = []

        for _ in range(num_simulations):
            race_result = []

            for play in value_plays:
                # Simulate win/loss based on true probability
                win = np.random.random() < play['true_probability']

                if win:
                    profit = play['odds']
                else:
                    profit = -1

                race_result.append(profit)

            # Take best result (assuming we bet on all value plays)
            # In reality, might bet on subset
            results.append(max(race_result) if race_result else -1)

        # Calculate statistics
        roi = (np.mean(results) / 1.0) * 100  # ROI as percentage
        win_rate = sum(1 for r in results if r > 0) / len(results) * 100
        profit_factor = abs(sum(r for r in results if r > 0) / sum(r for r in results if r < 0)) if any(r < 0 for r in results) else 0

        return {
            'roi': round(roi, 2),
            'win_rate': round(win_rate, 2),
            'profit_factor': round(profit_factor, 2),
            'avg_return': round(np.mean(results), 2),
            'std_dev': round(np.std(results), 2),
            'confidence_95': round(roi - (1.96 * np.std(results)), 2)
        }

    def generate_betting_strategy(
        self,
        value_plays: List[Dict],
        bankroll: float = 1000,
        max_plays_per_race: int = 3
    ) -> Dict[str, any]:
        """
        Generate optimal betting strategy for the race.

        Args:
            value_plays: List of value plays
            bankroll: Total bankroll
            max_plays_per_race: Maximum number of horses to bet

        Returns:
            Dictionary with betting strategy
        """
        if not value_plays:
            return {'action': 'Pass', 'bets': [], 'total_risk': 0}

        # Select top plays by EV
        top_plays = value_plays[:max_plays_per_race]

        bets = []
        total_risk = 0

        for play in top_plays:
            # Calculate Kelly bet
            kelly = self.calculate_kelly_criterion(
                play['true_probability'],
                play['odds'],
                bankroll,
                fraction=0.20  # Conservative 1/5 Kelly
            )

            if kelly['bet_amount'] > 0:
                bets.append({
                    'horse': play['horse'],
                    'odds': play['odds'],
                    'bet_amount': kelly['bet_amount'],
                    'expected_profit': round(kelly['bet_amount'] * play['expected_value'], 2),
                    'overlay': play['overlay']
                })

                total_risk += kelly['bet_amount']

        if bets:
            action = 'Bet'
        else:
            action = 'Pass'

        return {
            'action': action,
            'bets': bets,
            'total_risk': round(total_risk, 2),
            'risk_percentage': round((total_risk / bankroll) * 100, 2)
        }
