import dash.html as html

import components.common as common

def display_info_text():
    # Inhalt der Textbox
    text_block = [
        html.P(f"Allgemeine Informationen", style={**common.text_style, 'fontWeight': 'bold', 'marginTop': '0px', 'fontSize': '0.95vw'}),
        html.P(["Darstellung der Bestände bzw. Inverkehrsetzungen von Personenwagen auf Bundes- und Kantonsebene im Zeitraum zwischen 2010 und 2024.",
                html.Br(),
               "Datenquellen:",
                html.Br(),
                html.Ul([
                    html.Li("Bestand-Daten: Bundesamt für Statistik (BFS)"),
                    html.Li("Inverkehrsetzungen: Bundesamt für Statistik (BFS)")
                ]),
                html.Br()],
               style=common.text_style),
        html.P("Bitte wählen Sie einen Kanton auf der Karte aus, um Details anzuzeigen.",
               style=common.text_style),
    ]

    return html.Div(text_block, style={
        'padding': '0px',
        'border': 'none',
        'backgroundColor': 'transparent'
    })
