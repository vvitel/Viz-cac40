import dash_mantine_components as dmc
import plotly.graph_objects as go
from datetime import datetime, date
from dash import html, dcc


#créer le front de l'application
def create_layout(dic_action_select, dico_company):
    return html.Div([
    dcc.Store(id="store_dic_company", data=dico_company),
    dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab("Informations", value="tab_information", style={"fontSize": "25px"}),
                    dmc.Tab("Visualisation", value="tab_visualisation", style={"fontSize": "25px"}),
                    dmc.Tab("Analyse", value="tab_analyse", style={"fontSize": "25px"}),
                ]
            ),
            #onglet information
            dmc.TabsPanel(
                html.Div([html.Br(),
                          dmc.List([
                              dmc.ListItem("Cette application a pour objectif de visualiser les évolutions des actions du CAC 40 📉"),
                              dmc.ListItem("Boursicoter n'est pas la plus saine des activités, optez plutôt pour la marche ou la lecture"),
                              dmc.ListItem("Souvenez vous qu'un tiens vaut mieux que deux tu l'auras et qu'un sou est un sou ☝️")],
                              size=20),
                              ]),
            value="tab_information"
            ),
            #onglet visualisation des données
            dmc.TabsPanel(
                dmc.Grid(
                    children=[
                        dmc.Col(
                            html.Div([
                                html.Br(),
                                #choisir action
                                dmc.Badge("Choisir action", size="lg", radius="lg", color="blue"),
                                dmc.MultiSelect(label="Action", id="select_action", data=dic_action_select, searchable=True, radius="lg", clearable=True, style={"width": 200}),
                                dmc.DatePicker(label="Début", id="date_debut", value=date(2020, 1, 1), radius="lg", clearable=False, style={"width": 200}),
                                dmc.DatePicker(label="Fin", id="date_fin", value=datetime.now().date(), radius="lg", clearable=False, style={"width": 200}),
                                html.Br(),
                                #simulateur
                                dmc.Badge("Simulateur", size="lg", radius="lg", color="indigo"),
                                dmc.Select(label="Action", id="select_action_simu", data=dic_action_select, searchable=True, radius="lg", clearable=True, style={"width": 200}),
                                dmc.DatePicker(label="Date achat", id="date_achat", value="", radius="lg", clearable=True, style={"width": 200}),
                                dmc.DatePicker(label="Date vente", id="date_vente", value="", radius="lg", clearable=True, style={"width": 200}),
                                dmc.TextInput(label="Nombre d'action", id= "text_nb_action", w=200, radius="lg"),
                                html.Br(),
                                dmc.Text("", id="text_d0_dd", size="xl", c="black", style={"display": "none"}),
                                dmc.Text("", id="text_simu_invest", size="xl", c="blue", style={"display": "none"}),
                                dmc.Text("", id="text_simu_renta", size="xl", c="green", style={"display": "none"}),
                                html.Br(),
                                #chercher action
                                dmc.Badge("Chercher action", size="lg", radius="lg", color="violet"),
                                dmc.Group(children=[dmc.TextInput(label="Valeur inf.", id="text_valeur_inf", w=91, radius="lg"),
                                                    dmc.TextInput(label="Valeur sup.", id="text_valeur_sup", w=90, radius="lg"),]),
                                dmc.Group(children=[dmc.TextInput(label="Pourcent inf.", id="text_pourcent_inf", w=91, radius="lg"),
                                                    dmc.TextInput(label="Pourcent sup.", id="text_pourcent_sup", w=90, radius="lg")]),

                            ]), 
                        span=2),
                        dmc.Col(
                            #graphique
                            html.Div([dcc.Graph(figure=go.Figure(), id="final-figure", style={"display": "none", "width": "100%", "height": "100%"}),
                                      dmc.Switch(id="switch_moyenne", label="Afficher la moyenne", size="md", radius="lg", checked=False, style={"display": "none"})]), 
                        span=10)],
                align = "stretch"),
            value="tab_visualisation"
            ),
            #onglet analyse
            dmc.TabsPanel(
                html.Div([
                    html.Br(),
                    #choisir date
                    dmc.Group(children=[dmc.DatePicker(label="Début", id="date_debut_analyse", value=date(2020, 1, 1), radius="lg", clearable=False, style={"width": 200}),
                                        dmc.DatePicker(label="Fin", id="date_fin_analyse", value="", radius="lg", clearable=False, style={"width": 200}),]),
                    dcc.Graph(figure=go.Figure(), id="final-figure_analyse", style={"display": "none"})]),
            value="tab_analyse"
            ),
        ],
        color="red",
        orientation="horizontal",
        value="tab_information"
    )
    ])