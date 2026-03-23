#!/usr/bin/env python3
"""
Active Listings Summary - All 27 towns (as of March 2026).

Run this script to see a summary of active listings and direct links
for all towns matching the house search criteria.
"""

from tabulate import tabulate

LISTINGS_DATA = [
    # (Town, State, Active Listings, Median List Price, Days on Market, Search Links)
    {
        "town": "Glen Ridge",
        "state": "NJ",
        "zillow_listings": 7,
        "redfin_listings": 5,
        "median_list_price": "$1.09M",
        "avg_days_on_market": None,
        "sample_listings": [
            "1 single-family home + 5 luxury listings on Zillow",
            "Neighborhoods: Glenridge, South End, Bloomfield Avenue",
        ],
        "zillow_url": "https://www.zillow.com/glen-ridge-nj/",
        "redfin_url": "https://www.redfin.com/city/6809/NJ/Glen-Ridge",
    },
    {
        "town": "Glen Rock",
        "state": "NJ",
        "zillow_listings": 23,
        "redfin_listings": 9,
        "median_list_price": "$1.1M",
        "avg_days_on_market": 36,
        "sample_listings": [
            "274 Cornwall Rd — 6 BR/5.5 BA distinguished residence",
            "Renovated Colonial — 3,024 sqft, 4 BR, finished basement (~1,500 sqft)",
            "Multi-family: 3BR/1BA + 2BR/1BA (rented $3,750 + $2,800/mo)",
        ],
        "zillow_url": "https://www.zillow.com/glen-rock-nj/",
        "redfin_url": "https://www.redfin.com/city/6818/NJ/Glen-Rock",
    },
    {
        "town": "Pelham",
        "state": "NY",
        "zillow_listings": 26,
        "redfin_listings": 14,
        "median_list_price": "$1.37M",
        "avg_days_on_market": 42,
        "sample_listings": [
            "Colonial in Pelham Heights — 1907, 3,243 sqft, 5 BR/3.5 BA, 29 min to NYC",
            "4 BR/3.5 BA home across from train station, walk to shops",
            "2 BR/1 BA condo at Fairways, Pelham Manor — ~$525K",
        ],
        "zillow_url": "https://www.zillow.com/pelham-ny/",
        "redfin_url": "https://www.redfin.com/city/14762/NY/Pelham",
    },
    {
        "town": "Hastings-on-Hudson",
        "state": "NY",
        "zillow_listings": 20,
        "redfin_listings": 15,
        "median_list_price": "$1.02M",
        "avg_days_on_market": 15,
        "sample_listings": [
            "1909 Colonial — 4 BR, 1,544 sqft, steps from village center",
            "English Tudor — Riverview Manor neighborhood",
            "5 BR Colonial — 3,178 sqft + 755 sqft finished lower, chef's kitchen",
            "Clarewood Townhome — 3 BR/3.5 BA, 2,725 sqft, pool/tennis/gym",
        ],
        "zillow_url": "https://www.zillow.com/hastings-on-hudson-ny/",
        "redfin_url": "https://www.redfin.com/city/8353/NY/Hastings-on-Hudson",
    },
    {
        "town": "Great Neck",
        "state": "NY",
        "zillow_listings": 169,
        "redfin_listings": 47,
        "median_list_price": "$688K-$698K",
        "avg_days_on_market": 69,
        "sample_listings": [
            "Contemporary in Allenwood — 4 BR/4.5 BA, south-facing",
            "Brick Colonial in University Gardens — 5 BR/3.5 BA, meticulously maintained",
            "Kings Point: 29 homes | Great Neck Estates: 18 homes",
        ],
        "zillow_url": "https://www.zillow.com/great-neck-ny/",
        "redfin_url": "https://www.redfin.com/city/7691/NY/Great-Neck",
    },
    {
        "town": "South Orange",
        "state": "NJ",
        "zillow_listings": 22,
        "redfin_listings": 22,
        "median_list_price": "$899K",
        "avg_days_on_market": 34,
        "sample_listings": [
            "22 single-family homes on Zillow",
            "Market is competitive: avg 12 offers per listing",
            "Also: 4 condos, 2 townhouses, 7 multi-family units",
        ],
        "zillow_url": "https://www.zillow.com/south-orange-nj/",
        "redfin_url": "https://www.redfin.com/minorcivildivision/461/NJ/South-Orange-Village",
    },
    {
        "town": "Garden City",
        "state": "NY",
        "zillow_listings": 34,
        "redfin_listings": 23,
        "median_list_price": "$1.07M-$1.16M",
        "avg_days_on_market": 33,
        "sample_listings": [
            "26 single-family homes on Zillow",
            "7 homes under $800K available",
            "4 single-story homes at median $1.32M",
        ],
        "zillow_url": "https://www.zillow.com/garden-city-ny/",
        "redfin_url": "https://www.redfin.com/city/7197/NY/Garden-City",
    },
    {
        "town": "Maplewood",
        "state": "NJ",
        "zillow_listings": 28,
        "redfin_listings": None,
        "median_list_price": "$811K",
        "avg_days_on_market": 11,
        "sample_listings": [
            "92 Oakview Ave — $779K, 4 BR/2 BA",
            "483 Richmond Ave — $949K, 4 BR/4 BA",
            "29 Plymouth Ave — $629K, 3 BR/2 BA",
            "154 Parker Ave — $525K, 3 BR/2 BA",
            "694 Valley St — $599K, 3 BR/2 BA",
        ],
        "zillow_url": "https://www.zillow.com/maplewood-nj/",
        "redfin_url": "https://www.redfin.com/minorcivildivision/457/NJ/Maplewood-Township",
    },
    {
        "town": "Cranford",
        "state": "NJ",
        "zillow_listings": 42,
        "redfin_listings": 22,
        "median_list_price": "$667K",
        "avg_days_on_market": 24,
        "sample_listings": [
            "5 BR/4.5 BA Colonial, half-acre, no-flood zone, chef's kitchen",
            "Renovated Colonial on S Union Ave — 5 BR/3.5 BA (2023 reno)",
            "Updated two-family (2022 reno), income-producing",
        ],
        "zillow_url": "https://www.zillow.com/cranford-nj/",
        "redfin_url": "https://www.redfin.com/city/37655/NJ/Cranford",
    },
    {
        "town": "Irvington",
        "state": "NY",
        "zillow_listings": 28,
        "redfin_listings": 19,
        "median_list_price": "$1.16M",
        "avg_days_on_market": 36,
        "sample_listings": [
            "Marker Ridge by Toll Brothers — new townhomes, 3 BR, Spring 2026 move-in",
            "ZappiCo to-be-built — 4 BR/2.5 BA in Irvington school district",
            "Two-family (2016) — two 3 BR/2.5 BA duplex units",
            "Affordable: co-ops from ~$609K",
        ],
        "zillow_url": "https://www.zillow.com/irvington-ny/",
        "redfin_url": "https://www.redfin.com/city/9593/NY/Irvington",
    },
    {
        "town": "Bronxville",
        "state": "NY",
        "zillow_listings": 39,
        "redfin_listings": 13,
        "median_list_price": "$1.56M",
        "avg_days_on_market": None,
        "sample_listings": [
            "Elmsmere Estates — 5 BR/3.5 BA, pool, move-in ready",
            "5 Orchard Pl — Lewis Bowman Colonial, comprehensive renovation",
            "Bronxville Manor Colonial — 3 BR/1.5 BA, Viking kitchen",
            "Spanish Colonial — 3,780+ sqft, 4-5 BR, 1/3 acre",
        ],
        "zillow_url": "https://www.zillow.com/bronxville-ny/",
        "redfin_url": "https://www.redfin.com/city/2214/NY/Bronxville",
    },
    {
        "town": "Larchmont",
        "state": "NY",
        "zillow_listings": 25,
        "redfin_listings": 22,
        "median_list_price": "$1.47M",
        "avg_days_on_market": 86,
        "sample_listings": [
            "1 Crest Ave — $1.95M, 4 BR/3 BA, 2,389 sqft",
            "10 Varela Ln — $1.598M, 4 BR/5 BA, 3,522 sqft",
            "64 Maple Hill Dr — $1.3M, 3 BR/4 BA, 2,361 sqft",
            "11A Garit Ln — $839K, 4 BR/2 BA, 1,880 sqft",
            "18 Revere Rd — $608K, 3 BR/2 BA, 1,494 sqft",
        ],
        "zillow_url": "https://www.zillow.com/larchmont-ny/",
        "redfin_url": "https://www.redfin.com/city/10526/NY/Larchmont",
    },
    {
        "town": "Chatham",
        "state": "NJ",
        "zillow_listings": 43,
        "redfin_listings": 34,
        "median_list_price": "$2.04M",
        "avg_days_on_market": 64,
        "sample_listings": [
            "~50% of listings under $2M (median at $2.04M)",
            "Classic colonials with modern updates, walk-to-town",
            "New construction: 5 BR/5.1 BA custom colonials, 4 floors",
        ],
        "zillow_url": "https://www.zillow.com/chatham-nj/",
        "redfin_url": "https://www.redfin.com/city/3129/NJ/Chatham",
    },
    {
        "town": "Stamford (N. Stamford)",
        "state": "CT",
        "zillow_listings": 40,
        "redfin_listings": None,
        "median_list_price": "$750K",
        "avg_days_on_market": 17,
        "sample_listings": [
            "Lakefront property — 450 ft private lakefront, 1 hr to NYC",
            "Colonial on 2 acres — 1999 build, new central A/C, hardwood floors",
            "49 Alexandra — Colonial w/ modern addition, 1-acre flat lot",
            "25 Riverbank Dr — 4 BR, wall of windows, sunset views",
        ],
        "zillow_url": "https://www.zillow.com/north-stamford-stamford-ct/",
        "redfin_url": "https://www.redfin.com/neighborhood/550108/CT/Stamford/North-Stamford",
    },
    {
        "town": "Manhasset",
        "state": "NY",
        "zillow_listings": 49,
        "redfin_listings": 27,
        "median_list_price": "$1.6M-$2.0M",
        "avg_days_on_market": 33,
        "sample_listings": [
            "3 BR/1.5 BA Colonial — fireplace, open kitchen, heart of Manhasset",
            "2 BR/2 BA ranch — Estates I, high ceilings, low taxes",
            "14 single-story homes at median $1.6M",
        ],
        "zillow_url": "https://www.zillow.com/manhasset-ny/",
        "redfin_url": "https://www.redfin.com/city/24109/NY/Manhasset",
    },
    {
        "town": "Port Washington",
        "state": "NY",
        "zillow_listings": 28,
        "redfin_listings": 14,
        "median_list_price": "$1.2M",
        "avg_days_on_market": 37,
        "sample_listings": [
            "Renovated 2 BR/1.5 BA — moments from water",
            "Brick-front 3 BR/2 BA in Eastern Crest, blocks from LIRR",
            "34 Hillview Ave — 3 BR/3 BA Colonial, stroll to Main St",
        ],
        "zillow_url": "https://www.zillow.com/port-washington-ny/",
        "redfin_url": "https://www.redfin.com/city/25155/NY/Port-Washington",
    },
    {
        "town": "Summit",
        "state": "NJ",
        "zillow_listings": 13,
        "redfin_listings": 23,
        "median_list_price": "$1.11M-$1.64M",
        "avg_days_on_market": 61,
        "sample_listings": [
            "Renovated Colonial — half-acre, chef's kitchen, fireplace family room",
            "Colonial on .37 acre — Northside location, fenced backyard",
            "21 luxury listings on Redfin",
        ],
        "zillow_url": "https://www.zillow.com/summit-nj/",
        "redfin_url": "https://www.redfin.com/city/18243/NJ/Summit",
    },
    {
        "town": "Madison",
        "state": "NJ",
        "zillow_listings": 27,
        "redfin_listings": 18,
        "median_list_price": "$894K",
        "avg_days_on_market": 69,
        "sample_listings": [
            "1920s charming home — desirable location, great schools",
            "Move-in ready 5 BR/3 BA — walk to downtown & Midtown Direct train",
            "Modern farmhouse by Casa Vita Builders — 5 BR, 4 levels of luxury",
        ],
        "zillow_url": "https://www.zillow.com/madison-nj/",
        "redfin_url": "https://www.redfin.com/city/10822/NJ/Madison",
    },
    {
        "town": "Millburn/Short Hills",
        "state": "NJ",
        "zillow_listings": 49,
        "redfin_listings": 22,
        "median_list_price": "$2.25M-$2.79M",
        "avg_days_on_market": 23,
        "sample_listings": [
            "474 White Oak Ridge Rd — $1.5M, 4 BR/3 BA",
            "22 Great Hills Rd — $1.19M, 4 BR/4 BA, 2,902 sqft",
            "216 Glen Ave — $1.05M, 3 BR/3 BA",
            "415 Long Hill Dr — $1.895M, 5 BR/4 BA",
        ],
        "zillow_url": "https://www.zillow.com/millburn-nj/",
        "redfin_url": "https://www.redfin.com/minorcivildivision/462/NJ/Millburn-Township",
    },
    {
        "town": "Ridgewood",
        "state": "NJ",
        "zillow_listings": 26,
        "redfin_listings": 22,
        "median_list_price": "$1.12M",
        "avg_days_on_market": 67,
        "sample_listings": [
            "New construction — 5,500+ sqft, completion late Spring 2026",
            "5 BR/3+2 half BA Colonial on corner lot",
            "Move-in ready 3 BR/3.5 BA ranch",
            "7 homes under $800K available",
        ],
        "zillow_url": "https://www.zillow.com/ridgewood-nj/",
        "redfin_url": "https://www.redfin.com/city/16161/NJ/Ridgewood",
    },
    {
        "town": "Montclair",
        "state": "NJ",
        "zillow_listings": 43,
        "redfin_listings": 39,
        "median_list_price": "$1.12M",
        "avg_days_on_market": 29,
        "sample_listings": [
            "Renovated 5 BR/4.5 BA Colonial — quartz/granite, stainless appliances",
            "1909 Colonial in Upper Mountain/Bradford — designer refresh for 2026",
            "Investment properties near NYC trains — multi-unit options",
        ],
        "zillow_url": "https://www.zillow.com/montclair-nj/",
        "redfin_url": "https://www.redfin.com/city/35939/NJ/Montclair",
    },
    {
        "town": "Morristown",
        "state": "NJ",
        "zillow_listings": 70,
        "redfin_listings": 36,
        "median_list_price": "$683K-$766K",
        "avg_days_on_market": 26,
        "sample_listings": [
            "70 homes on Zillow — largest inventory of any town on this list",
            "34 single-family homes available",
            "Condos, townhouses, and multi-family also available",
        ],
        "zillow_url": "https://www.zillow.com/morristown-nj/",
        "redfin_url": "https://www.redfin.com/city/12345/NJ/Morristown",
    },
    {
        "town": "Scarsdale",
        "state": "NY",
        "zillow_listings": 66,
        "redfin_listings": 18,
        "median_list_price": "$2.53M",
        "avg_days_on_market": 66,
        "sample_listings": [
            "Sub-$2M: co-ops, condos, smaller SFH, Eastchester SD homes",
            "3 BR/1.5 BA in Eastchester SD — spacious, natural light",
            "Renovated Tudor w/ Eastchester schools — 2023 kitchen reno",
        ],
        "zillow_url": "https://www.zillow.com/scarsdale-ny/",
        "redfin_url": "https://www.redfin.com/city/16773/NY/Scarsdale",
    },
    {
        "town": "Westfield",
        "state": "NJ",
        "zillow_listings": 45,
        "redfin_listings": 33,
        "median_list_price": "$1.1M",
        "avg_days_on_market": 29,
        "sample_listings": [
            "Custom Colonial — 4 BR/4.5 BA, 1 block from Washington School",
            "Tudor-style — timeless charm, move-in ready",
            "Neo-Classical Colonial Revival — 6 BR/3.1 BA, architectural treasure",
            "5 new construction homes at median $1.45M",
        ],
        "zillow_url": "https://www.zillow.com/westfield-nj/",
        "redfin_url": "https://www.redfin.com/city/19891/NJ/Westfield",
    },
    {
        "town": "Chappaqua",
        "state": "NY",
        "zillow_listings": 14,
        "redfin_listings": 12,
        "median_list_price": "$724K",
        "avg_days_on_market": 62,
        "sample_listings": [
            "Bradley-built 5 BR Cape — cul-de-sac, fireplace, deck",
            "Colonial — 4-5 BR/3 BA, privacy, Chappaqua school district",
            "To-be-built — 3,485 sqft, move-in Spring 2026",
        ],
        "zillow_url": "https://www.zillow.com/chappaqua-ny/",
        "redfin_url": "https://www.redfin.com/city/21975/NY/Chappaqua",
    },
    {
        "town": "Darien",
        "state": "CT",
        "zillow_listings": 39,
        "redfin_listings": 15,
        "median_list_price": "$2.3M",
        "avg_days_on_market": 109,
        "sample_listings": [
            "475 Hoyt St — $1.25M, 4 BR/3 BA, 2,251 sqft (price cut $200K)",
            "33 Ridgeley St — $1.325M, 3 BR/2 BA, 2,343 sqft",
            "28 Great Hill Rd — $1.85M, 4 BR/4 BA, 3,511 sqft",
            "254 West Ave — $2.0M, 6 BR/6 BA, 3,266 sqft",
        ],
        "zillow_url": "https://www.zillow.com/darien-ct/",
        "redfin_url": "https://www.redfin.com/city/22280/CT/Darien",
    },
    {
        "town": "Norwalk/Rowayton",
        "state": "CT",
        "zillow_listings": 36,
        "redfin_listings": None,
        "median_list_price": "$1.73M",
        "avg_days_on_market": 35,
        "sample_listings": [
            "319 Rowayton Ave — $719K, 3 BR/2 BA, 1,428 sqft",
            "15 Shorefront Park — $899K, 3 BR/2 BA, 2,394 sqft",
            "22 Harstrom Pl — 1920s classic, gut-renovated 2022, new roof 2026",
        ],
        "zillow_url": "https://www.zillow.com/rowayton-norwalk-ct/",
        "redfin_url": "https://www.redfin.com/neighborhood/524674/CT/Norwalk/Rowayton",
    },
]


def main():
    print("\n" + "=" * 80)
    print("  ACTIVE LISTINGS ACROSS ALL 27 TOWNS (March 2026)")
    print("=" * 80)

    # Summary table
    headers = [
        "#",
        "Town",
        "St",
        "Zillow\nListings",
        "Redfin\nListings",
        "Median\nList Price",
        "Avg Days\non Market",
    ]
    rows = []
    total_zillow = 0
    total_redfin = 0
    for i, d in enumerate(LISTINGS_DATA, 1):
        z = d["zillow_listings"] or 0
        r = d["redfin_listings"] or 0
        total_zillow += z
        total_redfin += r
        rows.append([
            i,
            d["town"],
            d["state"],
            d["zillow_listings"] or "N/A",
            d["redfin_listings"] or "N/A",
            d["median_list_price"],
            f"{d['avg_days_on_market']}d" if d["avg_days_on_market"] else "N/A",
        ])
    rows.append(["", "TOTAL", "", total_zillow, total_redfin, "", ""])

    print(tabulate(rows, headers=headers, tablefmt="rounded_grid", stralign="center"))

    # Detailed listings per town
    for i, d in enumerate(LISTINGS_DATA, 1):
        print(f"\n{'─' * 70}")
        print(f"  {i}. {d['town']}, {d['state']}")
        print(f"     Listings: Zillow ({d['zillow_listings'] or 'N/A'}) | Redfin ({d['redfin_listings'] or 'N/A'})")
        print(f"     Median list price: {d['median_list_price']}")
        if d["avg_days_on_market"]:
            print(f"     Avg days on market: {d['avg_days_on_market']}")
        print(f"     Sample listings:")
        for listing in d["sample_listings"]:
            print(f"       - {listing}")
        print(f"     Links:")
        print(f"       Zillow: {d['zillow_url']}")
        print(f"       Redfin: {d['redfin_url']}")

    print(f"\n{'=' * 80}")
    print(f"  TOTAL: ~{total_zillow} listings on Zillow + ~{total_redfin} on Redfin")
    print(f"  across all 27 towns (some overlap between platforms)")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
