import pandas as pd

# general settings and functions

# functions
def hex_to_rgba_value(hex_color, alpha=0.4):
    '''
    Converts a hex-coded color into a RGBA string with transparency.
    :param hex_color: The hex color to convert
    :return a RGBA string
    '''
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

def normalize_fuel_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate some fuel categories in the given dataframe.
     - sum up hybrid categories and provide these in the column 'Hybrid'
     - sum up Anderer, Gas, ohne Motor, Wasserstoff and provide these in the column 'Andere'

    :param df: original dataframe
    :return: df: aggregated dataframeKopie des DataFrames mit aggregierter Spalte 'Treibstoff_mod'
    """
    hybrid_categories = {
        "Benzin-elektrisch: Normal-Hybrid",
        "Benzin-elektrisch: Plug-in-Hybrid",
        "Diesel-elektrisch: Normal-Hybrid",
        "Diesel-elektrisch: Plug-in-Hybrid"
    }

    other_categories = {
        "Anderer",
        "Gas (mono- und bivalent)",
        "Ohne Motor",
        "Wasserstoff"
    }

    # prepare an aggregation map to sum up the values for each new category
    aggregation_map = {
        **{category: "Hybrid" for category in hybrid_categories},
        **{category: "Andere" for category in other_categories}
    }

    df = df.copy()
    # overwrite the original column 'Treibstoff'
    df['Treibstoff'] = df['Treibstoff'].replace(aggregation_map)

    return df

def format_number(value: int, use_separator: bool = True) -> str:
    '''
    Converts a number into an appropriate formatted number.
    :param value:
    :param use_separator:
    :return: reformatted number
    '''
    if use_separator:
        return f"{int(value):,}".replace(",", "'")  # CH format
    return str(int(value))

# settings
available_years = list(range(2010,2025,1))
default_year = available_years[int(len(available_years)/2)]

# colormap
colors = {
    "blue": "#1f77b4",
    "orange": "#ff7f0e",
    "green": "#2ca02c",
    "red": "#d62728",
    "purple": "#9467bd",
    "brown": "#8c564b",
    "pink": "#e377c2",
    "grey": "#7f7f7f"
}

if __name__ == "__main__":
    print(colors)