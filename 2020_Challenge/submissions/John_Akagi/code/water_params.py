# -*- coding: utf-8 -*-
"""
This file holds the parameters used during the data processing.
Primarily this is ideal usage values and water costs

Sources for Water Usage:
    
Water Cost:         https://www.loganutah.org/government/departments/public_works/water_and_waste_water/rates.php
Irrigation Usage:   https://blog.lawneq.com/calculating-lawn-irrigation-water-usage-and-costs/
                    https://todayshomeowner.com/calculating-lawn-irrigation-costs/
When to Water:      https://www.lawndoctor.com/blog/how-to-water-lawn/
Shower Flow:        https://www.epa.gov/watersense/showerheads
Shower Duration:    https://www.home-water-works.org/indoor-use/showers
"""

# Ideal Usage Values
ideal_toilet_gpf = 1.28
moderate_toilet_gpf = 1.6
ideal_faucet_gpm = 1.5
ideal_shower_gpm = 2.0
ideal_shower_duration = 5.0

# Cost Values (Logan)
cost_kgal = 1.42
cost_gal = cost_kgal/1000.0

# Irrigation Values
ideal_start = 4 # Earliest time to water
ideal_end = 9   # Latest time to water
gal_sqft = 0.623 # Gallons per sqft lawn per week 

# Time Values
days_month = 30 # Average days per month
days_week = 7   # Days per week
sec_day = 24*3600 # Seconds per day
