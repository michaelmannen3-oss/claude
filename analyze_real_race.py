"""
THOROUGHBRED EDGE PRO - Real Race Analysis Template
Use this to analyze actual races with real data
"""

from thoroughbred_edge_pro import ThoroughbredEdgePro


def analyze_real_race():
    """
    Template for analyzing a real race.
    Fill in the data from tomorrow's race card and past performances.
    """

    # INSTRUCTIONS:
    # 1. Get tomorrow's race card from DRF, Equibase, or your track
    # 2. Fill in the race_data below with actual information
    # 3. For each horse, you need past performance data
    # 4. Run this script: python analyze_real_race.py

    # ============================================================================
    # RACE INFORMATION - Fill this in from the race card
    # ============================================================================

    race_data = {
        # Basic race info
        'distance': 8.5,              # Distance in furlongs (e.g., 6f, 8.5f, 10f)
        'surface': 'dirt',            # 'dirt', 'turf', or 'synthetic'
        'class_level': 'Allowance',   # Grade_1, Grade_2, Stakes, Allowance, Claiming_High, etc.
        'track_condition': 'fast',    # 'fast', 'good', 'muddy', 'sloppy'

        # ========================================================================
        # HORSES - Add each horse running in the race
        # ========================================================================

        'horses': [
            {
                # Horse #1 - FILL IN ACTUAL DATA
                'name': 'HORSE_NAME_HERE',
                'post_position': 1,
                'odds': 5.0,  # Morning line or current odds (e.g., 5.0 = 5-1)
                'trainer': 'Trainer Name',
                'jockey': 'Jockey Name',
                'days_since_last_race': 28,  # Days since last race
                'days_since_workout': 3,      # Days since last workout (optional)

                # Equipment
                'current_equipment': {
                    'blinkers': False,
                    'lasix': True,
                    'tongue_tie': False
                },

                'past_equipment': {
                    'blinkers': False,
                    'lasix': True,
                    'tongue_tie': False
                },

                # Trainer/Jockey stats (optional but helpful)
                'trainer_stats': {
                    'win_percentage': 18,  # Win % (e.g., 18%)
                    'roi': 0.85           # ROI (e.g., 0.85 = $0.85 return per $1)
                },

                'jockey_stats': {
                    'win_percentage': 16,
                    'roi': 0.80
                },

                # PAST PERFORMANCES - Most important data!
                # Include last 3-5 races minimum
                'past_performances': [
                    {
                        'date': '2025-12-01',           # Race date
                        'distance': 8,                   # Distance in furlongs
                        'class_level': 'Allowance',      # Class level
                        'speed_figure': 92,              # Speed figure (Beyer or equivalent)
                        'finish_position': 2,            # Where they finished (1=won)
                        'first_call_position': 3,        # Position at first call
                        'field_size': 8,                 # Number of horses in race
                        'surface': 'dirt'
                    },
                    {
                        'date': '2025-11-05',
                        'distance': 8.5,
                        'class_level': 'Claiming_High',
                        'speed_figure': 88,
                        'finish_position': 1,
                        'first_call_position': 5,
                        'field_size': 9,
                        'surface': 'dirt'
                    },
                    {
                        'date': '2025-10-10',
                        'distance': 8,
                        'class_level': 'Claiming_High',
                        'speed_figure': 85,
                        'finish_position': 3,
                        'first_call_position': 6,
                        'field_size': 8,
                        'surface': 'dirt'
                    },
                    # Add more past races...
                ]
            },

            # Horse #2 - Copy the structure above and fill in for each horse
            {
                'name': 'SECOND_HORSE_NAME',
                'post_position': 2,
                'odds': 8.0,
                'trainer': 'Trainer Name',
                'jockey': 'Jockey Name',
                'days_since_last_race': 21,
                'current_equipment': {'blinkers': True, 'lasix': True},
                'past_equipment': {'blinkers': False, 'lasix': False},
                'equipment_changes': True,  # Set to True if equipment changed
                'trainer_stats': {'win_percentage': 15, 'roi': 0.90},
                'jockey_stats': {'win_percentage': 14, 'roi': 0.85},
                'past_performances': [
                    # Add past races here...
                ]
            },

            # Add more horses - copy the structure above
            # You need data for ALL horses in the race for accurate pace analysis
        ]
    }

    # ============================================================================
    # RUN THE ANALYSIS
    # ============================================================================

    print("\n" + "="*80)
    print("THOROUGHBRED EDGE PRO - Real Race Analysis")
    print("="*80 + "\n")

    # Initialize system
    edge_pro = ThoroughbredEdgePro(track_takeout=0.17)  # Adjust takeout if needed

    # Analyze the race
    print("Analyzing race with three-model convergence...")
    race_analysis = edge_pro.analyze_race(race_data)

    # Find value bets
    print("Identifying value plays...\n")
    value_bets = edge_pro.find_value_bets(
        race_analysis,
        min_overlay=1.10,      # Require 10% overlay minimum
        min_odds=3.0,          # Only consider horses 3-1 or higher
        max_odds=50.0,         # Avoid extreme longshots
        bankroll=1000          # Adjust to your actual bankroll
    )

    # Display full analysis
    print(edge_pro.display_analysis(value_bets, verbose=True))

    # Show underdog specials
    print("\n" + "="*80)
    print("UNDERDOG SPECIALS (8-1 or higher)")
    print("="*80)

    underdogs = edge_pro.get_underdog_specials(race_analysis, min_odds=8.0)

    if underdogs:
        for i, dog in enumerate(underdogs, 1):
            print(f"\n#{i} - {dog['horse']} @ {dog['odds']:.1f}-1")
            print(f"   True Win Probability: {dog['true_probability']:.2%}")
            print(f"   Pace Advantage: {dog['pace_advantage']:.1f}/100")
            if dog['key_angles']:
                print(f"   Key Angles:")
                for angle in dog['key_angles']:
                    print(f"     - {angle}")
    else:
        print("\nNo underdog specials identified in this race.")

    print("\n" + "="*80)
    print("Analysis Complete")
    print("="*80 + "\n")


# ============================================================================
# DATA SOURCES - Where to get the information you need
# ============================================================================

INSTRUCTIONS = """
WHERE TO GET RACE DATA:

1. RACE CARDS (Basic Info):
   - Daily Racing Form (DRF): www.drf.com
   - Equibase: www.equibase.com
   - TrackMaster: www.trackmaster.com
   - Your local track website

2. PAST PERFORMANCES:
   - DRF Past Performances (PP's)
   - Equibase Past Performances
   - Brisnet.com
   - TimeformUS

3. SPEED FIGURES:
   - Beyer Speed Figures (in DRF)
   - Bris Speed Ratings
   - TimeformUS figures
   - Equibase Speed Figures

4. CURRENT ODDS:
   - Live odds from track tote board
   - Morning line odds (from race card)
   - Online ADW platforms (TVG, TwinSpires, etc.)

MINIMUM DATA REQUIRED FOR EACH HORSE:
✓ Name, post position, odds
✓ Last 3 races minimum (more is better)
✓ Speed figures from past races
✓ Finish positions and field sizes
✓ Current class level and distance

OPTIONAL BUT HELPFUL:
✓ Trainer/jockey statistics
✓ Equipment changes
✓ Days since last race
✓ Running positions during races

TIPS:
- More past performance data = better analysis
- Speed figures are critical - use consistent scale
- Accurate odds are important for value detection
- Include all horses in the race for pace analysis
"""


if __name__ == "__main__":
    print(INSTRUCTIONS)
    print("\n" + "="*80)
    print("NOTE: This template has placeholder data.")
    print("Edit this file and fill in real race data, then run it again.")
    print("="*80 + "\n")

    # Uncomment the line below once you've filled in real data
    # analyze_real_race()
