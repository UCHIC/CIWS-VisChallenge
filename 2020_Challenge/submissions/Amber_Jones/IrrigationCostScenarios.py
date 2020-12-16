##########################################
# Irrigation Cost Scenarios
##########################################
# Created by: Amber Jones
# Date: 3 Dec 2020
# This script focuses on outdoor/irrigation/sprinkler watering including several watering/irrigation scenarios.
# Hose use is also an outdoor use, but is disregarded for this analysis.
# The script imports labeled event data, groups by label, determines average daily and monthly volumes.
# Scenario 1: Reduce irrigation rate. Uses 1 inch/week recommendation.
# Scenario 2: Reduce irrigated area. Uses half of currently irrigated area.
# Scenario 3: Reduce both rate and area.
# All of these are compared to the current.
# Pricing for each scenario was also determined based on Providence City tiered rates.

# Import Libraries
#####################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
#####################

# Import Classified/Labeled Event Data
#####################
df_events = pd.read_csv('Classified_Events.csv', engine='python', header=0, parse_dates=True, infer_datetime_format=True)

# Organize data
#####################
# Group data by label
df = df_events.groupby('Label', as_index=False)['Volume(gal)'].sum()
df['Volume(gal)'] = df['Volume(gal)'].astype(int)
# Reorder rows
df = df.reindex([3, 2, 5, 4, 0, 1])
# Add columns for daily and monthly
df['daily'] = (df['Volume(gal)']/14).astype(int)
df['monthly'] = df['daily'] * 30

#####################
# Irrigation scenarios
#####################

# Reduce irrigation rate
#####################
# Recommended irrigation for turfgrass: 1 inch water = 27154 gallons/acre
# (see https://www.lowes.com/n/how-to/watering-tips)
lot_size = 0.28
lot_fraction = 2/3  # removing house and paved
one_inch = 27154  # gallons/acre per week
reduce_watering = one_inch * lot_size * lot_fraction * 30/7
# 27154 * 0.28 * 2/3 * (30 days/month) / (7 days/week) = 21723 gallons/month
# Comaparing to the current practice
current = df['monthly'][df['Label'] == 'irrigation'].sum()  # monthly water use under current scenario
current_inches = current*7/30*1/lot_fraction*1/lot_size*1/one_inch  # weekly watering depth under current scenario
# 47340 * 7/30 * 3/2 * 1/0.28 *1/27154 = 2.18 inches/week

# Reduce irrigated area
#####################
lot_reduce = 0.5
reduce_lawn = current * lot_reduce
reduce_both = one_inch * lot_size * lot_fraction * lot_reduce * 30/7
# 27154 gallons/acre 0.28*2/3*0.5 acres = 2534.5 gal is 1 inch of water
# 27154 * 0.28 * 2/3 * 30/7 * 0.5 = 10862 gallons/month

# Define datasets
#####################
Labels = ['Sprinklers', 'Indoor']
Scenario = ['Current Watering', 'Reduce Lawn', 'Reduce Watering', 'Reduce Both']
indoor = df['monthly'][df['Label'] != 'irrigation'].sum()
Indoor = [indoor, indoor, indoor, indoor]
Sprinklers = [current, reduce_lawn, reduce_watering, reduce_both]

#####################
# Pricing
#####################
# Providence City water rate tiers:
# $23.25 for 10,000 gallons of water.
# $0.75 per 1,000 gallons from 10,001 to 50,000 gallons.
# $1.50 per 1,000 gallons over 50,000 gallons.
tier1 = 10000
tier2 = 50000
flat_rate = 23.25
rate_tier1 = 0.75
rate_tier2 = 1.5

# Create dataframe with pricing information
pricing = pd.DataFrame({'Scenario': Scenario, 'Indoor': Indoor, 'Sprinklers': Sprinklers})
pricing['Total'] = pricing['Indoor'] + pricing['Sprinklers']
pricing['FirstTier'] = np.where(pricing['Total'] >= tier2, tier2-tier1, pricing['Total']-tier1)
pricing['SecondTier'] = np.where(pricing['Total'] >= tier2, pricing['Total']-tier2, 0)
pricing['FirstTierCost'] = pricing['FirstTier']*rate_tier1/1000
pricing['SecondTierCost'] = pricing['SecondTier']*rate_tier2/1000
pricing['TotalCost'] = pricing['FirstTierCost'] + pricing['SecondTierCost'] + flat_rate

#####################
# Plotting
#####################

# Bar chart
#####################
# Creates a stacked bar chart with indoor use remaining constant and sprinkler use varying for each scenario.
# Includes annotations for each pricing tier.

fig1 = plt.figure(figsize=(8, 5))
ax = fig1.add_subplot(1, 1, 1)

outdoor_color = '#346888'
indoor_color = '#94bed9'
width = 0.95

# Bars
p1 = ax.bar(Scenario, Sprinklers, bottom=Indoor, color=outdoor_color, width=width, edgecolor='w')
p2 = ax.bar(Scenario, Indoor, bottom=0, color=indoor_color, width=width, edgecolor='w')

# Lines and labels
p3 = ax.axhline(y=tier1, linewidth=1.5, linestyle='--', color='k')
# plt.text(x=4.5, y=10500, s='Flat Rate Tier', fontweight='bold', color='k')
p4 = ax.axhline(y=tier2, linewidth=1.5, linestyle='--', color='k')
# plt.text(x=4.5, y=50500, s='Irrigation Tier', fontweight='bold', color='gray')

# Cost and volume annotations
for i, rows in pricing.iterrows():
    ax.annotate('{:,.0f}'.format(rows['Total']) + ' gal', xy=(i, rows['Total']+1000),
                rotation=0, color='k', ha='center', va='center', alpha=0.7, fontsize=9)
    ax.annotate('${:,.2f}'.format(rows['TotalCost']), xy=(i, 13000),
                rotation=0, color='k', ha='center', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='square', fc='white', linewidth=0))

# Brackets for Rate Ranges
x1 = 3.65
x2 = 3.75
ax.annotate('Flat Rate\n$23.25', xy=(x1, 4700), xytext=(x2, 4700), annotation_clip=False, rotation=0,
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=2.75, lengthB=0.9', lw=1))
ax.annotate(' $0.75/\n1000gal', xy=(x1, 30000), xytext=(x2, 30000), annotation_clip=False, rotation=0,
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=10.9, lengthB=0.9', lw=1))
ax.annotate(' $1.50/\n1000gal', xy=(x1, 52600), xytext=(x2, 52600), annotation_clip=False, rotation=0,
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=1.25, lengthB=0.9', lw=1))

# Extras
ax.legend((p1, p2), Labels, loc='center right', ncol=1, frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(top=False, bottom=False, left=True, right=False, labelleft=True, labelbottom=True)
plt.ylabel('Monthly Volume (gal)')
plt.title('Summer Season Monthly Water Use and Cost')
plt.show()

# to save
plt.savefig('Images/outdoor_scenarios.png', bbox_inches='tight')

# Illustrations
#####################
# Creates an illustration of a reduced lot size with labels for irrigated area
fig2 = plt.figure(figsize=(7, 9))
fig2.subplots_adjust(hspace=0, wspace=0)
ax = fig2.add_subplot(2, 1, 1)
# import background
img = plt.imread('Images/house.png')
ax.imshow(img, extent=[0, 170, 0, 110])
ax.axis('off')
# add text
plt.text(x=47.5, y=51.15, s='{:,.3f}'.format(lot_size * lot_fraction) + ' acres',
         fontweight='bold', color='w', fontname='Arial Narrow', va='bottom', fontsize=12)
plt.text(x=140, y=51.15, s='{:,.3f}'.format(lot_size * lot_fraction * lot_reduce) + ' acres',
         fontweight='bold', color='w', fontname='Arial Narrow', va='bottom', fontsize=12)

# Creates an illustration with grass to compare weekly watering rates
ax = fig2.add_subplot(2, 1, 2)
# import background
img = plt.imread("Images/grass.png")
ax.imshow(img, extent=[0, 170, 0, 110])
ax.axis('off')
# Create a Rectangle patch and add to axes
rect = patches.Rectangle((3.28, 54.5), 80.15, (25*(current_inches-1)), linewidth=1, edgecolor='#2F5597', facecolor='#2F5597')
ax.add_patch(rect)
# add text
plt.text(x=26, y=45+(25*(current_inches-1)), s='{:,.2f}'.format(current_inches) + ' inches/week',
         fontweight='bold', color='w', fontname='Arial Narrow', va='bottom', fontsize=13, alpha=0.8)
plt.text(x=25, y=55+(25*(current_inches-1)), s='Currently watering',
         fontweight='bold', color='#203864', fontname='Arial Narrow', va='bottom', fontsize=13)
plt.text(x=112, y=45, s='1 inch/week',
         fontweight='bold', color='w', fontname='Arial Narrow', va='bottom', fontsize=13, alpha=0.8)
plt.text(x=97, y=55, s='Recommended watering',
         fontweight='bold', color='#203864', fontname='Arial Narrow', va='bottom', fontsize=13)

# to save
plt.savefig('Images/outdoor_illustration.png', bbox_inches='tight')

##########################################
