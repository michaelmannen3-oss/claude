"""
THOROUGHBRED EDGE PRO - FanDuel Racing Data Parser
Easy copy-paste from FanDuel Racing to instant analysis
"""

from thoroughbred_edge_pro import ThoroughbredEdgePro


def analyze_fanduel_race():
    """
    Analyze a race from FanDuel Racing.

    HOW TO USE:
    1. Go to FanDuel Racing website (racing.fanduel.com)
    2. Pick a race you want to analyze
    3. Copy the race information below
    4. Run this script: python fanduel_analyzer.py
    """

    # =========================================================================
    # STEP 1: Go to racing.fanduel.com and find a race
    # =========================================================================

    print("\n" + "="*80)
    print("THOROUGHBRED EDGE PRO - FanDuel Racing Analysis")
    print("="*80)
    print("\nTo analyze a FanDuel race:")
    print("1. Open: https://racing.fanduel.com")
    print("2. Browse races for today/tomorrow")
    print("3. Click on a race to see entries")
    print("4. Look for:")
    print("   - Horse names and post positions")
    print("   - Morning line odds (or current odds)")
    print("   - Past performance tab for speed figures")
    print("5. Fill in the data below")
    print("="*80 + "\n")

    # =========================================================================
    # STEP 2: Fill in this race information from FanDuel
    # =========================================================================

    race_info = {
        'track': 'Gulfstream Park',      # Track name from FanDuel
        'race_number': 5,                 # Race number
        'post_time': '3:45 PM',          # Post time
        'distance': 8.5,                  # Distance in furlongs
        'surface': 'dirt',                # dirt, turf, synthetic
        'class_level': 'Allowance',       # Class (Maiden, Claiming, Allowance, Stakes, Graded)
    }

    # =========================================================================
    # STEP 3: Copy horse data from FanDuel entries
    # =========================================================================

    # SIMPLE FORMAT - Just need basics from FanDuel:
    # Format: [Post, Name, ML Odds, Trainer, Jockey, Last 3 Beyer Figs]

    horses_from_fanduel = [
        # Example entries - REPLACE WITH REAL DATA FROM FANDUEL:
        [1, 'Horse Name Here', 3.5, 'Todd Pletcher', 'I. Ortiz Jr', [88, 86, 84]],
        [2, 'Another Horse', 12.0, 'Brad Cox', 'J. Rosario', [82, 80, 78]],
        [3, 'Third Horse', 8.0, 'Chad Brown', 'J. Castellano', [85, 83, 81]],
        # Add all horses from the FanDuel race card here...
    ]

    # =========================================================================
    # STEP 4: (OPTIONAL) Add detailed past performances if you have them
    # =========================================================================

    # If you click "Past Performances" on FanDuel, you can get more detail:
    detailed_pp = {
        'Horse Name Here': {
            'last_race_date': '2025-12-15',
            'days_since_last': 21,
            'running_style': 'C',  # E=Early, EP=Early Presser, P=Presser, S=Sustained, C=Closer
            'equipment': 'L',  # L=Lasix, B=Blinkers, etc.
            'past_races': [
                {'date': '2025-12-15', 'dist': 8, 'beyer': 88, 'finish': 2, 'class': 'Allowance'},
                {'date': '2025-11-20', 'dist': 8.5, 'beyer': 86, 'finish': 1, 'class': 'Claiming_High'},
                {'date': '2025-10-28', 'dist': 8, 'beyer': 84, 'finish': 3, 'class': 'Claiming_High'},
            ]
        },
        # Add more horses if you want detailed analysis...
    }

    # =========================================================================
    # AUTO-CONVERT TO THOROUGHBRED EDGE PRO FORMAT
    # =========================================================================

    horses_full = []

    for horse_data in horses_from_fanduel:
        post, name, odds, trainer, jockey, beyer_figs = horse_data

        # Determine running style from speed figures and position
        # (Can be overridden if you have detailed_pp data)
        if name in detailed_pp:
            style = detailed_pp[name].get('running_style', 'P')
            days_off = detailed_pp[name].get('days_since_last', 28)
            past_races = detailed_pp[name].get('past_races', [])
        else:
            style = 'P'  # Default to Presser
            days_off = 28
            past_races = []

        # Create past performances from Beyer figures
        if not past_races:
            for i, beyer in enumerate(beyer_figs):
                past_races.append({
                    'date': f'2025-12-{20-i*10:02d}',
                    'distance': race_info['distance'],
                    'class_level': race_info['class_level'],
                    'speed_figure': beyer,
                    'finish_position': 1 if i == 0 else 2,
                    'first_call_position': 3 if style in ['E', 'EP'] else 6,
                    'field_size': 8,
                    'surface': race_info['surface']
                })
        else:
            # Convert detailed races to standard format
            formatted_races = []
            for race in past_races:
                formatted_races.append({
                    'date': race.get('date', '2025-12-01'),
                    'distance': race.get('dist', race_info['distance']),
                    'class_level': race.get('class', race_info['class_level']),
                    'speed_figure': race.get('beyer', 85),
                    'finish_position': race.get('finish', 2),
                    'first_call_position': race.get('first_call', 4),
                    'field_size': race.get('field', 8),
                    'surface': race_info['surface']
                })
            past_races = formatted_races

        horses_full.append({
            'name': name,
            'post_position': post,
            'odds': odds,
            'trainer': trainer,
            'jockey': jockey,
            'days_since_last_race': days_off,
            'current_equipment': {'blinkers': False, 'lasix': True},
            'past_equipment': {'blinkers': False, 'lasix': True},
            'trainer_stats': {'win_percentage': 15, 'roi': 0.85},
            'jockey_stats': {'win_percentage': 15, 'roi': 0.82},
            'past_performances': past_races
        })

    race_data = {
        'distance': race_info['distance'],
        'surface': race_info['surface'],
        'class_level': race_info['class_level'],
        'track_condition': 'fast',
        'horses': horses_full
    }

    # =========================================================================
    # RUN THOROUGHBRED EDGE PRO ANALYSIS
    # =========================================================================

    print(f"\n{'='*80}")
    print(f"ANALYZING: {race_info['track']} - Race {race_info['race_number']}")
    print(f"Post Time: {race_info['post_time']}")
    print(f"Distance: {race_info['distance']} furlongs on {race_info['surface']}")
    print(f"Class: {race_info['class_level']}")
    print(f"Field: {len(horses_from_fanduel)} horses")
    print(f"{'='*80}\n")

    # Initialize THOROUGHBRED EDGE PRO
    edge_pro = ThoroughbredEdgePro(track_takeout=0.17)

    # Analyze race
    print("Running three-model convergence analysis...")
    race_analysis = edge_pro.analyze_race(race_data)

    # Find value plays
    print("Identifying value plays with game theory...\n")
    value_bets = edge_pro.find_value_bets(
        race_analysis,
        min_overlay=1.10,      # 10% minimum overlay
        min_odds=3.0,          # Only 3-1 or higher
        max_odds=50.0,         # Max 50-1
        bankroll=1000          # Adjust to your bankroll
    )

    # Display results
    print(edge_pro.display_analysis(value_bets, verbose=True))

    # Show underdog specials
    underdogs = edge_pro.get_underdog_specials(race_analysis, min_odds=8.0)

    if underdogs:
        print("\n" + "="*80)
        print("UNDERDOG SPECIALS (8-1 or higher)")
        print("="*80)
        for i, dog in enumerate(underdogs, 1):
            print(f"\n#{i} - {dog['horse']} @ {dog['odds']:.1f}-1")
            print(f"   True Win Probability: {dog['true_probability']:.2%}")
            print(f"   Pace Advantage: {dog['pace_advantage']:.1f}/100")
            if dog['key_angles']:
                print(f"   Key Angles:")
                for angle in dog['key_angles']:
                    print(f"     - {angle}")

    print("\n" + "="*80)
    print("Analysis Complete - Ready to bet on FanDuel Racing!")
    print("="*80 + "\n")


# =============================================================================
# FANDUEL RACING - WHERE TO FIND THE DATA
# =============================================================================

FANDUEL_GUIDE = """
╔════════════════════════════════════════════════════════════════════════════╗
║                   FANDUEL RACING DATA COLLECTION GUIDE                     ║
╚════════════════════════════════════════════════════════════════════════════╝

STEP-BY-STEP:

1. Go to: https://racing.fanduel.com

2. Click "RACETRACKS" at the top

3. Browse upcoming races:
   - Shows all tracks running today/tomorrow
   - Click on any race to see entries

4. On the race page, you'll see:
   ✓ Post positions and horse names
   ✓ Morning line odds (ML column)
   ✓ Trainer and jockey names
   ✓ Click "PAST PERFORMANCES" for speed figures

5. For each horse, note:
   - Post position (#)
   - Horse name
   - ML odds (or current odds if live)
   - Last 3 Beyer Speed Figures (from PP tab)
   - Trainer/Jockey names

6. Enter data in horses_from_fanduel list above

7. Run: python fanduel_analyzer.py

════════════════════════════════════════════════════════════════════════════

FANDUEL RACING TRACKS (Examples):

Today's popular tracks:
  - Gulfstream Park (Florida)
  - Santa Anita (California)
  - Aqueduct (New York)
  - Fair Grounds (Louisiana)
  - Oaklawn Park (Arkansas)
  - Tampa Bay Downs (Florida)

Check FanDuel Racing for full schedule!

════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(FANDUEL_GUIDE)

    print("\n⚠️  Edit the 'horses_from_fanduel' list above with real FanDuel data!")
    print("Then uncomment the line below and run again.\n")

    # Uncomment this line after adding FanDuel race data:
    # analyze_fanduel_race()
