"""
THOROUGHBRED EDGE PRO - Interactive App Demo
Visual interface showing the three-model convergence system
"""

from thoroughbred_edge_pro import ThoroughbredEdgePro
import time


def print_header():
    """Print application header."""
    print("\n" * 2)
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "THOROUGHBRED EDGE PRO" + " " * 37 + "█")
    print("█" + " " * 15 + "Three-Model Convergence System v1.0" + " " * 30 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print()


def print_section(title):
    """Print section header."""
    print("\n" + "─" * 80)
    print(f"  {title}")
    print("─" * 80)


def print_horse_card(horse, rank=None):
    """Print detailed horse analysis card."""
    prefix = f"#{rank} " if rank else ""

    print(f"\n┌{'─' * 78}┐")
    print(f"│ {prefix}{horse['name']:40} Post {horse['post_position']}  |  Odds: {horse['odds']:.1f}-1{' ' * 10}│")
    print(f"├{'─' * 78}┤")

    # Model Scores
    print(f"│ MODEL SCORES:                                                              │")
    print(f"│   🏃 Speed Model:  {horse['speed_score']:5.1f}/100  [{create_bar(horse['speed_score'])}]   │")
    print(f"│   ⚡ Pace Model:   {horse['pace_score']:5.1f}/100  [{create_bar(horse['pace_score'])}]   │")
    print(f"│   📊 Form Model:   {horse['form_score']:5.1f}/100  [{create_bar(horse['form_score'])}]   │")

    # Value Metrics
    if 'true_probability' in horse:
        implied_prob = 1 / (horse['odds'] + 1)
        print(f"├{'─' * 78}┤")
        print(f"│ VALUE ANALYSIS:                                                            │")
        print(f"│   True Win %:     {horse['true_probability']*100:5.2f}%                                                    │")
        print(f"│   Implied Win %:  {implied_prob*100:5.2f}%                                                    │")

        if 'expected_value' in horse and horse['expected_value'] > 0:
            print(f"│   Expected Value: +{horse['expected_value']:.3f}  ✓ POSITIVE VALUE                         │")
            print(f"│   Overlay:        {horse['overlay']:.1f}%  ⭐                                               │")

    # Running Style & Pace
    if 'running_style' in horse:
        style = horse['running_style']
        print(f"├{'─' * 78}┤")
        print(f"│ RUNNING STYLE: {style['style']:30} ({style['style_code']})                    │")
        if 'pace_advantage' in horse:
            adv_indicator = "✓✓✓" if horse['pace_advantage'] >= 70 else "✓✓" if horse['pace_advantage'] >= 60 else "✓"
            print(f"│ Pace Advantage:   {horse['pace_advantage']:.1f}/100  {adv_indicator}                                          │")

    # Key Angles
    if horse.get('angles'):
        print(f"├{'─' * 78}┤")
        print(f"│ 🎯 KEY ANGLES:                                                             │")
        for angle in horse['angles'][:4]:
            print(f"│   • {angle:72} │")

    # Connections
    if 'connections' in horse:
        conn = horse['connections']
        print(f"├{'─' * 78}┤")
        print(f"│ CONNECTIONS:                                                               │")
        print(f"│   Trainer Rating: {conn['trainer_rating']:.1f}/100                                               │")
        print(f"│   Jockey Rating:  {conn['jockey_rating']:.1f}/100                                               │")

    print(f"└{'─' * 78}┘")


def create_bar(value, max_val=100, width=20):
    """Create a visual bar for scores."""
    filled = int((value / max_val) * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar


def print_race_overview(race_analysis):
    """Print race overview."""
    info = race_analysis['race_info']
    pace = race_analysis['pace_scenario']
    bias = race_analysis['favorite_bias']

    print("\n┌" + "─" * 78 + "┐")
    print("│ RACE OVERVIEW                                                              │")
    print("├" + "─" * 78 + "┤")
    print(f"│ Distance:      {info['distance']:.1f} furlongs ({get_distance_name(info['distance'])})                       │")
    print(f"│ Surface:       {info['surface'].upper():20}                                        │")
    print(f"│ Class:         {info['class_level']:20}                                        │")
    print(f"│ Field Size:    {race_analysis['field_size']} horses                                                      │")
    print("├" + "─" * 78 + "┤")
    print("│ PACE SCENARIO                                                              │")
    print(f"│ Type:          {pace['scenario']:20}  {get_pace_emoji(pace['scenario'])}                              │")
    print(f"│ Pressure:      {pace['pace_pressure']:.1f}/100  [{create_bar(pace['pace_pressure'])}]   │")
    print(f"│ Early Speed:   {pace['early_speed_count']} horses                                                     │")
    print(f"│ Closers:       {pace['closer_count']} horses                                                     │")
    print(f"│ Advantages:    {', '.join(pace['advantages'])}                                             │")
    print("├" + "─" * 78 + "┤")
    print("│ CROWD PSYCHOLOGY                                                           │")
    print(f"│ Bias Type:     {bias['bias']:30}                            │")
    print(f"│ Severity:      {bias['severity']}/100                                                   │")
    print(f"│ Longshot Opps: {bias['longshot_opportunities']} horses                                                     │")
    print("└" + "─" * 78 + "┘")


def get_distance_name(furlongs):
    """Get common name for distance."""
    if furlongs <= 5.5:
        return "Sprint"
    elif furlongs <= 7:
        return "One Turn Mile"
    elif furlongs <= 9:
        return "Route"
    else:
        return "Marathon"


def get_pace_emoji(scenario):
    """Get emoji for pace scenario."""
    emojis = {
        'Hot Pace': '🔥',
        'Slow Pace': '🐌',
        'Honest Pace': '⚖️',
        'Closer-Heavy': '🏃'
    }
    return emojis.get(scenario, '📊')


def print_value_summary(value_analysis):
    """Print value betting summary."""
    value_plays = value_analysis['value_plays']
    strategy = value_analysis['strategy']
    sim = value_analysis['simulation']

    print("\n┌" + "─" * 78 + "┐")
    print("│ 💰 VALUE BETTING SUMMARY                                                   │")
    print("├" + "─" * 78 + "┤")
    print(f"│ Value Plays Found:    {len(value_plays)}                                                       │")
    print(f"│ Recommended Action:   {strategy['action']:20}                                    │")

    if strategy['bets']:
        print(f"│ Total Risk:           ${strategy['total_risk']:7.2f}  ({strategy['risk_percentage']:.1f}% of bankroll)                │")
        print("├" + "─" * 78 + "┤")
        print("│ SIMULATION RESULTS (10,000 races)                                          │")
        print(f"│ Expected ROI:         {sim['roi']:7.2f}%  {'🚀' if sim['roi'] > 100 else '✓'}                                        │")
        print(f"│ Win Rate:             {sim['win_rate']:7.2f}%                                                │")
        print(f"│ Profit Factor:        {sim['profit_factor']:7.2f}                                                  │")

    print("└" + "─" * 78 + "┘")


def print_betting_tickets(strategy):
    """Print betting recommendations as tickets."""
    if not strategy.get('bets'):
        print("\n  No qualifying bets for this race.\n")
        return

    print("\n" + "═" * 80)
    print("  💵 RECOMMENDED BETS")
    print("═" * 80)

    for i, bet in enumerate(strategy['bets'], 1):
        print(f"\n  TICKET #{i}")
        print(f"  ┌{'─' * 76}┐")
        print(f"  │ Horse:            {bet['horse']:40}            │")
        print(f"  │ Odds:             {bet['odds']:.1f}-1                                                │")
        print(f"  │ Bet Amount:       ${bet['bet_amount']:7.2f}                                          │")
        print(f"  │ Potential Win:    ${bet['bet_amount'] * bet['odds']:7.2f}                                          │")
        print(f"  │ Expected Profit:  ${bet['expected_profit']:7.2f}                                          │")
        print(f"  │ Overlay Edge:     {bet['overlay']:.1f}%                                              │")
        print(f"  └{'─' * 76}┘")


def run_app():
    """Run the interactive app demo."""
    print_header()

    print("  Loading race data...")
    time.sleep(0.5)

    # Load sample race data
    from example_usage import race_data

    print("  Initializing THOROUGHBRED EDGE PRO...")
    time.sleep(0.5)

    edge_pro = ThoroughbredEdgePro(track_takeout=0.17)

    print("  Analyzing race with three-model convergence...")
    time.sleep(0.8)

    race_analysis = edge_pro.analyze_race(race_data)

    print("  Running game theory analysis...")
    time.sleep(0.6)

    value_bets = edge_pro.find_value_bets(
        race_analysis,
        min_overlay=1.10,
        min_odds=3.0,
        max_odds=25.0,
        bankroll=1000
    )

    print("  ✓ Analysis Complete!\n")
    time.sleep(0.3)

    # Display race overview
    print_section("📋 RACE ANALYSIS")
    print_race_overview(race_analysis)

    # Display value summary
    print_value_summary(value_bets)

    # Display top value plays
    print_section("⭐ TOP VALUE PLAYS")

    for i, play in enumerate(value_bets['value_plays'][:3], 1):
        # Find full horse data
        horse = next((h for h in race_analysis['horses'] if h['name'] == play['horse']), None)
        if horse:
            # Merge value play data into horse data
            horse.update({
                'expected_value': play['expected_value'],
                'overlay': play['overlay']
            })
            print_horse_card(horse, rank=i)

    # Display betting tickets
    print_section("🎫 BETTING RECOMMENDATIONS")
    print_betting_tickets(value_bets['strategy'])

    # Display all horses (abbreviated)
    print_section("🏇 COMPLETE FIELD ANALYSIS")

    # Sort by odds
    all_horses = sorted(race_analysis['horses'], key=lambda x: x['odds'])

    print(f"\n{'#':<3} {'Horse':<25} {'Odds':<8} {'Speed':<7} {'Pace':<7} {'Form':<7} {'Value':<8}")
    print("─" * 80)

    for i, horse in enumerate(all_horses, 1):
        value_indicator = "⭐" if horse.get('expected_value', 0) > 1 else "✓" if horse.get('expected_value', 0) > 0 else ""
        print(f"{i:<3} {horse['name']:<25} {horse['odds']:>5.1f}-1  {horse['speed_score']:>5.1f}  {horse['pace_score']:>6.1f}  {horse['form_score']:>6.1f}  {value_indicator:<8}")

    # Footer
    print("\n" + "═" * 80)
    print("  THOROUGHBRED EDGE PRO v1.0.0 - Game Theory Racing Analysis")
    print("  Emphasis on Underdogs | Three-Model Convergence | Value Identification")
    print("═" * 80 + "\n")


if __name__ == "__main__":
    run_app()
