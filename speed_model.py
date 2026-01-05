"""
THOROUGHBRED EDGE PRO - Speed Model
Analyzes raw velocity, track-adjusted speed ratings, and performance metrics
"""

import numpy as np
from typing import Dict, List, Optional


class SpeedModel:
    """
    Speed model for thoroughbred racing analysis.
    Calculates Beyer-style speed figures with track variant adjustments.
    """

    # Class par speeds (baseline for different class levels)
    CLASS_PARS = {
        'Grade_1': 110,
        'Grade_2': 105,
        'Grade_3': 100,
        'Stakes': 95,
        'Allowance': 90,
        'Claiming_High': 85,
        'Claiming_Mid': 80,
        'Claiming_Low': 75,
        'Maiden_Special': 82,
        'Maiden_Claiming': 72
    }

    # Surface adjustments (dirt baseline = 0)
    SURFACE_ADJUSTMENTS = {
        'dirt': 0,
        'turf': -3,
        'synthetic': -2,
        'wet_dirt': -4,
        'wet_turf': -5
    }

    def __init__(self):
        self.track_variants = {}  # Stores computed track variants

    def calculate_speed_figure(
        self,
        final_time: float,
        distance: float,
        class_level: str,
        surface: str,
        track_condition: str = 'fast',
        beaten_lengths: float = 0
    ) -> float:
        """
        Calculate Beyer-style speed figure.

        Args:
            final_time: Final time in seconds
            distance: Distance in furlongs (1 furlong = 220 yards)
            class_level: Class level of the race
            surface: Track surface type
            track_condition: Track condition
            beaten_lengths: Lengths beaten (0 if winner)

        Returns:
            Speed figure (higher is better)
        """
        # Get class par
        class_par = self.CLASS_PARS.get(class_level, 80)

        # Calculate par time for distance (baseline: 6f in 1:10 = 70 seconds)
        par_time = (distance / 6.0) * 70.0

        # Adjust for class
        par_time_adjusted = par_time * (100 / class_par)

        # Calculate raw speed figure
        time_difference = par_time_adjusted - final_time
        raw_figure = 100 + (time_difference * 5)  # 5 points per second

        # Adjust for surface
        surface_key = surface if track_condition == 'fast' else f'wet_{surface}'
        surface_adj = self.SURFACE_ADJUSTMENTS.get(surface_key, 0)

        # Adjust for beaten lengths (1 length ≈ 1 point)
        length_adj = beaten_lengths * 1.0

        # Final speed figure
        speed_figure = raw_figure + surface_adj - length_adj

        return round(speed_figure, 2)

    def calculate_track_variant(self, race_results: List[Dict]) -> float:
        """
        Calculate track variant based on multiple races on the same day.

        Args:
            race_results: List of race result dictionaries

        Returns:
            Track variant (positive = fast track, negative = slow track)
        """
        if not race_results:
            return 0.0

        variants = []
        for race in race_results:
            expected_figure = self.CLASS_PARS.get(race.get('class_level', 'Claiming_Mid'), 80)
            actual_figure = race.get('raw_speed_figure', 80)
            variant = actual_figure - expected_figure
            variants.append(variant)

        # Average variant across all races
        track_variant = np.mean(variants)
        return round(track_variant, 2)

    def calculate_velocity_rating(
        self,
        final_time: float,
        distance: float,
        weight_carried: int = 120
    ) -> float:
        """
        Calculate velocity rating (feet per second, adjusted for weight).

        Args:
            final_time: Final time in seconds
            distance: Distance in furlongs
            weight_carried: Weight carried in pounds

        Returns:
            Velocity rating
        """
        # Convert furlongs to feet (1 furlong = 660 feet)
        distance_feet = distance * 660

        # Raw velocity
        velocity = distance_feet / final_time

        # Weight adjustment (1 point per 5 lbs over 120)
        weight_adj = (126 - weight_carried) / 5.0

        adjusted_velocity = velocity + weight_adj

        return round(adjusted_velocity, 2)

    def normalize_across_distances(
        self,
        speed_figure: float,
        distance: float,
        target_distance: float = 6.0
    ) -> float:
        """
        Normalize speed figures across different distances.

        Args:
            speed_figure: Original speed figure
            distance: Original distance in furlongs
            target_distance: Target distance for normalization (default 6f)

        Returns:
            Normalized speed figure
        """
        # Sprint vs route adjustment
        if distance < 8 and target_distance >= 8:
            # Penalize sprinters in routes
            adjustment = -3
        elif distance >= 8 and target_distance < 8:
            # Penalize routers in sprints
            adjustment = -2
        else:
            adjustment = 0

        # Distance differential adjustment
        dist_diff = abs(distance - target_distance)
        if dist_diff > 2:
            adjustment -= dist_diff * 0.5

        normalized = speed_figure + adjustment
        return round(normalized, 2)

    def calculate_average_speed_rating(
        self,
        past_performances: List[Dict],
        num_races: int = 3,
        recency_weight: bool = True
    ) -> Dict[str, float]:
        """
        Calculate average speed rating from past performances.

        Args:
            past_performances: List of past performance dictionaries
            num_races: Number of recent races to consider
            recency_weight: Whether to weight recent races more heavily

        Returns:
            Dictionary with average, best, and consistency metrics
        """
        if not past_performances:
            return {'average': 0, 'best': 0, 'consistency': 0}

        # Sort by date (most recent first)
        sorted_races = sorted(
            past_performances,
            key=lambda x: x.get('date', ''),
            reverse=True
        )[:num_races]

        figures = [race.get('speed_figure', 0) for race in sorted_races]

        if not figures:
            return {'average': 0, 'best': 0, 'consistency': 0}

        if recency_weight:
            # Weight recent races more heavily (exponential decay)
            weights = [0.5 ** i for i in range(len(figures))]
            weights = np.array(weights) / np.sum(weights)
            average = np.average(figures, weights=weights)
        else:
            average = np.mean(figures)

        best = max(figures)
        consistency = 100 - (np.std(figures) * 2)  # Lower std = higher consistency

        return {
            'average': round(average, 2),
            'best': round(best, 2),
            'consistency': round(max(0, consistency), 2)
        }

    def identify_speed_improvements(
        self,
        past_performances: List[Dict],
        lookback: int = 5
    ) -> Dict[str, any]:
        """
        Identify horses showing speed figure improvements (underdog indicators).

        Args:
            past_performances: List of past performance dictionaries
            lookback: Number of races to analyze

        Returns:
            Dictionary with improvement metrics
        """
        if len(past_performances) < 2:
            return {'improving': False, 'trend': 0, 'acceleration': 0}

        sorted_races = sorted(
            past_performances,
            key=lambda x: x.get('date', ''),
            reverse=True
        )[:lookback]

        figures = [race.get('speed_figure', 0) for race in sorted_races]

        if len(figures) < 2:
            return {'improving': False, 'trend': 0, 'acceleration': 0}

        # Calculate trend (linear regression slope)
        x = np.arange(len(figures))
        trend = np.polyfit(x, figures, 1)[0]

        # Calculate acceleration (change in trend)
        if len(figures) >= 3:
            recent_trend = figures[0] - figures[1]
            older_trend = figures[-2] - figures[-1]
            acceleration = recent_trend - older_trend
        else:
            acceleration = 0

        improving = trend > 1.5  # Improving if gaining 1.5+ points per race

        return {
            'improving': improving,
            'trend': round(trend, 2),
            'acceleration': round(acceleration, 2),
            'recent_best': max(figures[:3]) if len(figures) >= 3 else max(figures)
        }
