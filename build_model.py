#!/usr/bin/env python3
"""
Cost Intelligence Model Builder
Processes extracted cost plan data and builds regression models.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import statistics

def load_data(data_file: str) -> list:
    """Load extracted cost plan data."""
    path = Path(data_file)
    if not path.exists():
        return []
    with open(path) as f:
        data = json.load(f)
    return data.get("cost_plans", [])

def classify_scheme_type(avg_unit_size: float, num_units: int) -> str:
    """Classify scheme type based on unit size."""
    if avg_unit_size > 150000:
        return "big_box"
    elif avg_unit_size > 30000:
        return "mid_box"
    elif num_units > 5:
        return "mli"
    else:
        return "mid_box"

def classify_region(location: str) -> str:
    """Classify region from location string."""
    location_lower = location.lower()
    
    london_areas = ['london', 'croydon', 'enfield', 'waltham', 'walthamstow', 'bow', 
                    'thamesmead', 'park royal', 'wimbledon', 'chessington', 'acton']
    se_areas = ['bracknell', 'watford', 'borehamwood', 'hemel', 'guildford', 'st albans',
                'harlow', 'banbury', 'thatcham', 'sevenoaks', 'letchworth']
    em_areas = ['leicester', 'enderby', 'daventry', 'northampton', 'nottingham']
    wm_areas = ['birmingham', 'tyseley', 'coventry', 'gaydon']
    ee_areas = ['peterborough', 'bedford', 'chelmsford', 'norwich']
    sw_areas = ['ferndown', 'bournemouth', 'gloucester', 'bristol']
    nw_areas = ['manchester', 'trafford', 'salford']
    ne_areas = ['leeds', 'sheffield', 'york']
    
    for area in london_areas:
        if area in location_lower:
            return "london"
    for area in se_areas:
        if area in location_lower:
            return "south_east"
    for area in em_areas:
        if area in location_lower:
            return "east_midlands"
    for area in wm_areas:
        if area in location_lower:
            return "west_midlands"
    for area in ee_areas:
        if area in location_lower:
            return "east_england"
    for area in sw_areas:
        if area in location_lower:
            return "south_west"
    for area in nw_areas:
        if area in location_lower:
            return "north_west"
    for area in ne_areas:
        if area in location_lower:
            return "north_east"
    
    return "unknown"

def build_statistics(plans: list) -> dict:
    """Build summary statistics from cost plans."""
    
    # Group by scheme type
    by_type = defaultdict(list)
    by_region = defaultdict(list)
    by_quarter = defaultdict(list)
    by_unit_size = defaultdict(list)
    
    for plan in plans:
        if not plan.get("total_budget_psf"):
            continue
            
        gia = plan.get("total_gia_sqft", 0)
        units = plan.get("number_of_units", 1)
        avg_unit = gia / units if units > 0 else gia
        
        scheme_type = plan.get("scheme_type") or classify_scheme_type(avg_unit, units)
        region = classify_region(plan.get("location", ""))
        
        by_type[scheme_type].append(plan)
        by_region[region].append(plan)
        
        # Group by unit size bands
        if avg_unit < 15000:
            by_unit_size["<15k"].append(plan)
        elif avg_unit < 30000:
            by_unit_size["15-30k"].append(plan)
        elif avg_unit < 75000:
            by_unit_size["30-75k"].append(plan)
        elif avg_unit < 150000:
            by_unit_size["75-150k"].append(plan)
        else:
            by_unit_size[">150k"].append(plan)
    
    def calc_stats(plans_list):
        if not plans_list:
            return None
        psf_values = [p["total_budget_psf"] for p in plans_list if p.get("total_budget_psf")]
        base_values = [p["base_build_psf"] for p in plans_list if p.get("base_build_psf")]
        if not psf_values:
            return None
        return {
            "count": len(psf_values),
            "avg_total_psf": round(statistics.mean(psf_values), 2),
            "median_total_psf": round(statistics.median(psf_values), 2),
            "min_total_psf": round(min(psf_values), 2),
            "max_total_psf": round(max(psf_values), 2),
            "avg_base_psf": round(statistics.mean(base_values), 2) if base_values else None,
            "std_dev": round(statistics.stdev(psf_values), 2) if len(psf_values) > 1 else 0
        }
    
    return {
        "by_scheme_type": {k: calc_stats(v) for k, v in by_type.items()},
        "by_region": {k: calc_stats(v) for k, v in by_region.items()},
        "by_unit_size": {k: calc_stats(v) for k, v in by_unit_size.items()},
        "total_plans": len(plans),
        "total_gfa": sum(p.get("total_gia_sqft", 0) for p in plans),
        "total_value": sum(p.get("total_budget_cost", 0) for p in plans)
    }

def build_regression_coefficients(plans: list) -> dict:
    """Build simple regression coefficients for cost prediction."""
    
    # Unit size vs £/sq ft regression
    data_points = []
    for plan in plans:
        if not plan.get("total_budget_psf") or not plan.get("total_gia_sqft"):
            continue
        gia = plan["total_gia_sqft"]
        units = plan.get("number_of_units", 1)
        avg_unit = gia / units if units > 0 else gia
        data_points.append((avg_unit, plan["total_budget_psf"]))
    
    if len(data_points) < 5:
        return {"error": "Insufficient data for regression"}
    
    # Simple linear regression
    x_mean = statistics.mean([p[0] for p in data_points])
    y_mean = statistics.mean([p[1] for p in data_points])
    
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in data_points)
    denominator = sum((x - x_mean) ** 2 for x, _ in data_points)
    
    slope = numerator / denominator if denominator != 0 else 0
    intercept = y_mean - slope * x_mean
    
    # R-squared
    ss_tot = sum((y - y_mean) ** 2 for _, y in data_points)
    ss_res = sum((y - (intercept + slope * x)) ** 2 for x, y in data_points)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return {
        "unit_size_regression": {
            "slope": round(slope, 8),
            "intercept": round(intercept, 2),
            "r_squared": round(r_squared, 3),
            "formula": f"£/sq ft = {round(intercept, 2)} + ({round(slope, 6)} × avg_unit_sqft)",
            "interpretation": f"Each additional 10,000 sq ft reduces cost by £{abs(round(slope * 10000, 2))}/sq ft"
        }
    }

def main():
    # Load data
    data_file = Path(__file__).parent / "extracted_data.json"
    plans = load_data(str(data_file))
    
    if not plans:
        print("No data found. Run extraction first.")
        return
    
    # Build model
    stats = build_statistics(plans)
    regression = build_regression_coefficients(plans)
    
    model = {
        "metadata": {
            "built": datetime.now().isoformat(),
            "total_plans": len(plans),
            "source": "KAM Project Consultants Ltd cost plans"
        },
        "statistics": stats,
        "regression": regression
    }
    
    # Save model
    output_file = Path(__file__).parent / "cost_model.json"
    with open(output_file, "w") as f:
        json.dump(model, f, indent=2)
    
    print(f"Model built from {len(plans)} cost plans")
    print(f"Saved to: {output_file}")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
