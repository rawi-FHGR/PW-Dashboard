import dash.html as html

def display_info_text():

    text_style = {
        'fontFamily': 'Arial, sans-serif',  # oder die gleiche wie in deinem Plotly-Layout
        'fontSize': '18px',
        'color': '#000000'
    }

    # Inhalt der Textbox
    text_block = [
        html.P(f"Allgemeine Informationen",
               style={**text_style,
                      'fontWeight': 'bold',
                      'marginTop': '10px',
                      'fontSize': '20px'}),
        html.P(["Darstellung der Bestände bzw. Inverkehrsetzungen von Personenwagen auf Bundes- und Kantonsebene im Zeitraum zwischen 2010 und 2024.",
                html.Br(),
               "Datenquellen:",
                html.Br(),
                " * Bestand-Daten: Bundesamt für Statistik (BFS)",
                html.Br(),
               " * Inverkehrsetzungen: Bundesamt für Statistik (BFS)",
                html.Br()],
               style=text_style),
        html.P("Bitte wählen Sie einen Kanton auf der Karte aus, um Details anzuzeigen.",
               style=text_style)
    ]

    return html.Div(text_block, style={
        'padding': '0px',  # kein Innenabstand nötig
        'border': 'none',  # keine Umrandung
        'backgroundColor': 'transparent'
    })
