import pandas as pd

df = pd.read_csv('Classified_Events.csv')
df.StartTime = pd.to_datetime(df.StartTime, format='%Y-%m-%d %H:%M:%S')
df.EndTime = pd.to_datetime(df.EndTime, format='%Y-%m-%d %H:%M:%S')
df.Label = df.Label.str.capitalize()

categories = df.Label.unique()
categories = [i.replace('Clothwasher', 'Washing Machine') for i in categories]

filt_Faucet = df.Label == 'Faucet'
filt_Toilet = df.Label == 'Toilet'
filt_Hose = df.Label == 'Hose'
filt_Clothwasher = df.Label == 'Clothwasher'
filt_Shower = df.Label == 'Shower'
filt_Irrigation = df.Label == 'Irrigation'

V_Faucet_sum = df.loc[filt_Faucet, 'Volume(gal)'].sum()
V_Toilet_sum = df.loc[filt_Toilet, 'Volume(gal)'].sum()
V_Hose_sum = df.loc[filt_Hose, 'Volume(gal)'].sum()
V_Clothwasher_sum = df.loc[filt_Clothwasher, 'Volume(gal)'].sum()
V_Shower_sum = df.loc[filt_Shower, 'Volume(gal)'].sum()
V_Irrigation_sum = df.loc[filt_Irrigation, 'Volume(gal)'].sum()
V_sum = [V_Faucet_sum, V_Toilet_sum, V_Hose_sum, V_Clothwasher_sum, V_Shower_sum, V_Irrigation_sum]

V_Faucet_mean = df.loc[filt_Faucet, 'Volume(gal)'].mean()
V_Toilet_mean = df.loc[filt_Toilet, 'Volume(gal)'].mean()
V_Hose_mean = df.loc[filt_Hose, 'Volume(gal)'].mean()
V_Clothwasher_mean = df.loc[filt_Clothwasher, 'Volume(gal)'].mean()
V_Shower_mean = df.loc[filt_Shower, 'Volume(gal)'].mean()
V_Irrigation_mean = df.loc[filt_Irrigation, 'Volume(gal)'].mean()
V_mean = [V_Faucet_mean, V_Toilet_mean, V_Hose_mean, V_Clothwasher_mean, V_Shower_mean, V_Irrigation_mean]

D_Faucet_sum = df.loc[filt_Faucet, 'Duration(min)'].sum()
D_Toilet_sum = df.loc[filt_Toilet, 'Duration(min)'].sum()
D_Hose_sum = df.loc[filt_Hose, 'Duration(min)'].sum()
D_Clothwasher_sum = df.loc[filt_Clothwasher, 'Duration(min)'].sum()
D_Shower_sum = df.loc[filt_Shower, 'Duration(min)'].sum()
D_Irrigation_sum = df.loc[filt_Irrigation, 'Duration(min)'].sum()
D_sum = [D_Faucet_sum, D_Toilet_sum, D_Hose_sum, D_Clothwasher_sum, D_Shower_sum, D_Irrigation_sum]

D_Faucet_mean = df.loc[filt_Faucet, 'Duration(min)'].mean()
D_Toilet_mean = df.loc[filt_Toilet, 'Duration(min)'].mean()
D_Hose_mean = df.loc[filt_Hose, 'Duration(min)'].mean()
D_Clothwasher_mean = df.loc[filt_Clothwasher, 'Duration(min)'].mean()
D_Shower_mean = df.loc[filt_Shower, 'Duration(min)'].mean()
D_Irrigation_mean = df.loc[filt_Irrigation, 'Duration(min)'].mean()
D_mean = [D_Faucet_mean, D_Toilet_mean, D_Hose_mean, D_Clothwasher_mean, D_Shower_mean, D_Irrigation_mean]


F_Faucet_mean = df.loc[filt_Faucet, 'Flowrate(gpm)'].mean()
F_Toilet_mean = df.loc[filt_Toilet, 'Flowrate(gpm)'].mean()
F_Hose_mean = df.loc[filt_Hose, 'Flowrate(gpm)'].mean()
F_Clothwasher_mean = df.loc[filt_Clothwasher, 'Flowrate(gpm)'].mean()
F_Shower_mean = df.loc[filt_Shower, 'Flowrate(gpm)'].mean()
F_Irrigation_mean = df.loc[filt_Irrigation, 'Flowrate(gpm)'].mean()
F_mean = [F_Faucet_mean, F_Toilet_mean, F_Hose_mean, F_Clothwasher_mean, F_Shower_mean, F_Irrigation_mean]
