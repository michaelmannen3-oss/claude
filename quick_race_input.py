"""
THOROUGHBRED EDGE PRO - Quick Race Analysis
Simplified data entry for analyzing real races
"""

from thoroughbred_edge_pro import ThoroughbredEdgePro


def quick_analyze():
    """
    Quick analysis with minimal data entry.
    Provide: Horse names, odds, and last 3 speed figures.
    """

    print("\n" + "="*80)
    print("THOROUGHBRED EDGE PRO - Quick Race Analyzer")
    print("="*80)
    print("\nTO USE THIS:")
    print("1. Get tomorrow's race card from DRF, Equibase, or your track")
    print("2. Edit the race_info and horses lists below")
    print("3. Run: python quick_race_input.py")
    print("\n" + "="*80 + "\n")

    # ==========================================================================
    # QUICK RACE SETUP - Edit these values
    # ==========================================================================

    race_info = {
        'track': 'Santa Anita',        # Track name
        'race_number': 5,               # Race number
        'distance': 8.5,                # Distance in furlongs
        'surface': 'dirt',              # dirt, turf, or synthetic
        'class_level': 'Allowance'      # Class level
    }

    # Simple horse list - just need: name, odds, last speed figures
    # Format: [name, odds, [last 3 speed figs], post, days_off, running_style]
    # Running style: 'E'=Early, 'EP'=Early Presser, 'P'=Presser, 'S'=Sustained, 'C'=Closer

    horses_simple = [
        # [Name, Odds, [Speed Figs], Post, Days Off, Style]
        ['Horse Name 1', 3.0, [92, 90, 88], 1, 28, 'E'],
        ['Horse Name 2', 5.0, [88, 87, 86], 2, 21, 'C'],
        ['Horse Name 3', 8.0, [85, 84, 83], 3, 35, 'S'],
        # Add more horses...
    ]

    # ==========================================================================
    # Convert simple format to full race data
    # ==========================================================================

    horses_full = []

    for horse_info in horses_simple:
        name, odds, speed_figs, post, days_off, style = horse_info

        # Estimate class and positions based on speed figures
        avg_fig = sum(speed_figs) / len(speed_figs)

        if avg_fig >= 100:
            class_level = 'Stakes'
        elif avg_fig >= 90:
            class_level = 'Allowance'
        elif avg_fig >= 80:
            class_level = 'Claiming_High'
        else:
            class_level = 'Claiming_Mid'

        # Create past performances from speed figures
        past_perfs = []
        for i, fig in enumerate(speed_figs):
            # Estimate finish position from figure
            if fig >= speed_figs[0] - 2:
                finish = 1 if i == 0 else 2
            elif fig >= speed_figs[0] - 5:
                finish = 3
            else:
                finish = 4

            # Estimate first call position based on running style
            style_positions = {
                'E': 1,
                'EP': 2,
                'P': 4,
                'S': 5,
                'C': 7
            }

            past_perfs.append({
                'date': f'2025-12-{15-i:02d}',
                'distance': race_info['distance'],
                'class_level': class_level,
                'speed_figure': fig,
                'finish_position': finish,
                'first_call_position': style_positions.get(style, 5),
                'field_size': 8,
                'surface': race_info['surface']
            })

        horses_full.append({
            'name': name,
            'post_position': post,
            'odds': odds,
            'trainer': 'Unknown',
            'jockey': 'Unknown',
            'days_since_last_race': days_off,
            'current_equipment': {'blinkers': False, 'lasix': True},
            'past_equipment': {'blinkers': False, 'lasix': True},
            'trainer_stats': {'win_percentage': 15, 'roi': 0.85},
            'jockey_stats': {'win_percentage': 15, 'roi': 0.85},
            'past_performances': past_perfs
        })

    race_data = {
        'distance': race_info['distance'],
        'surface': race_info['surface'],
        'class_level': race_info['class_level'],
        'track_condition': 'fast',
        'horses': horses_full
    }

    # ==========================================================================
    # Run Analysis
    # ==========================================================================

    print(f"\nAnalyzing {race_info['track']} - Race {race_info['race_number']}")
    print(f"{race_info['distance']} furlongs on {race_info['surface']}")
    print(f"Class: {race_info['class_level']}")
    print(f"Field: {len(horses_simple)} horses\n")

    edge_pro = ThoroughbredEdgePro()

    race_analysis = edge_pro.analyze_race(race_data)

    value_bets = edge_pro.find_value_bets(
        race_analysis,
        min_overlay=1.10,
        min_odds=3.0,
        max_odds=30.0,
        bankroll=1000
    )

    print(edge_pro.display_analysis(value_bets, verbose=True))


if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Edit the 'horses_simple' list above with your race data!")
    print("Then uncomment the line below and run again.\n")

    # Uncomment this line after adding your race data:
    # quick_analyze()
