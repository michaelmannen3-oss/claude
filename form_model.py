"""
THOROUGHBRED EDGE PRO - Form Model
Assesses class levels, recent performance, trainer/jockey statistics, and connections
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class FormModel:
    """
    Form model for thoroughbred racing analysis.
    Evaluates recent performance, class, connections, and form cycles.
    """

    # Class level hierarchy (higher is better)
    CLASS_HIERARCHY = {
        'Grade_1': 10,
        'Grade_2': 9,
        'Grade_3': 8,
        'Stakes': 7,
        'Allowance': 6,
        'Claiming_High': 5,
        'Claiming_Mid': 4,
        'Claiming_Low': 3,
        'Maiden_Special': 4,
        'Maiden_Claiming': 2
    }

    def __init__(self):
        self.trainer_stats = {}
        self.jockey_stats = {}

    def calculate_class_rating(
        self,
        current_class: str,
        past_performances: List[Dict],
        num_races: int = 5
    ) -> Dict[str, any]:
        """
        Calculate class rating and identify class movements.

        Args:
            current_class: Current race class level
            past_performances: List of past performance dictionaries
            num_races: Number of races to analyze

        Returns:
            Dictionary with class metrics
        """
        current_level = self.CLASS_HIERARCHY.get(current_class, 5)

        if not past_performances:
            return {
                'class_rating': 50,
                'movement': 'Unknown',
                'avg_class': current_level,
                'best_class': current_level
            }

        recent_races = past_performances[:num_races]
        class_levels = [
            self.CLASS_HIERARCHY.get(race.get('class_level', 'Claiming_Mid'), 4)
            for race in recent_races
        ]

        avg_class = np.mean(class_levels)
        best_class = max(class_levels)

        # Determine class movement
        if current_level > avg_class + 1:
            movement = 'Rising'
            class_rating = 70  # Rising in class = tougher
        elif current_level < avg_class - 1:
            movement = 'Dropping'
            class_rating = 85  # Dropping in class = easier (UNDERDOG ANGLE)
        else:
            movement = 'Stable'
            class_rating = 75

        # Bonus for proven ability at this level
        if current_level in class_levels:
            class_rating += 10

        return {
            'class_rating': min(100, class_rating),
            'movement': movement,
            'avg_class': round(avg_class, 2),
            'best_class': best_class,
            'class_experience': current_level in class_levels
        }

    def calculate_recency_rating(
        self,
        days_since_last_race: int,
        days_since_workout: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Calculate recency rating based on layoff patterns.

        Args:
            days_since_last_race: Days since last race
            days_since_workout: Days since last workout (optional)

        Returns:
            Dictionary with recency metrics
        """
        # Optimal range is 14-45 days
        if 14 <= days_since_last_race <= 45:
            recency_rating = 90
            status = 'Optimal'
        elif 7 <= days_since_last_race < 14:
            recency_rating = 85
            status = 'Fresh'
        elif 45 < days_since_last_race <= 90:
            recency_rating = 70
            status = 'Off_Pace'
        elif days_since_last_race > 90:
            recency_rating = 50
            status = 'Layoff'
            # Check for workout - if recent workout, could be sharp
            if days_since_workout and days_since_workout <= 7:
                recency_rating += 20
                status = 'Layoff_With_Works'
        else:
            recency_rating = 60
            status = 'Too_Fresh'

        return {
            'recency_rating': recency_rating,
            'status': status,
            'days_off': days_since_last_race
        }

    def analyze_recent_form(
        self,
        past_performances: List[Dict],
        num_races: int = 5
    ) -> Dict[str, any]:
        """
        Analyze recent form cycle (wins, places, improvements).

        Args:
            past_performances: List of past performance dictionaries
            num_races: Number of races to analyze

        Returns:
            Dictionary with form metrics
        """
        if not past_performances:
            return {
                'form_rating': 50,
                'wins': 0,
                'places': 0,
                'trend': 'Unknown',
                'form_cycle': 'Unknown'
            }

        recent_races = past_performances[:num_races]

        wins = sum(1 for r in recent_races if r.get('finish_position', 99) == 1)
        places = sum(1 for r in recent_races if r.get('finish_position', 99) <= 3)

        # Calculate finish position trend
        positions = [r.get('finish_position', 8) for r in recent_races]

        if len(positions) >= 3:
            # Negative trend = improving (lower positions)
            trend_slope = np.polyfit(range(len(positions)), positions, 1)[0]

            if trend_slope < -0.5:
                trend = 'Improving'
                form_rating = 80
            elif trend_slope > 0.5:
                trend = 'Declining'
                form_rating = 60
            else:
                trend = 'Stable'
                form_rating = 70
        else:
            trend = 'Insufficient_Data'
            form_rating = 65

        # Adjust for wins/places
        form_rating += (wins * 10) + (places * 3)

        # Form cycle classification
        if wins >= 2:
            form_cycle = 'Peak'
        elif places >= 3:
            form_cycle = 'Competitive'
        elif trend == 'Improving':
            form_cycle = 'Ascending'  # KEY UNDERDOG ANGLE
        elif trend == 'Declining':
            form_cycle = 'Descending'
        else:
            form_cycle = 'Moderate'

        return {
            'form_rating': min(100, form_rating),
            'wins': wins,
            'places': places,
            'trend': trend,
            'form_cycle': form_cycle,
            'avg_finish': round(np.mean(positions), 2)
        }

    def calculate_trainer_jockey_rating(
        self,
        trainer: str,
        jockey: str,
        trainer_stats: Optional[Dict] = None,
        jockey_stats: Optional[Dict] = None,
        trainer_jockey_combo_stats: Optional[Dict] = None
    ) -> Dict[str, float]:
        """
        Calculate trainer/jockey ratings and combo bonus.

        Args:
            trainer: Trainer name
            jockey: Jockey name
            trainer_stats: Trainer statistics (win%, ROI, etc.)
            jockey_stats: Jockey statistics
            trainer_jockey_combo_stats: Trainer/jockey combination statistics

        Returns:
            Dictionary with connection ratings
        """
        # Default ratings
        trainer_rating = 50
        jockey_rating = 50
        combo_bonus = 0

        # Trainer rating
        if trainer_stats:
            win_pct = trainer_stats.get('win_percentage', 10)
            roi = trainer_stats.get('roi', 0.70)

            trainer_rating = min(100, (win_pct * 3) + (roi * 20))

        # Jockey rating
        if jockey_stats:
            win_pct = jockey_stats.get('win_percentage', 10)
            roi = jockey_stats.get('roi', 0.70)

            jockey_rating = min(100, (win_pct * 3) + (roi * 20))

        # Combo bonus (trainer/jockey teams can be powerful)
        if trainer_jockey_combo_stats:
            combo_win_pct = trainer_jockey_combo_stats.get('win_percentage', 0)
            combo_starts = trainer_jockey_combo_stats.get('starts', 0)

            if combo_starts >= 5:  # Established team
                if combo_win_pct >= 25:
                    combo_bonus = 20
                elif combo_win_pct >= 15:
                    combo_bonus = 10

        return {
            'trainer_rating': round(trainer_rating, 2),
            'jockey_rating': round(jockey_rating, 2),
            'combo_bonus': combo_bonus,
            'connections_rating': round((trainer_rating + jockey_rating) / 2 + combo_bonus, 2)
        }

    def analyze_equipment_changes(
        self,
        current_equipment: Dict,
        past_equipment: Dict
    ) -> Dict[str, any]:
        """
        Analyze impact of equipment changes (blinkers, lasix, etc.).

        Args:
            current_equipment: Current race equipment
            past_equipment: Previous race equipment

        Returns:
            Dictionary with equipment change analysis
        """
        changes = []
        impact_score = 0

        # Blinkers
        if current_equipment.get('blinkers') and not past_equipment.get('blinkers'):
            changes.append('Blinkers_On')
            impact_score += 10  # Blinkers on can help focus
        elif not current_equipment.get('blinkers') and past_equipment.get('blinkers'):
            changes.append('Blinkers_Off')
            impact_score -= 5

        # Lasix (first time)
        if current_equipment.get('lasix') and not past_equipment.get('lasix'):
            changes.append('Lasix_First_Time')
            impact_score += 15  # First-time Lasix is powerful angle

        # Tongue tie
        if current_equipment.get('tongue_tie') and not past_equipment.get('tongue_tie'):
            changes.append('Tongue_Tie_Added')
            impact_score += 5

        return {
            'changes': changes,
            'impact_score': impact_score,
            'significant': len(changes) > 0
        }

    def calculate_distance_suitability(
        self,
        current_distance: float,
        past_performances: List[Dict]
    ) -> Dict[str, any]:
        """
        Calculate how suitable the distance is for the horse.

        Args:
            current_distance: Current race distance in furlongs
            past_performances: List of past performance dictionaries

        Returns:
            Dictionary with distance suitability metrics
        """
        if not past_performances:
            return {'suitability': 50, 'experience': False, 'best_distance': None}

        # Find performances at similar distances (within 1 furlong)
        similar_distance_races = [
            r for r in past_performances
            if abs(r.get('distance', 0) - current_distance) <= 1
        ]

        if similar_distance_races:
            # Calculate average finish at this distance
            avg_finish = np.mean([r.get('finish_position', 8) for r in similar_distance_races])

            if avg_finish <= 2:
                suitability = 90
            elif avg_finish <= 4:
                suitability = 75
            else:
                suitability = 60

            experience = True

            # Find best distance
            distance_performance = {}
            for race in past_performances:
                dist = race.get('distance', 6)
                finish = race.get('finish_position', 8)

                if dist not in distance_performance:
                    distance_performance[dist] = []
                distance_performance[dist].append(finish)

            best_distance = min(
                distance_performance.items(),
                key=lambda x: np.mean(x[1])
            )[0] if distance_performance else current_distance

        else:
            # No experience at this distance
            suitability = 60
            experience = False
            best_distance = None

            # Check if stretching out or cutting back
            avg_distance = np.mean([r.get('distance', 6) for r in past_performances])

            if current_distance > avg_distance + 1:
                suitability -= 10  # Stretching out
            elif current_distance < avg_distance - 1:
                suitability -= 5   # Cutting back

        return {
            'suitability': max(0, suitability),
            'experience': experience,
            'best_distance': best_distance,
            'races_at_distance': len(similar_distance_races)
        }

    def identify_bounce_candidates(
        self,
        past_performances: List[Dict]
    ) -> Dict[str, any]:
        """
        Identify horses likely to bounce (regress) after career-best effort.
        Helps avoid false favorites.

        Args:
            past_performances: List of past performance dictionaries

        Returns:
            Dictionary with bounce analysis
        """
        if len(past_performances) < 3:
            return {'bounce_risk': 50, 'reason': 'Insufficient data'}

        recent_race = past_performances[0]
        recent_speed = recent_race.get('speed_figure', 0)

        # Get average of races 2-5
        prior_races = past_performances[1:6]
        prior_avg = np.mean([r.get('speed_figure', 0) for r in prior_races])

        # Big improvement = bounce risk
        improvement = recent_speed - prior_avg

        if improvement >= 10:
            bounce_risk = 80
            reason = f'Career-best by {improvement:.1f} points - high bounce risk'
        elif improvement >= 6:
            bounce_risk = 65
            reason = f'Significant improvement of {improvement:.1f} points'
        elif improvement <= -5:
            bounce_risk = 30
            reason = 'Coming off subpar effort - bounce back candidate'
        else:
            bounce_risk = 50
            reason = 'Normal pattern'

        return {
            'bounce_risk': bounce_risk,
            'reason': reason,
            'last_figure': recent_speed,
            'avg_figure': round(prior_avg, 2),
            'improvement': round(improvement, 2)
        }

    def calculate_composite_form_score(
        self,
        class_rating: Dict,
        recency: Dict,
        recent_form: Dict,
        connections: Dict,
        distance_suit: Dict
    ) -> float:
        """
        Calculate composite form score from all form factors.

        Args:
            class_rating: Class rating dictionary
            recency: Recency rating dictionary
            recent_form: Recent form dictionary
            connections: Trainer/jockey rating dictionary
            distance_suit: Distance suitability dictionary

        Returns:
            Composite form score (0-100)
        """
        weights = {
            'class': 0.25,
            'recency': 0.15,
            'form': 0.30,
            'connections': 0.15,
            'distance': 0.15
        }

        composite = (
            class_rating.get('class_rating', 50) * weights['class'] +
            recency.get('recency_rating', 50) * weights['recency'] +
            recent_form.get('form_rating', 50) * weights['form'] +
            connections.get('connections_rating', 50) * weights['connections'] +
            distance_suit.get('suitability', 50) * weights['distance']
        )

        return round(composite, 2)
