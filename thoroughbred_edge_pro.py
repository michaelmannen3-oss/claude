"""
THOROUGHBRED EDGE PRO - Main Interface
Three-Model Convergence System for Horse Racing Value Identification
"""

import numpy as np
from typing import Dict, List, Optional
from speed_model import SpeedModel
from pace_model import PaceModel
from form_model import FormModel
from game_theory_engine import GameTheoryEngine


class ThoroughbredEdgePro:
    """
    Main interface for THOROUGHBRED EDGE PRO.
    Integrates speed, pace, and form models with game theory analysis.
    """

    def __init__(self, track_takeout: float = 0.17):
        """
        Initialize THOROUGHBRED EDGE PRO system.

        Args:
            track_takeout: Track takeout percentage (default 17%)
        """
        self.speed_model = SpeedModel()
        self.pace_model = PaceModel()
        self.form_model = FormModel()
        self.game_theory = GameTheoryEngine(track_takeout)

        self.version = "1.0.0"
        self.name = "THOROUGHBRED EDGE PRO"

    def analyze_horse(
        self,
        horse_data: Dict,
        race_context: Dict
    ) -> Dict[str, any]:
        """
        Comprehensive analysis of a single horse.

        Args:
            horse_data: Dictionary containing horse information and past performances
            race_context: Dictionary containing race information

        Returns:
            Complete analysis dictionary
        """
        # Extract data
        past_performances = horse_data.get('past_performances', [])
        current_class = race_context.get('class_level', 'Claiming_Mid')
        distance = race_context.get('distance', 6)
        surface = race_context.get('surface', 'dirt')

        # Speed Model Analysis
        speed_analysis = self.speed_model.calculate_average_speed_rating(
            past_performances,
            num_races=3,
            recency_weight=True
        )

        speed_improvement = self.speed_model.identify_speed_improvements(
            past_performances,
            lookback=5
        )

        speed_score = speed_analysis['average']

        # Pace Model Analysis
        running_style = self.pace_model.determine_running_style(
            past_performances,
            num_races=5
        )

        pace_score = 50  # Base score, will be adjusted by race scenario

        # Form Model Analysis
        class_rating = self.form_model.calculate_class_rating(
            current_class,
            past_performances,
            num_races=5
        )

        recency = self.form_model.calculate_recency_rating(
            horse_data.get('days_since_last_race', 30),
            horse_data.get('days_since_workout')
        )

        recent_form = self.form_model.analyze_recent_form(
            past_performances,
            num_races=5
        )

        connections = self.form_model.calculate_trainer_jockey_rating(
            horse_data.get('trainer', 'Unknown'),
            horse_data.get('jockey', 'Unknown'),
            horse_data.get('trainer_stats'),
            horse_data.get('jockey_stats'),
            horse_data.get('trainer_jockey_stats')
        )

        distance_suit = self.form_model.calculate_distance_suitability(
            distance,
            past_performances
        )

        bounce_analysis = self.form_model.identify_bounce_candidates(
            past_performances
        )

        form_score = self.form_model.calculate_composite_form_score(
            class_rating,
            recency,
            recent_form,
            connections,
            distance_suit
        )

        # Identify angles
        angles = []

        # Speed angles
        if speed_improvement['improving']:
            angles.append(f"Speed improving: +{speed_improvement['trend']:.1f} pts/race")

        # Form angles
        if class_rating['movement'] == 'Dropping':
            angles.append("Dropping in class - KEY ANGLE")

        if recent_form['form_cycle'] == 'Ascending':
            angles.append("Form cycle ascending")

        # Equipment angles
        if horse_data.get('equipment_changes'):
            eq_changes = self.form_model.analyze_equipment_changes(
                horse_data.get('current_equipment', {}),
                horse_data.get('past_equipment', {})
            )
            if eq_changes['significant']:
                for change in eq_changes['changes']:
                    angles.append(change.replace('_', ' '))

        # Bounce risk
        if bounce_analysis['bounce_risk'] >= 70:
            angles.append(f"BOUNCE RISK: {bounce_analysis['reason']}")

        return {
            'name': horse_data.get('name', 'Unknown'),
            'post_position': horse_data.get('post_position', 0),
            'odds': horse_data.get('odds', 99),
            'speed_score': round(speed_score, 2),
            'pace_score': pace_score,
            'form_score': round(form_score, 2),
            'running_style': running_style,
            'speed_analysis': speed_analysis,
            'speed_improvement': speed_improvement,
            'class_rating': class_rating,
            'recency': recency,
            'recent_form': recent_form,
            'connections': connections,
            'distance_suitability': distance_suit,
            'bounce_analysis': bounce_analysis,
            'angles': angles
        }

    def analyze_race(
        self,
        race_data: Dict
    ) -> Dict[str, any]:
        """
        Analyze entire race with all horses.

        Args:
            race_data: Dictionary containing race information and all horses

        Returns:
            Complete race analysis
        """
        horses = race_data.get('horses', [])
        race_context = {
            'distance': race_data.get('distance', 6),
            'surface': race_data.get('surface', 'dirt'),
            'class_level': race_data.get('class_level', 'Claiming_Mid'),
            'track_condition': race_data.get('track_condition', 'fast')
        }

        # Analyze each horse
        horse_analyses = []

        for horse_data in horses:
            analysis = self.analyze_horse(horse_data, race_context)
            horse_analyses.append(analysis)

        # Pace Scenario Analysis
        pace_scenario = self.pace_model.analyze_pace_scenario(
            horse_analyses,
            race_context['distance']
        )

        # Adjust pace scores based on scenario
        for analysis in horse_analyses:
            style = analysis['running_style']['style_code']
            pace_advantage = self.pace_model.calculate_pace_advantage(
                style,
                pace_scenario,
                race_context['distance']
            )
            analysis['pace_score'] = pace_advantage
            analysis['pace_advantage'] = pace_advantage

        # Identify pace angles
        pace_angles = self.pace_model.identify_pace_angles(
            horse_analyses,
            pace_scenario
        )

        # Calculate true probabilities
        field_size = len(horses)

        for analysis in horse_analyses:
            true_prob = self.game_theory.calculate_true_probability(
                analysis['speed_score'],
                analysis['pace_score'],
                analysis['form_score'],
                field_size
            )
            analysis['true_probability'] = true_prob

        # Game Theory Analysis
        favorite_bias = self.game_theory.identify_favorite_bias(horse_analyses)
        crowd_psychology = self.game_theory.analyze_crowd_psychology(
            horse_analyses,
            field_size
        )

        return {
            'race_info': race_context,
            'field_size': field_size,
            'horses': horse_analyses,
            'pace_scenario': pace_scenario,
            'pace_angles': pace_angles,
            'favorite_bias': favorite_bias,
            'crowd_psychology': crowd_psychology
        }

    def find_value_bets(
        self,
        race_analysis: Dict,
        min_overlay: float = 1.15,
        min_odds: float = 3.0,
        max_odds: float = 50.0,
        bankroll: float = 1000
    ) -> Dict[str, any]:
        """
        Find value betting opportunities with emphasis on underdogs.

        Args:
            race_analysis: Race analysis from analyze_race()
            min_overlay: Minimum overlay percentage (1.15 = 15% edge)
            min_odds: Minimum odds to consider
            max_odds: Maximum odds to consider
            bankroll: Betting bankroll

        Returns:
            Dictionary with value plays and betting strategy
        """
        horses = race_analysis.get('horses', [])

        # Find value plays
        value_plays = self.game_theory.find_value_plays(
            horses,
            min_overlay=min_overlay,
            min_odds=min_odds,
            max_odds=max_odds
        )

        # Simulate betting scenarios
        simulation = self.game_theory.simulate_betting_scenarios(
            value_plays,
            num_simulations=10000,
            bankroll=bankroll
        )

        # Generate betting strategy
        strategy = self.game_theory.generate_betting_strategy(
            value_plays,
            bankroll=bankroll,
            max_plays_per_race=3
        )

        return {
            'value_plays': value_plays,
            'simulation': simulation,
            'strategy': strategy,
            'pace_scenario': race_analysis.get('pace_scenario'),
            'favorite_bias': race_analysis.get('favorite_bias'),
            'num_opportunities': len(value_plays)
        }

    def display_analysis(
        self,
        value_analysis: Dict,
        verbose: bool = True
    ) -> str:
        """
        Display analysis results in readable format.

        Args:
            value_analysis: Value analysis from find_value_bets()
            verbose: Whether to show detailed information

        Returns:
            Formatted analysis string
        """
        output = []
        output.append("=" * 60)
        output.append(f"{self.name} v{self.version}")
        output.append("=" * 60)
        output.append("")

        # Pace Scenario
        pace = value_analysis.get('pace_scenario', {})
        output.append(f"PACE SCENARIO: {pace.get('scenario', 'Unknown')}")
        output.append(f"Pace Pressure: {pace.get('pace_pressure', 0):.1f}/100")
        output.append(f"Advantaged Styles: {', '.join(pace.get('advantages', []))}")
        output.append("")

        # Favorite Bias
        bias = value_analysis.get('favorite_bias', {})
        output.append(f"CROWD BIAS: {bias.get('bias', 'Unknown')}")
        output.append(f"Longshot Opportunities: {bias.get('longshot_opportunities', 0)}")
        output.append("")

        # Value Plays
        value_plays = value_analysis.get('value_plays', [])
        output.append(f"VALUE PLAYS IDENTIFIED: {len(value_plays)}")
        output.append("-" * 60)

        for i, play in enumerate(value_plays, 1):
            output.append(f"\n#{i} - {play['horse']} (Post {play['post']})")
            output.append(f"   Odds: {play['odds']:.1f}-1")
            output.append(f"   Overlay: {play['overlay']:.1f}%")
            output.append(f"   Expected Value: {play['expected_value']:.3f}")
            output.append(f"   Confidence: {play['confidence']:.1f}/100")
            output.append(f"   Scores - Speed: {play['speed_score']:.1f} | Pace: {play['pace_score']:.1f} | Form: {play['form_score']:.1f}")

            if play.get('angles'):
                output.append(f"   Angles: {', '.join(play['angles'][:3])}")

        # Simulation Results
        if verbose:
            sim = value_analysis.get('simulation', {})
            output.append("\n" + "-" * 60)
            output.append("SIMULATION RESULTS (10,000 iterations)")
            output.append(f"Expected ROI: {sim.get('roi', 0):.2f}%")
            output.append(f"Win Rate: {sim.get('win_rate', 0):.2f}%")
            output.append(f"Profit Factor: {sim.get('profit_factor', 0):.2f}")
            output.append("")

        # Betting Strategy
        strategy = value_analysis.get('strategy', {})
        output.append("-" * 60)
        output.append(f"RECOMMENDED ACTION: {strategy.get('action', 'Pass')}")

        if strategy.get('bets'):
            output.append(f"Total Risk: ${strategy.get('total_risk', 0):.2f} ({strategy.get('risk_percentage', 0):.1f}% of bankroll)")
            output.append("\nBetting Recommendations:")

            for bet in strategy['bets']:
                output.append(f"  ${bet['bet_amount']:.2f} on {bet['horse']} @ {bet['odds']:.1f}-1")
                output.append(f"    Expected Profit: ${bet['expected_profit']:.2f}")

        output.append("\n" + "=" * 60)

        return "\n".join(output)

    def get_underdog_specials(
        self,
        race_analysis: Dict,
        min_odds: float = 8.0
    ) -> List[Dict]:
        """
        Get special underdog plays (emphasis of the system).

        Args:
            race_analysis: Race analysis from analyze_race()
            min_odds: Minimum odds to qualify as underdog

        Returns:
            List of underdog special plays
        """
        horses = race_analysis.get('horses', [])

        underdog_specials = []

        for horse in horses:
            odds = horse.get('odds', 99)

            if odds < min_odds:
                continue

            # Check for underdog angles
            angles = horse.get('angles', [])
            speed_improving = horse.get('speed_improvement', {}).get('improving', False)
            class_drop = horse.get('class_rating', {}).get('movement') == 'Dropping'
            pace_advantage = horse.get('pace_advantage', 50)

            # Must have at least one strong angle
            if speed_improving or class_drop or pace_advantage >= 70:
                underdog_specials.append({
                    'horse': horse.get('name'),
                    'odds': odds,
                    'key_angles': [a for a in angles if 'KEY' in a or 'improving' in a or 'class' in a.lower()],
                    'speed_score': horse.get('speed_score'),
                    'pace_advantage': pace_advantage,
                    'form_score': horse.get('form_score'),
                    'true_probability': horse.get('true_probability')
                })

        # Sort by true probability
        underdog_specials.sort(key=lambda x: x['true_probability'], reverse=True)

        return underdog_specials
