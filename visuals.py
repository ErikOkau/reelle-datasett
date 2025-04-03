import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
import seaborn as sns

# data import from csv files
sjois_dataMax = pd.read_csv(
    "Sea_Ice_Index_Max_Rankings.csv",
    sep=";", header=None, names=["aar", "areal"], skiprows=1
)

sjois_dataMaxAnually = pd.read_csv(
    "Sea_Ice_Index_Anually.csv",
    sep=";", header=None, names=["aar", "areal"], skiprows=1
)

temperatur_data = pd.read_csv(
    "bjornoya_temp.csv",
    sep=";", names=["aar", "temperatur"], skiprows=1
)

print("Sjøis-data:")
print(sjois_dataMax)
print("\nTemperatur-data:")
print(temperatur_data.head())

# Kombiner datasett
merged_data = pd.merge(sjois_dataMax, temperatur_data, on="aar")

# Analyse av sjøis og temperatur
plt.figure(figsize=(12,6))
sns.lineplot(data=merged_data, x="aar", y="areal", label="Sjøis (km²)")
sns.lineplot(data=merged_data, x="aar", y="temperatur", label="Temperatur (°C)", alpha=0.7)
plt.title("Sammenheng mellom sjøis og temperatur på Svalbard (1979-2023)", pad=20)
plt.xlabel("År"), plt.ylabel("Verdi"), plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show(block=False)

# Regresjonsanalyse
slope_ice, _, _, p_ice, _ = linregress(merged_data["aar"], merged_data["areal"])
slope_temp, _, _, p_temp, _ = linregress(merged_data["aar"], merged_data["temperatur"])

korrelasjon = merged_data["areal"].corr(merged_data["temperatur"]) # Korrelasjon mellom sjøis og temperatur

print(f"\nSjøistrend: {slope_ice:.2f} km²/år (p={p_ice:.3f})")
print(f"\nTemperaturtrend: {slope_temp:.2f} °C/år (p={p_temp:.3f})")
print(f"\nKorrelasjon:\n{korrelasjon:.2f}")

# Trendplott med regresjon 
plt.figure(figsize=(12,6))
sns.regplot(x="aar", y="areal", data=merged_data, label=f"Sjøis (-{abs(slope_ice):.2f} km²/år)")
sns.regplot(x="aar", y="temperatur", data=merged_data, label=f"Temperatur (+{slope_temp:.2f}°C/år)")
plt.title("Lineære trender for sjøis og temperatur", pad=20), plt.xlabel("År"), plt.ylabel("Verdi"), plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show(block=False)



periode_1 = merged_data[merged_data["aar"] <= 2000]
periode_2 = merged_data[merged_data["aar"] > 2000]  

slope_p1, _, _, p_p1, _ = linregress(periode_1["aar"], periode_1["areal"])
slope_p2, _, _, p_p2, _ = linregress(periode_2["aar"], periode_2["areal"])

print(f"\nTrender per periode:")
print(f"1979-2000: {slope_p1:.2f} km²/år (p={p_p1:.3f})")
print(f"2001-2023: {slope_p2:.2f} km²/år (p={p_p2:.3f})")

# Periodesammenligning (1979-2000 vs. 2001-2023)
merged_data["periode"] = merged_data["aar"].apply(lambda x: "1979-2000" if x <= 2000 else "2001-2023")
sns.lmplot(x="aar", y="areal", hue="periode", data=merged_data, height=6, aspect=1.5)
plt.title("Akselererende sjøistap etter år 2000", pad=20)
plt.xlabel("År"), plt.ylabel("Sjøis (km²)")
plt.text(1985, 15, f"1979-2000: {slope_p1:.2f} km²/år", color="blue")
plt.text(1985, 14.5, f"2001-2023: {slope_p2:.2f} km²/år", color="orange")

plt.show()
