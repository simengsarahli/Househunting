#!/usr/bin/env python3
"""
House Search Agent - Finds towns matching your criteria for commuting to NYC.

Usage:
    python3 search_agent.py                  # Run with default criteria
    python3 search_agent.py --max-price 1500000 --max-tax 20000
    python3 search_agent.py --sort school    # Sort by school rating
    python3 search_agent.py --sort price     # Sort by price (ascending)
    python3 search_agent.py --sort commute   # Sort by commute time
    python3 search_agent.py --sort tax       # Sort by property tax
    python3 search_agent.py --state NJ       # Filter by state
    python3 search_agent.py --top 5          # Show top N results only
    python3 search_agent.py --detail Summit  # Detailed view of a specific town
"""

import argparse
import sys

from tabulate import tabulate

from config import SEARCH_CRITERIA
from towns_data import TOWNS


def filter_towns(
    towns: list[dict],
    max_price: int | None = None,
    max_tax: int | None = None,
    max_commute: int | None = None,
    min_school: float | None = None,
    state: str | None = None,
) -> list[dict]:
    """Filter towns based on search criteria."""
    results = []
    for town in towns:
        if max_price and town["price_range_high"] < max_price * 0.5:
            # Include towns where at least some homes are in budget
            pass
        if max_price and town["price_range_low"] > max_price:
            continue
        if max_tax and town["avg_property_tax"] > max_tax:
            continue
        if max_commute and town["commute_minutes"] > max_commute:
            continue
        if min_school and town["avg_school_rating"] < min_school:
            continue
        if state and town["state"].upper() != state.upper():
            continue
        results.append(town)
    return results


def sort_towns(towns: list[dict], sort_by: str = "score") -> list[dict]:
    """Sort towns by the given criteria."""
    sort_keys = {
        "school": lambda t: -t["avg_school_rating"],
        "price": lambda t: t["median_home_price"],
        "commute": lambda t: t["commute_minutes"],
        "tax": lambda t: t["avg_property_tax"],
        "score": lambda t: -compute_score(t),
    }
    key_fn = sort_keys.get(sort_by, sort_keys["score"])
    return sorted(towns, key=key_fn)


def compute_score(town: dict) -> float:
    """
    Compute a composite score (0-100) balancing all criteria.

    Weights:
    - School quality: 35%
    - Commute time: 25%
    - Price affordability: 20%
    - Tax affordability: 20%
    """
    criteria = SEARCH_CRITERIA

    # School score: 0-100 (rating out of 10 -> percentage)
    school_score = (town["avg_school_rating"] / 10) * 100

    # Commute score: 0-100 (lower commute = higher score)
    max_commute = criteria["max_commute_minutes"]
    commute_score = max(0, (max_commute - town["commute_minutes"]) / max_commute * 100)

    # Price score: 0-100 (lower median price relative to budget = higher score)
    max_price = criteria["max_price"]
    price_score = max(0, (max_price - town["median_home_price"]) / max_price * 100)

    # Tax score: 0-100 (lower tax = higher score)
    max_tax = criteria["max_property_tax"]
    tax_score = max(0, (max_tax - town["avg_property_tax"]) / max_tax * 100)

    return (
        school_score * 0.35
        + commute_score * 0.25
        + price_score * 0.20
        + tax_score * 0.20
    )


def format_currency(amount: int) -> str:
    """Format integer as currency string."""
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    return f"${amount:,.0f}"


def print_summary_table(towns: list[dict]) -> None:
    """Print a summary table of matching towns."""
    headers = [
        "Rank",
        "Town",
        "State",
        "Score",
        "Commute",
        "School\nRating",
        "Median\nPrice",
        "Price\nRange",
        "Avg Tax\n(/yr)",
        "Transit",
    ]

    rows = []
    for i, town in enumerate(towns, 1):
        rows.append([
            i,
            town["name"],
            town["state"],
            f"{compute_score(town):.0f}/100",
            f"{town['commute_minutes']} min",
            f"{town['avg_school_rating']}/10",
            format_currency(town["median_home_price"]),
            f"{format_currency(town['price_range_low'])}-{format_currency(town['price_range_high'])}",
            format_currency(town["avg_property_tax"]),
            town["transit_line"].split("(")[0].strip(),
        ])

    print(tabulate(rows, headers=headers, tablefmt="rounded_grid", stralign="center"))


def print_detail(town: dict) -> None:
    """Print detailed information about a specific town."""
    score = compute_score(town)
    print(f"\n{'=' * 60}")
    print(f"  {town['name']}, {town['state']} ({town['county']} County)")
    print(f"  Composite Score: {score:.0f}/100")
    print(f"{'=' * 60}")

    print(f"\n  COMMUTE")
    print(f"    Train to Midtown: {town['commute_minutes']} minutes")
    print(f"    Transit line:     {town['transit_line']}")

    print(f"\n  PRICING")
    print(f"    Median price:     {format_currency(town['median_home_price'])}")
    print(f"    Typical range:    {format_currency(town['price_range_low'])} - {format_currency(town['price_range_high'])}")
    print(f"    Avg property tax: {format_currency(town['avg_property_tax'])}/year")
    print(f"    Eff. tax rate:    {town['tax_rate_pct']:.2f}%")

    print(f"\n  SCHOOLS (GreatSchools rating, 1-10)")
    print(f"    Elementary:       {town['elementary_school_rating']}/10")
    print(f"    Middle:           {town['middle_school_rating']}/10")
    print(f"    High:             {town['high_school_rating']}/10")
    print(f"    Average:          {town['avg_school_rating']}/10")
    print(f"    Notable schools:")
    for school in town["notable_schools"]:
        print(f"      - {school}")

    print(f"\n  HIGHLIGHTS")
    for highlight in town["highlights"]:
        print(f"    - {highlight}")

    # Price analysis relative to budget
    budget = SEARCH_CRITERIA["max_price"]
    if town["median_home_price"] <= budget * 0.7:
        affordability = "Well within budget"
    elif town["median_home_price"] <= budget * 0.9:
        affordability = "Comfortably in budget"
    elif town["median_home_price"] <= budget:
        affordability = "At budget limit - limited inventory"
    else:
        affordability = "Over budget for median home - look for below-median options"

    print(f"\n  BUDGET ANALYSIS (vs ${budget:,.0f} budget)")
    print(f"    Affordability: {affordability}")
    print(f"    Homes under budget: {'Many options' if town['price_range_low'] < budget * 0.6 else 'Some options' if town['price_range_low'] < budget else 'Limited'}")
    print()


def print_search_summary(criteria: dict) -> None:
    """Print the active search criteria."""
    print("\n" + "=" * 60)
    print("  HOUSE SEARCH AGENT - NYC Commuter Towns")
    print("=" * 60)
    print(f"  Max price:      {format_currency(criteria['max_price'])}")
    print(f"  Max property tax: {format_currency(criteria['max_property_tax'])}/year")
    print(f"  Max commute:    {criteria['max_commute_minutes']} min to {criteria['commute_destination']}")
    print(f"  Min school:     {criteria['min_school_rating']}/10 (GreatSchools)")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="House Search Agent for NYC commuters")
    parser.add_argument("--max-price", type=int, help="Maximum home price")
    parser.add_argument("--max-tax", type=int, help="Maximum annual property tax")
    parser.add_argument("--max-commute", type=int, help="Maximum commute time (minutes)")
    parser.add_argument("--min-school", type=float, help="Minimum school rating (1-10)")
    parser.add_argument("--state", type=str, help="Filter by state (NJ, NY, CT)")
    parser.add_argument(
        "--sort",
        choices=["score", "school", "price", "commute", "tax"],
        default="score",
        help="Sort results by criteria (default: composite score)",
    )
    parser.add_argument("--top", type=int, help="Show only top N results")
    parser.add_argument("--detail", type=str, help="Show detailed info for a specific town")
    parser.add_argument("--all-details", action="store_true", help="Show detailed view for all matching towns")

    args = parser.parse_args()

    # Merge CLI args with config defaults
    criteria = SEARCH_CRITERIA.copy()
    if args.max_price:
        criteria["max_price"] = args.max_price
    if args.max_tax:
        criteria["max_property_tax"] = args.max_tax
    if args.max_commute:
        criteria["max_commute_minutes"] = args.max_commute
    if args.min_school:
        criteria["min_school_rating"] = args.min_school

    # Detail view for a single town
    if args.detail:
        matches = [t for t in TOWNS if args.detail.lower() in t["name"].lower()]
        if not matches:
            print(f"No town found matching '{args.detail}'")
            sys.exit(1)
        for town in matches:
            print_detail(town)
        return

    print_search_summary(criteria)

    # Filter and sort
    results = filter_towns(
        TOWNS,
        max_price=criteria["max_price"],
        max_tax=criteria["max_property_tax"],
        max_commute=criteria["max_commute_minutes"],
        min_school=criteria["min_school_rating"],
        state=args.state,
    )

    if not results:
        print("No towns match all your criteria. Try relaxing some constraints.")
        sys.exit(0)

    results = sort_towns(results, args.sort)

    if args.top:
        results = results[: args.top]

    print(f"Found {len(results)} towns matching your criteria:\n")
    print_summary_table(results)

    # Print top 3 recommendations
    top3 = results[:3]
    print(f"\n{'=' * 60}")
    print("  TOP RECOMMENDATIONS")
    print(f"{'=' * 60}")
    for i, town in enumerate(top3, 1):
        score = compute_score(town)
        print(f"\n  #{i}: {town['name']}, {town['state']} (Score: {score:.0f}/100)")
        print(f"      {town['commute_minutes']} min commute | Schools: {town['avg_school_rating']}/10 | "
              f"Median: {format_currency(town['median_home_price'])} | Tax: {format_currency(town['avg_property_tax'])}/yr")
        print(f"      Why: {town['highlights'][0]}")

    if args.all_details:
        for town in results:
            print_detail(town)

    print(f"\n  Tip: Run with --detail <town-name> for full details on any town.")
    print(f"  Tip: Run with --sort school|price|commute|tax to re-rank results.\n")


if __name__ == "__main__":
    main()
