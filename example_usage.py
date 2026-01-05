"""
THOROUGHBRED EDGE PRO - Example Usage
Demonstrates the three-model convergence system with sample race data
"""

from thoroughbred_edge_pro import ThoroughbredEdgePro


# Sample race data
race_data = {
    'distance': 8.5,  # 1 mile 1/16th (route race)
    'surface': 'dirt',
    'class_level': 'Allowance',
    'track_condition': 'fast',
    'horses': [
        {
            'name': 'Morning Glory',
            'post_position': 1,
            'odds': 2.5,  # Favorite
            'trainer': 'Bob Baffert',
            'jockey': 'J. Rosario',
            'days_since_last_race': 28,
            'current_equipment': {'blinkers': False, 'lasix': True},
            'past_equipment': {'blinkers': False, 'lasix': True},
            'trainer_stats': {'win_percentage': 22, 'roi': 0.85},
            'jockey_stats': {'win_percentage': 18, 'roi': 0.80},
            'past_performances': [
                {
                    'date': '2025-12-01',
                    'distance': 8,
                    'class_level': 'Allowance',
                    'speed_figure': 98,
                    'finish_position': 1,
                    'first_call_position': 2,
                    'field_size': 8
                },
                {
                    'date': '2025-11-05',
                    'distance': 8.5,
                    'class_level': 'Stakes',
                    'speed_figure': 95,
                    'finish_position': 2,
                    'first_call_position': 3,
                    'field_size': 9
                },
                {
                    'date': '2025-10-10',
                    'distance': 8,
                    'class_level': 'Allowance',
                    'speed_figure': 93,
                    'finish_position': 1,
                    'first_call_position': 2,
                    'field_size': 7
                }
            ]
        },
        {
            'name': 'Desert Storm',
            'post_position': 2,
            'odds': 5.0,
            'trainer': 'T. Pletcher',
            'jockey': 'I. Ortiz Jr.',
            'days_since_last_race': 35,
            'current_equipment': {'blinkers': True, 'lasix': True},
            'past_equipment': {'blinkers': False, 'lasix': True},
            'equipment_changes': True,
            'trainer_stats': {'win_percentage': 20, 'roi': 0.82},
            'jockey_stats': {'win_percentage': 19, 'roi': 0.85},
            'past_performances': [
                {
                    'date': '2025-11-25',
                    'distance': 8.5,
                    'class_level': 'Allowance',
                    'speed_figure': 91,
                    'finish_position': 3,
                    'first_call_position': 1,
                    'field_size': 8
                },
                {
                    'date': '2025-10-30',
                    'distance': 9,
                    'class_level': 'Stakes',
                    'speed_figure': 88,
                    'finish_position': 4,
                    'first_call_position': 2,
                    'field_size': 10
                },
                {
                    'date': '2025-10-01',
                    'distance': 8,
                    'class_level': 'Allowance',
                    'speed_figure': 90,
                    'finish_position': 2,
                    'first_call_position': 1,
                    'field_size': 7
                }
            ]
        },
        {
            'name': 'Silent Thunder',
            'post_position': 3,
            'odds': 12.0,  # Underdog
            'trainer': 'M. Maker',
            'jockey': 'J. Castellano',
            'days_since_last_race': 21,
            'current_equipment': {'blinkers': False, 'lasix': True},
            'past_equipment': {'blinkers': False, 'lasix': False},
            'equipment_changes': True,
            'trainer_stats': {'win_percentage': 15, 'roi': 0.95},
            'jockey_stats': {'win_percentage': 16, 'roi': 0.88},
            'past_performances': [
                {
                    'date': '2025-12-08',
                    'distance': 8.5,
                    'class_level': 'Claiming_High',
                    'speed_figure': 88,
                    'finish_position': 1,
                    'first_call_position': 6,
                    'field_size': 9
                },
                {
                    'date': '2025-11-15',
                    'distance': 9,
                    'class_level': 'Claiming_High',
                    'speed_figure': 86,
                    'finish_position': 2,
                    'first_call_position': 7,
                    'field_size': 10
                },
                {
                    'date': '2025-10-20',
                    'distance': 8,
                    'class_level': 'Claiming_Mid',
                    'speed_figure': 84,
                    'finish_position': 1,
                    'first_call_position': 8,
                    'field_size': 8
                },
                {
                    'date': '2025-09-28',
                    'distance': 8.5,
                    'class_level': 'Claiming_Mid',
                    'speed_figure': 82,
                    'finish_position': 3,
                    'first_call_position': 7,
                    'field_size': 9
                },
                {
                    'date': '2025-09-01',
                    'distance': 8,
                    'class_level': 'Claiming_Mid',
                    'speed_figure': 80,
                    'finish_position': 4,
                    'first_call_position': 6,
                    'field_size': 8
                }
            ]
        },
        {
            'name': 'Quick Strike',
            'post_position': 4,
            'odds': 4.0,
            'trainer': 'S. Asmussen',
            'jockey': 'R. Santana Jr.',
            'days_since_last_race': 42,
            'current_equipment': {'blinkers': True, 'lasix': True},
            'past_equipment': {'blinkers': True, 'lasix': True},
            'trainer_stats': {'win_percentage': 17, 'roi': 0.78},
            'jockey_stats': {'win_percentage': 15, 'roi': 0.76},
            'past_performances': [
                {
                    'date': '2025-11-18',
                    'distance': 6,
                    'class_level': 'Allowance',
                    'speed_figure': 92,
                    'finish_position': 1,
                    'first_call_position': 1,
                    'field_size': 7
                },
                {
                    'date': '2025-10-22',
                    'distance': 7,
                    'class_level': 'Allowance',
                    'speed_figure': 90,
                    'finish_position': 2,
                    'first_call_position': 1,
                    'field_size': 8
                },
                {
                    'date': '2025-09-30',
                    'distance': 6,
                    'class_level': 'Claiming_High',
                    'speed_figure': 88,
                    'finish_position': 1,
                    'first_call_position': 1,
                    'field_size': 6
                }
            ]
        },
        {
            'name': 'Midnight Runner',
            'post_position': 5,
            'odds': 15.0,  # Longshot
            'trainer': 'G. Motion',
            'jockey': 'M. Smith',
            'days_since_last_race': 18,
            'current_equipment': {'blinkers': True, 'lasix': True},
            'past_equipment': {'blinkers': False, 'lasix': True},
            'equipment_changes': True,
            'trainer_stats': {'win_percentage': 14, 'roi': 1.05},
            'jockey_stats': {'win_percentage': 14, 'roi': 0.92},
            'past_performances': [
                {
                    'date': '2025-12-10',
                    'distance': 8.5,
                    'class_level': 'Claiming_High',
                    'speed_figure': 87,
                    'finish_position': 2,
                    'first_call_position': 5,
                    'field_size': 10
                },
                {
                    'date': '2025-11-20',
                    'distance': 9,
                    'class_level': 'Claiming_High',
                    'speed_figure': 85,
                    'finish_position': 3,
                    'first_call_position': 6,
                    'field_size': 9
                },
                {
                    'date': '2025-10-28',
                    'distance': 8,
                    'class_level': 'Claiming_Mid',
                    'speed_figure': 83,
                    'finish_position': 1,
                    'first_call_position': 7,
                    'field_size': 8
                },
                {
                    'date': '2025-10-05',
                    'distance': 8.5,
                    'class_level': 'Claiming_Mid',
                    'speed_figure': 81,
                    'finish_position': 2,
                    'first_call_position': 6,
                    'field_size': 9
                }
            ]
        },
        {
            'name': 'Royal Champion',
            'post_position': 6,
            'odds': 8.0,
            'trainer': 'W. Mott',
            'jockey': 'J. Alvarado',
            'days_since_last_race': 25,
            'current_equipment': {'blinkers': False, 'lasix': True},
            'past_equipment': {'blinkers': False, 'lasix': True},
            'trainer_stats': {'win_percentage': 19, 'roi': 0.88},
            'jockey_stats': {'win_percentage': 16, 'roi': 0.82},
            'past_performances': [
                {
                    'date': '2025-12-03',
                    'distance': 8.5,
                    'class_level': 'Allowance',
                    'speed_figure': 90,
                    'finish_position': 3,
                    'first_call_position': 4,
                    'field_size': 8
                },
                {
                    'date': '2025-11-08',
                    'distance': 8,
                    'class_level': 'Allowance',
                    'speed_figure': 89,
                    'finish_position': 2,
                    'first_call_position': 5,
                    'field_size': 7
                },
                {
                    'date': '2025-10-15',
                    'distance': 9,
                    'class_level': 'Allowance',
                    'speed_figure': 87,
                    'finish_position': 4,
                    'first_call_position': 6,
                    'field_size': 10
                }
            ]
        }
    ]
}


def main():
    """Run example analysis."""
    print("\n" + "=" * 70)
    print("THOROUGHBRED EDGE PRO - Example Analysis")
    print("Three-Model Convergence System with Game Theory")
    print("=" * 70 + "\n")

    # Initialize system
    edge_pro = ThoroughbredEdgePro(track_takeout=0.17)

    # Analyze race
    print("Analyzing race...")
    race_analysis = edge_pro.analyze_race(race_data)

    # Find value bets
    print("Identifying value plays...")
    value_bets = edge_pro.find_value_bets(
        race_analysis,
        min_overlay=1.10,  # Looking for 10%+ overlay
        min_odds=3.0,      # Only horses 3-1 or higher
        max_odds=25.0,     # Avoid extreme longshots
        bankroll=1000
    )

    # Display results
    print("\n")
    print(edge_pro.display_analysis(value_bets, verbose=True))

    # Get underdog specials
    print("\n" + "=" * 70)
    print("UNDERDOG SPECIALS (8-1 or higher)")
    print("=" * 70)

    underdog_specials = edge_pro.get_underdog_specials(
        race_analysis,
        min_odds=8.0
    )

    if underdog_specials:
        for i, dog in enumerate(underdog_specials, 1):
            print(f"\n#{i} - {dog['horse']} @ {dog['odds']:.1f}-1")
            print(f"   True Win Probability: {dog['true_probability']:.2%}")
            print(f"   Pace Advantage: {dog['pace_advantage']:.1f}/100")
            print(f"   Key Angles:")
            for angle in dog['key_angles']:
                print(f"     - {angle}")
    else:
        print("\nNo underdog specials identified in this race.")

    print("\n" + "=" * 70)
    print("Analysis Complete")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
