#!/usr/bin/env python3
"""
Free UK Business Directory Submission Helper
=============================================
Site: homekitchenuk.netlify.app
Business: Home Kitchen UK

This script:
1. Loads the comprehensive directory list from free-uk-directories.json
2. Provides utilities to filter/prioritize directories
3. Generates a submission tracking spreadsheet (CSV)
4. Can attempt automated submissions where supported (future enhancement)
5. Exports prioritized lists for manual submission

Usage:
    python3 free-uk-directories.py show              # Display the directory list
    python3 free-uk-directories.py csv               # Export as CSV tracking sheet
    python3 free-uk-directories.py priority          # Show priority submission order
    python3 free-uk-directories.py stats             # Show statistics
    python3 free-uk-directories.py filter --da-min 50 # Filter by minimum DA
    python3 free-uk-directories.py checklist         # Generate manual submission checklist
"""

import json
import csv
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(SCRIPT_DIR, "free-uk-directories.json")
CSV_FILE = os.path.join(SCRIPT_DIR, "submission-tracker.csv")
CHECKLIST_FILE = os.path.join(SCRIPT_DIR, "submission-checklist.md")

# NAP details for consistent submissions
NAP_DETAILS = {
    "name": "Home Kitchen UK",
    "website": "https://homekitchenuk.netlify.app",
    "email": "hermeswillmakesmoney@gmail.com",
    "phone": "",  # Add phone if available (optional but helps SEO)
    "address": "",  # Add UK address if available
    "short_description": "Expert UK reviews of kitchen appliances, cookware, and home goods. Helping British consumers make informed buying decisions.",
    "long_description": "Home Kitchen UK provides in-depth, unbiased reviews and buying guides for kitchen appliances, cookware, and home goods. We test and compare products to help UK consumers find the best value for their homes. From kettles and toasters to refrigerators and ovens, we cover everything you need for a well-equipped kitchen.",
    "categories": ["Home & Garden", "Kitchen & Dining", "Appliances", "Consumer Reviews", "Shopping"],
    "keywords": ["kitchen appliances UK", "home appliance reviews", "kitchen gadgets", "cookware reviews", "UK buying guides"],
    "opening_hours": "Monday-Friday: 9:00 AM - 5:00 PM",  # Adjust as needed
    "logo_url": "https://homekitchenuk.netlify.app/logo.png",  # Adjust to actual logo URL
}


def load_directories() -> Dict:
    """Load the directory list from JSON."""
    with open(JSON_FILE, "r") as f:
        return json.load(f)


def filter_free_only(directories: List[Dict]) -> List[Dict]:
    """Return only directories that offer free listings."""
    return [d for d in directories if d["free_listing"]]


def filter_by_da(directories: List[Dict], min_da: int = 0, max_da: int = 100) -> List[Dict]:
    """Filter directories by domain authority range."""
    return [d for d in directories if min_da <= d["domain_authority"] <= max_da]


def filter_uk_only(directories: List[Dict]) -> List[Dict]:
    """Return only UK-focused directories."""
    return [d for d in directories if d["uk_focused"]]


def filter_by_category(directories: List[Dict], category: str) -> List[Dict]:
    """Filter directories by category."""
    return [d for d in directories if d["category"] == category]


def filter_do_follow(directories: List[Dict]) -> List[Dict]:
    """Return only directories with do-follow links (better SEO)."""
    return [d for d in directories if d["do_follow"]]


def sort_by_da(directories: List[Dict], reverse: bool = True) -> List[Dict]:
    """Sort directories by domain authority."""
    return sorted(directories, key=lambda x: x["domain_authority"], reverse=reverse)


def show_directories(directories: List[Dict], detailed: bool = False):
    """Display directory list in formatted output."""
    print(f"\n{'='*80}")
    print(f"  FREE UK BUSINESS DIRECTORIES - Home Kitchen UK")
    print(f"  Total: {len(directories)} directories")
    print(f"{'='*80}\n")

    if detailed:
        for i, d in enumerate(directories, 1):
            print(f"  {i:3d}. {d['name']}")
            print(f"       URL:      {d['url']}")
            print(f"       Submit:   {d['submission_url']}")
            print(f"       DA:       {d['domain_authority']}")
            print(f"       Account:  {'Yes' if d['requires_account'] else 'No'} ({d['account_type']})")
            print(f"       UK Focus: {'Yes' if d['uk_focused'] else 'No'}")
            print(f"       Category: {d['category']}")
            print(f"       Link:     {'Do-Follow' if d['do_follow'] else 'No-Follow'}")
            print(f"       Notes:    {d['notes']}")
            print()
    else:
        print(f"  {'#':<4} {'Directory':<30} {'DA':<5} {'Free':<6} {'UK':<5} {'Follow':<8} {'Category':<15}")
        print(f"  {'-'*4} {'-'*30} {'-'*5} {'-'*6} {'-'*5} {'-'*8} {'-'*15}")
        for i, d in enumerate(directories, 1):
            free = "✓" if d["free_listing"] else "✗"
            uk = "✓" if d["uk_focused"] else "—"
            follow = "Do-Follow" if d["do_follow"] else "No-Follow"
            print(f"  {i:<4} {d['name']:<30} {d['domain_authority']:<5} {free:<6} {uk:<5} {follow:<8} {d['category']:<15}")

    print(f"\n  {'='*80}")
    free_count = len([d for d in directories if d['free_listing']])
    uk_count = len([d for d in directories if d['uk_focused']])
    dofollow_count = len([d for d in directories if d['do_follow']])
    print(f"  Free listings: {free_count} | UK-focused: {uk_count} | Do-Follow: {dofollow_count}")
    print()


def export_csv(directories: List[Dict]):
    """Export directory list as a submission tracking CSV."""
    fieldnames = [
        "Order", "Directory Name", "URL", "Submission URL", "Domain Authority",
        "Free Listing", "UK Focused", "Do-Follow", "Category", "Requires Account",
        "Account Type", "Status", "Date Submitted", "Login Email", "Notes"
    ]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, d in enumerate(directories, 1):
            writer.writerow({
                "Order": i,
                "Directory Name": d["name"],
                "URL": d["url"],
                "Submission URL": d["submission_url"],
                "Domain Authority": d["domain_authority"],
                "Free Listing": "Yes" if d["free_listing"] else "No",
                "UK Focused": "Yes" if d["uk_focused"] else "No",
                "Do-Follow": "Yes" if d["do_follow"] else "No",
                "Category": d["category"],
                "Requires Account": "Yes" if d["requires_account"] else "No",
                "Account Type": d["account_type"],
                "Status": "Pending",
                "Date Submitted": "",
                "Login Email": "",
                "Notes": d["notes"],
            })

    print(f"\n  ✓ CSV tracking sheet saved to: {CSV_FILE}")
    print(f"  ✓ Contains {len(directories)} directories ready for tracking")
    print(f"  ✓ Open in Excel/Google Sheets to track your submissions\n")


def generate_checklist(directories: List[Dict]):
    """Generate a markdown checklist for manual submissions."""
    priority = [
        "Google Business Profile", "Bing Places for Business", "Yelp UK",
        "Yell.com", "Houzz UK", "Hotfrog UK", "FreeIndex",
        "Cylex UK", "Thomson Local", "192.com", "Brownbook",
        "Scoot", "Bizify", "The Best Of UK", "Infobel UK",
    ]

    # Sort: priority items first, then rest by DA
    priority_dirs = []
    other_dirs = []
    for d in directories:
        if d["name"] in priority:
            priority_dirs.append(d)
        else:
            other_dirs.append(d)

    priority_dirs.sort(key=lambda x: priority.index(x["name"]) if x["name"] in priority else 999)
    other_dirs.sort(key=lambda x: x["domain_authority"], reverse=True)

    all_sorted = priority_dirs + other_dirs

    with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Home Kitchen UK - SEO Directory Submission Checklist\n\n")
        f.write(f"**Site:** https://homekitchenuk.netlify.app  \n")
        f.write(f"**Business:** Home Kitchen UK  \n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        f.write(f"**Total Directories:** {len(all_sorted)}\n\n")

        f.write("---\n\n")
        f.write("## NAP Details (Copy & Paste into each directory)\n\n")
        f.write(f"- **Business Name:** {NAP_DETAILS['name']}\n")
        f.write(f"- **Website:** {NAP_DETAILS['website']}\n")
        f.write(f"- **Email:** {NAP_DETAILS['email']}\n")
        f.write(f"- **Phone:** {NAP_DETAILS['phone'] or '(Not provided)'}\n")
        f.write(f"- **Address:** {NAP_DETAILS['address'] or '(Online business - remote)'}\n")
        f.write(f"- **Short Description:** {NAP_DETAILS['short_description']}\n\n")
        f.write(f"**Long Description:**\n> {NAP_DETAILS['long_description']}\n\n")
        f.write(f"**Categories:** {', '.join(NAP_DETAILS['categories'])}\n\n")
        f.write(f"**Keywords:** {', '.join(NAP_DETAILS['keywords'])}\n\n")

        f.write("---\n\n")
        f.write("## HIGH PRIORITY (Submit First)\n\n")
        f.write("These directories have the highest impact. Complete these first.\n\n")
        f.write("| # | Directory | DA | Submit URL | Account? | Done? |\n")
        f.write("|---|-----------|----|------------|----------|-------|\n")

        for i, d in enumerate(priority_dirs, 1):
            sub_url = d["submission_url"].replace("|", "\\|")
            acc = "Yes" if d["requires_account"] else "No"
            f.write(f"| {i} | [{d['name']}]({d['url']}) | {d['domain_authority']} | [Submit]({sub_url}) | {acc} | ⬜ |\n")

        f.write("\n---\n\n")
        f.write("## ADDITIONAL DIRECTORIES\n\n")
        f.write("Complete these after the high-priority list.\n\n")
        f.write("| # | Directory | DA | Submit URL | Account? | Done? |\n")
        f.write("|---|-----------|----|------------|----------|-------|\n")

        for i, d in enumerate(other_dirs, 1):
            sub_url = d["submission_url"].replace("|", "\\|")
            acc = "Yes" if d["requires_account"] else "No"
            f.write(f"| {i + len(priority_dirs)} | [{d['name']}]({d['url']}) | {d['domain_authority']} | [Submit]({sub_url}) | {acc} | ⬜ |\n")

        f.write("\n---\n\n")
        f.write("## Submission Tips\n\n")
        for i, tip in enumerate(NAP_DETAILS.get("_tips", []), 1):
            f.write(f"{i}. {tip}\n")

        f.write("\n### General Tips:\n")
        f.write("- Use the same email (hermeswillmakesmoney@gmail.com) for all accounts so you can recover passwords.\n")
        f.write("- Save all passwords in a password manager.\n")
        f.write("- If asked for a phone number and you don't have a business line, skip or use a virtual number.\n")
        f.write("- If asked for an address and you're online-only, use a virtual office or skip.\n")
        f.write("- Add your logo and photos where possible — listings with images get more clicks.\n")
        f.write("- Wait 1-2 days between submitting to each directory to look natural.\n")
        f.write("- After all submissions, use a tool like Ahrefs/Moz to verify backlinks are indexed.\n\n")

    print(f"\n  ✓ Checklist saved to: {CHECKLIST_FILE}")
    print(f"  ✓ Open as markdown or print for manual tracking\n")


def show_stats(directories: List[Dict]):
    """Display statistics about the directory list."""
    free = filter_free_only(directories)
    uk = filter_uk_only(directories)
    dofollow = filter_do_follow(directories)
    high_da = filter_by_da(directories, min_da=50)
    no_account = [d for d in directories if not d["requires_account"]]

    avg_da = sum(d["domain_authority"] for d in directories) / len(directories) if directories else 0
    avg_da_free = sum(d["domain_authority"] for d in free) / len(free) if free else 0

    print(f"\n{'='*50}")
    print(f"  DIRECTORY STATISTICS")
    print(f"{'='*50}")
    print(f"  Total directories listed:    {len(directories)}")
    print(f"  Free listings:               {len(free)}")
    print(f"  UK-focused:                  {len(uk)}")
    print(f"  Do-follow backlinks:         {len(dofollow)}")
    print(f"  High DA (DA ≥ 50):           {len(high_da)}")
    print(f"  No account needed:           {len(no_account)}")
    print(f"  Average DA (all):            {avg_da:.1f}")
    print(f"  Average DA (free only):      {avg_da_free:.1f}")
    print(f"{'='*50}")

    # Category breakdown
    print(f"\n  BY CATEGORY:")
    cats = {}
    for d in directories:
        cats[d["category"]] = cats.get(d["category"], 0) + 1
    for cat, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
        print(f"    {cat:<20} {count}")

    # DA distribution
    print(f"\n  DA DISTRIBUTION:")
    ranges = [(0, 30), (30, 50), (50, 70), (70, 90), (90, 100)]
    for lo, hi in ranges:
        count = len([d for d in directories if lo <= d["domain_authority"] < hi])
        bar = "█" * count
        print(f"    DA {lo:3d}-{hi:3d}:  {count:2d} {bar}")
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 free-uk-directories.py <command> [options]")
        print()
        print("Commands:")
        print("  show       Display the directory list")
        print("  show-full  Display with full details")
        print("  csv        Export as submission tracking CSV")
        print("  priority   Show priority submission order")
        print("  stats      Show statistics")
        print("  checklist  Generate markdown submission checklist")
        print("  filter     Filter directories (--da-min, --da-max, --uk-only, --free-only, --dofollow)")
        print()
        print("Examples:")
        print("  python3 free-uk-directories.py show")
        print("  python3 free-uk-directories.py stats")
        print("  python3 free-uk-directories.py filter --da-min 50 --dofollow")
        sys.exit(1)

    command = sys.argv[1]
    data = load_directories()
    directories = data["directories"]

    if command == "show":
        show_directories(directories, detailed=False)

    elif command == "show-full":
        show_directories(directories, detailed=True)

    elif command == "csv":
        # Export in priority order: high DA first, then UK-focused, then rest
        sorted_dirs = sort_by_da(directories)
        export_csv(sorted_dirs)

    elif command == "priority":
        priority_names = data.get("submission_strategy", {}).get("priority_order", [])
        priority_dirs = []
        other_dirs = []
        for d in directories:
            if d["name"] in priority_names:
                priority_dirs.append(d)
            else:
                other_dirs.append(d)
        priority_dirs.sort(key=lambda x: priority_names.index(x["name"]))
        other_dirs.sort(key=lambda x: x["domain_authority"], reverse=True)
        show_directories(priority_dirs + other_dirs, detailed=False)

    elif command == "stats":
        show_stats(directories)

    elif command == "checklist":
        generate_checklist(directories)

    elif command == "filter":
        result = directories
        args = sys.argv[2:]

        if "--da-min" in args:
            idx = args.index("--da-min")
            min_da = int(args[idx + 1])
            result = filter_by_da(result, min_da=min_da)
        if "--da-max" in args:
            idx = args.index("--da-max")
            max_da = int(args[idx + 1])
            result = filter_by_da(result, max_da=max_da)
        if "--uk-only" in args:
            result = filter_uk_only(result)
        if "--free-only" in args:
            result = filter_free_only(result)
        if "--dofollow" in args:
            result = filter_do_follow(result)
        if "--sort-da" in args:
            result = sort_by_da(result)

        show_directories(result, detailed="--detailed" in args)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
