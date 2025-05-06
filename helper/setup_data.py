import pandas
import pandas as pd
from pyaxis import pyaxis

# Datei-Pfad
file_path_01 = './Data/Inverkehrsetzung_Gemeinde_2010_2024.px'
file_path_02 = './Data/Bestand_Gemeinde_2010_2024.px'
file_path_03 = './Data/Bevölkerung_Gemeinde_2010_2023.px'

# Einlesen der PX-Dateien
try:
    data_01 = pyaxis.parse(file_path_01, encoding="utf-8")
except UnicodeDecodeError:
    data_01 = pyaxis.parse(file_path_01, encoding="ISO-8859-1")

try:
    data_02 = pyaxis.parse(file_path_02, encoding="utf-8")
except UnicodeDecodeError:
    data_02 = pyaxis.parse(file_path_02, encoding="ISO-8859-1")

try:
    data_03 = pyaxis.parse(file_path_03, encoding="utf-8")
except UnicodeDecodeError:
    data_03 = pyaxis.parse(file_path_03, encoding="ISO-8859-1")

df_01 = pd.DataFrame(data_01['DATA'])
df_01["DATA"] = pd.to_numeric(df_01["DATA"], errors="coerce")
df_02 = pd.DataFrame(data_02['DATA'])
df_02["DATA"] = pd.to_numeric(df_02["DATA"], errors="coerce")
df_03 = pd.DataFrame(data_03['DATA'])
df_03["DATA"] = pd.to_numeric(df_03["DATA"], errors="coerce")


def get_df_ivs() -> pandas.DataFrame:
    return df_01

def get_df_bestand() -> pandas.DataFrame:
    return df_02

def get_df_volk() -> pandas.DataFrame:
    return df_03

if __name__ == "__main__":
    # Anzahl Gemeinden
    print(df_01["Gemeinde"].nunique())
    print(df_02["Gemeinde"].nunique())
    df_03_nurGmd = df_03[df_03["Kanton (-) / Bezirk (>>) / Gemeinde (......)"].str.startswith("......")]
    print(df_03_nurGmd["Kanton (-) / Bezirk (>>) / Gemeinde (......)"].nunique())
