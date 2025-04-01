import pandas as pd

# data import from csv files
Sea_Ice_Index_Monthly_Data_by_Year = pd.read_csv("Sea_Ice_Index_Monthly_Data_by_Year_G02135_v3.0.csv")  # Antatt format: aar, areal (km²)
Sea_Ice_Index_Min_Max_Rankings = pd.read_csv("Sea_Ice_Index_Min_Max_Rankings_G02135_v3.0.csv") # Antatt format: aar, areal (km²)

temperatur_data = pd.read_csv("bjornoya_temp.csv")  # Antatt format: aar, temperatur (°C) 

import matplotlib.pyplot as plt
import seaborn as sns

# Plot sjois over tid
plt.figure(figsize=(10,5))
sns.lineplot(x="aar", y="areal", data=Sea_Ice_Index_Min_Max_Rankings)
plt.title("Sjois paa Svalbard over tid")
plt.xlabel("aar")
plt.ylabel("Areal (km²)")

# Plot temperatur over tid
plt.figure(figsize=(10,5))  
sns.lineplot(x="aar", y="temperatur", data=temperatur_data)
plt.title("Temperatur paa Bjornoya over tid")
plt.xlabel("aar")
plt.ylabel("Temperatur (°C)")

# Slaa sammen datasett paa aar/maaned
merged_data = pd.merge(Sea_Ice_Index_Min_Max_Rankings, temperatur_data, on="aar")

# Beregn korrelasjon
correlation = merged_data["areal"].corr(merged_data["temperatur"])
print(f"Korrelasjon mellom sjois og temperatur: {correlation:.2f}")

from scipy.stats import linregress

# Regresjon for sjois over tid
slope_ice, intercept_ice, r_value_ice, p_value_ice, std_err_ice = linregress(
    merged_data["aar"], merged_data["areal"]
)
print(f"Sjois-trend: {slope_ice:.2f} km² per aar (p={p_value_ice:.3f})")

# Regresjon for temperatur over tid
slope_temp, intercept_temp, r_value_temp, p_value_temp, std_err_temp = linregress(
    merged_data["aar"], merged_data["temperatur"]
)
print(f"Temperatur-trend: {slope_temp:.2f} °C per aar (p={p_value_temp:.3f})")


# Sjois med trendlinje
plt.figure(figsize=(10,5))
sns.scatterplot(x="aar", y="areal", data=merged_data)
plt.plot(merged_data["aar"], intercept_ice + slope_ice*merged_data["aar"], 'r', label='Trendlinje')
plt.title("Sjois paa Svalbard med lineær trend")
plt.legend()

# Tilsvarende for temperatur



# Del data i to perioder (f.eks. for 2000 og etter 2000)
merged_data["periode"] = merged_data["aar"].apply(lambda x: "1970-2000" if x <= 2000 else "2001-2023")

# Grupper og sammenlign
sns.lmplot(x="aar", y="areal", hue="periode", data=merged_data, height=5, aspect=1.5)
plt.title("Sjois-trender i to perioder")