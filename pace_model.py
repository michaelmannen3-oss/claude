"""
THOROUGHBRED EDGE PRO - Pace Model
Evaluates early, middle, and late pace scenarios with energy distribution analysis
"""

import numpy as np
from typing import Dict, List, Optional, Tuple


class PaceModel:
    """
    Pace model for thoroughbred racing analysis.
    Analyzes fractional times and energy distribution to predict pace scenarios.
    """

    # Pace style classifications
    PACE_STYLES = {
        'E': 'Early Speed',      # Front runner
        'EP': 'Early Presser',   # Stalks early leaders
        'P': 'Presser',          # Mid-pack, moves early
        'S': 'Sustained',        # Mid-pack, late move
        'C': 'Closer'            # Come from behind
    }

    def __init__(self):
        self.pace_scenarios = {}

    def calculate_fractional_pace(
        self,
        fractions: Dict[str, float],
        distance: float
    ) -> Dict[str, float]:
        """
        Calculate pace metrics from fractional times.

        Args:
            fractions: Dictionary of fractional times (e.g., {'2f': 22.5, '4f': 45.0, '6f': 69.0})
            distance: Total distance in furlongs

        Returns:
            Dictionary with early, middle, and late pace ratings
        """
        results = {
            'early_pace': 0,
            'middle_pace': 0,
            'late_pace': 0,
            'pace_distribution': 'Unknown'
        }

        if not fractions:
            return results

        # Sort fractions by distance
        sorted_fractions = sorted(fractions.items(), key=lambda x: float(x[0].replace('f', '')))

        # Early pace (first call) - faster is higher rating
        if len(sorted_fractions) >= 1:
            first_call = sorted_fractions[0][1]
            first_distance = float(sorted_fractions[0][0].replace('f', ''))
            # Par for 2f is ~23 seconds
            par_early = (first_distance / 2.0) * 23.0
            early_diff = par_early - first_call
            results['early_pace'] = round(100 + (early_diff * 5), 2)

        # Middle pace (second call to penultimate call)
        if len(sorted_fractions) >= 3:
            second_call = sorted_fractions[1][1]
            third_call = sorted_fractions[2][1]
            middle_split = third_call - second_call
            split_distance = float(sorted_fractions[2][0].replace('f', '')) - float(sorted_fractions[1][0].replace('f', ''))
            par_middle = (split_distance / 2.0) * 24.0  # Slightly slower than early
            middle_diff = par_middle - middle_split
            results['middle_pace'] = round(100 + (middle_diff * 5), 2)

        # Late pace (final fraction)
        if len(sorted_fractions) >= 2:
            second_last = sorted_fractions[-2][1]
            final_time = sorted_fractions[-1][1]
            late_split = final_time - second_last
            split_distance = float(sorted_fractions[-1][0].replace('f', '')) - float(sorted_fractions[-2][0].replace('f', ''))
            par_late = (split_distance / 2.0) * 25.0  # Slowest segment typically
            late_diff = par_late - late_split
            results['late_pace'] = round(100 + (late_diff * 5), 2)

        # Determine pace distribution
        early = results['early_pace']
        late = results['late_pace']

        if early > 105 and late < 95:
            results['pace_distribution'] = 'Front-loaded'
        elif early < 95 and late > 105:
            results['pace_distribution'] = 'Back-loaded'
        elif abs(early - late) < 5:
            results['pace_distribution'] = 'Even'
        else:
            results['pace_distribution'] = 'Mixed'

        return results

    def determine_running_style(
        self,
        past_performances: List[Dict],
        num_races: int = 5
    ) -> Dict[str, any]:
        """
        Determine horse's typical running style from past performances.

        Args:
            past_performances: List of past performance dictionaries
            num_races: Number of races to analyze

        Returns:
            Dictionary with running style classification and consistency
        """
        if not past_performances:
            return {'style': 'Unknown', 'consistency': 0, 'style_code': 'S'}

        recent_races = past_performances[:num_races]
        position_data = []

        for race in recent_races:
            # Get position at first call and final position
            first_call_pos = race.get('first_call_position', 5)
            final_pos = race.get('final_position', 5)
            field_size = race.get('field_size', 8)

            # Calculate relative positions
            first_call_rel = first_call_pos / field_size
            position_data.append(first_call_rel)

        if not position_data:
            return {'style': 'Unknown', 'consistency': 0, 'style_code': 'S'}

        avg_early_position = np.mean(position_data)

        # Classify running style
        if avg_early_position <= 0.2:
            style_code = 'E'
        elif avg_early_position <= 0.35:
            style_code = 'EP'
        elif avg_early_position <= 0.5:
            style_code = 'P'
        elif avg_early_position <= 0.7:
            style_code = 'S'
        else:
            style_code = 'C'

        # Calculate consistency (lower std = more consistent)
        consistency = max(0, 100 - (np.std(position_data) * 100))

        return {
            'style': self.PACE_STYLES[style_code],
            'style_code': style_code,
            'consistency': round(consistency, 2),
            'avg_early_position_pct': round(avg_early_position * 100, 1)
        }

    def analyze_pace_scenario(
        self,
        horses: List[Dict],
        distance: float
    ) -> Dict[str, any]:
        """
        Analyze projected pace scenario for the entire race.
        Critical for finding undervalued closers in speed-heavy races.

        Args:
            horses: List of horse dictionaries with running styles
            distance: Race distance in furlongs

        Returns:
            Dictionary with pace scenario analysis
        """
        if not horses:
            return {'scenario': 'Unknown', 'pace_pressure': 0, 'advantages': []}

        # Count horses by running style
        style_counts = {'E': 0, 'EP': 0, 'P': 0, 'S': 0, 'C': 0}

        for horse in horses:
            style = horse.get('running_style', {}).get('style_code', 'S')
            style_counts[style] = style_counts.get(style, 0) + 1

        total_horses = len(horses)
        early_speed_count = style_counts['E'] + style_counts['EP']
        closer_count = style_counts['C'] + style_counts['S']

        # Calculate pace pressure (0-100 scale)
        pace_pressure = (early_speed_count / total_horses) * 100

        # Determine scenario
        if early_speed_count >= 4:
            scenario = 'Hot Pace'
            advantages = ['C', 'S']  # Closers and sustained runners benefit
        elif early_speed_count <= 1:
            scenario = 'Slow Pace'
            advantages = ['E', 'EP']  # Early speed will dominate
        elif closer_count >= 5:
            scenario = 'Closer-Heavy'
            advantages = ['E', 'EP']  # Early speed has advantage
        else:
            scenario = 'Honest Pace'
            advantages = ['EP', 'P', 'S']  # Balanced scenario

        # Adjust for distance
        if distance >= 9:  # Routes favor closers more
            if 'C' not in advantages and scenario == 'Hot Pace':
                advantages.append('C')
        elif distance <= 6:  # Sprints favor speed
            if 'E' not in advantages:
                advantages = ['E'] + advantages

        return {
            'scenario': scenario,
            'pace_pressure': round(pace_pressure, 2),
            'early_speed_count': early_speed_count,
            'closer_count': closer_count,
            'advantages': advantages,
            'style_distribution': style_counts
        }

    def calculate_pace_advantage(
        self,
        horse_style: str,
        race_scenario: Dict,
        distance: float
    ) -> float:
        """
        Calculate how much a horse's running style benefits from the pace scenario.
        High scores indicate undervalued horses.

        Args:
            horse_style: Horse's running style code (E, EP, P, S, C)
            race_scenario: Race pace scenario from analyze_pace_scenario
            distance: Race distance in furlongs

        Returns:
            Pace advantage score (0-100, higher is better)
        """
        base_advantage = 50  # Neutral

        advantaged_styles = race_scenario.get('advantages', [])

        if horse_style in advantaged_styles:
            # Horse is advantaged by pace scenario
            pace_pressure = race_scenario.get('pace_pressure', 50)

            if horse_style in ['C', 'S'] and pace_pressure > 70:
                # Closer in hot pace - strong advantage
                base_advantage += 30
            elif horse_style in ['E', 'EP'] and pace_pressure < 30:
                # Speed in slow pace - strong advantage
                base_advantage += 30
            else:
                # Moderate advantage
                base_advantage += 15
        else:
            # Horse is disadvantaged
            base_advantage -= 20

        # Distance adjustment
        if distance >= 9 and horse_style in ['C', 'S']:
            base_advantage += 10
        elif distance <= 6 and horse_style in ['E', 'EP']:
            base_advantage += 10

        return round(min(100, max(0, base_advantage)), 2)

    def calculate_energy_distribution(
        self,
        fractions: Dict[str, float],
        distance: float,
        running_style: str
    ) -> Dict[str, float]:
        """
        Calculate optimal energy distribution for a horse based on style.
        Used to identify horses running inefficient pace patterns.

        Args:
            fractions: Fractional times from past race
            distance: Distance in furlongs
            running_style: Horse's running style code

        Returns:
            Dictionary with energy distribution metrics
        """
        # Energy allocation by running style (early%, middle%, late%)
        OPTIMAL_DISTRIBUTIONS = {
            'E': (0.45, 0.35, 0.20),
            'EP': (0.40, 0.35, 0.25),
            'P': (0.35, 0.35, 0.30),
            'S': (0.30, 0.35, 0.35),
            'C': (0.25, 0.35, 0.40)
        }

        optimal = OPTIMAL_DISTRIBUTIONS.get(running_style, (0.33, 0.33, 0.34))

        # Calculate actual energy distribution from fractions
        pace_ratings = self.calculate_fractional_pace(fractions, distance)

        early = pace_ratings.get('early_pace', 100)
        middle = pace_ratings.get('middle_pace', 100)
        late = pace_ratings.get('late_pace', 100)

        # Normalize to percentages
        total = early + middle + late
        if total > 0:
            actual = (early / total, middle / total, late / total)
        else:
            actual = (0.33, 0.33, 0.34)

        # Calculate deviation from optimal
        deviation = sum(abs(a - o) for a, o in zip(actual, optimal))
        efficiency = max(0, 100 - (deviation * 100))

        return {
            'optimal_distribution': optimal,
            'actual_distribution': actual,
            'efficiency': round(efficiency, 2),
            'deviation': round(deviation, 4)
        }

    def identify_pace_angles(
        self,
        horses: List[Dict],
        race_scenario: Dict
    ) -> List[Dict]:
        """
        Identify horses with pace advantages (underdog angles).

        Args:
            horses: List of horse dictionaries
            race_scenario: Pace scenario analysis

        Returns:
            List of horses with significant pace advantages
        """
        pace_angles = []

        for horse in horses:
            style = horse.get('running_style', {}).get('style_code', 'S')
            odds = horse.get('odds', 99)

            # Calculate pace advantage
            advantage = self.calculate_pace_advantage(
                style,
                race_scenario,
                horse.get('distance', 6)
            )

            # Look for undervalued horses with pace advantages
            # Higher odds (underdogs) with high pace advantage = VALUE
            if advantage >= 65 and odds >= 8:
                pace_angles.append({
                    'horse': horse.get('name', 'Unknown'),
                    'pace_advantage': advantage,
                    'odds': odds,
                    'running_style': style,
                    'angle': 'Undervalued closer in hot pace' if style in ['C', 'S'] else 'Lone speed'
                })

        # Sort by pace advantage
        pace_angles.sort(key=lambda x: x['pace_advantage'], reverse=True)

        return pace_angles
