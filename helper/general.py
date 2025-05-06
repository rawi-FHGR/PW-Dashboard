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

# settings
available_years = list(range(2010,2025,1))
default_year = available_years[int(len(available_years)/2)]

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