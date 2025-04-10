from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from dash import callback, Output, Input
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

#récupérer les données
cac40 = pd.read_html("https://en.wikipedia.org/wiki/CAC_40")[4]
company, tickers = list(cac40.Company), list(cac40.Ticker)
date1="2020-01-01"
today = datetime.today().strftime("%Y-%m-%d")
df = yf.download(tickers, start=date1, end=today)

#filtrer et formater les données
def get_data(stock, dico_company, start_date=date1, end_date=today):
    df_func = df[(df.index >= start_date) & (df.index <= end_date)]
    date = pd.to_datetime(df_func.index.values)
    date = date.strftime('%Y-%m-%d').tolist()
    open, close = df_func[("Open", dico_company[stock])].values, df_func[("Close", dico_company[stock])].values
    low, high = df_func[("Low", dico_company[stock])].values, df_func[("High", dico_company[stock])].values
    volume = df_func[("Volume", dico_company[stock])].values
    return date, open, close, low, high, volume

#callback pour afficher les courbes
@callback([Output("final-figure", "figure", allow_duplicate=True),
           Output("final-figure", "style", allow_duplicate=True),
           Output("switch_moyenne", "style", allow_duplicate=True)],
          [Input("select_action", "value"), Input("date_debut", "value"),
           Input("date_fin", "value"), Input("switch_moyenne", "checked"),
           Input("store_dic_company", "data")],
          prevent_initial_call=True)
def update_image(select_action, date_debut, date_fin, switch_moyenne, store_dic_company):
    #afficher courbes en choisissant entreprises
    if (select_action is not None) and (select_action != []):
        fig = go.Figure()
        for i in select_action:
            jour, _, cloture, _, _, _ = get_data(i, store_dic_company, date_debut, date_fin)
            fig.add_trace(go.Scatter(x=jour, y=cloture, mode="lines+markers", name=i))
            #afficher la moyenne
            if switch_moyenne:
                mean = np.mean(cloture)
                fig.add_shape(type="line", x0=min(jour), x1=max(jour), y0=mean, y1=mean, line=dict(width=2, dash="dash"))
                fig.add_annotation(x=min(jour), y=mean, text=i, font=dict(size=12, color="black"), align="center")
        return fig, {"display": "block"}, {"display": "block"}
    else:
        return go.Figure(), {"display": "none"}, {"display": "none"}

#callback pour la recherche d'action
@callback([Output("final-figure", "figure", allow_duplicate=True),
           Output("final-figure", "style", allow_duplicate=True),],
          [Input("text_valeur_inf", "value"),
           Input("text_valeur_sup", "value"),
           Input("text_pourcent_inf", "value"),
           Input("text_pourcent_sup", "value"),
           Input("date_debut", "value"),
           Input("date_fin", "value"),
           Input("store_dic_company", "data")],
           prevent_initial_call=True)
def seek_stock(text_valeur_inf, text_valeur_sup, text_pourcent_inf, text_pourcent_sup, date_debut, date_fin, store_dic_company):
    fig = go.Figure()
    #recherche valeur
    if (text_valeur_inf != "") and (text_valeur_sup != ""):
        title = []
        for i in store_dic_company.keys():
            jour, _, cloture, _, _, _ = get_data(i, store_dic_company, date_debut, date_fin)
            inf, sup = int(text_valeur_inf), int(text_valeur_sup)
            if inf <= cloture[-1] <= sup:
                fig.add_trace(go.Scatter(x=jour, y=cloture, mode="lines+markers", name=i))
                title.append(i)
        #ajouter titre si une seule action
        if len(title) == 1:
            fig.update_layout(title=title[0], title_font=dict(color="blue"))
        return fig, {"display": "block"}
    #recherche evolution pourcentage
    if (text_pourcent_inf != "") and (text_pourcent_sup != ""):
        cpt = 0
        for i in store_dic_company.keys():
            jour, _, cloture, _, _, _ = get_data(i, store_dic_company, date_debut, date_fin)
            evol_pourcent = (cloture[-1] - cloture[0]) / cloture[0] * 100
            inf, sup = int(text_pourcent_inf), int(text_pourcent_sup)
            if inf <= evol_pourcent <= sup:
                fig.add_trace(go.Scatter(x=jour, y=cloture, mode="lines+markers", name=i))
                cpt += 1
        #ajouter titre si une seule action
        if cpt == 1:
            fig.update_layout(title=i, title_font=dict(color="blue"))
        return fig, {"display": "block"}
    else:
        return fig, {"display": "none"}


#callback pour simuler gain/perte
@callback([Output("text_simu_renta", "children"), Output("text_simu_renta", "style"),
           Output("text_simu_invest", "children"), Output("text_simu_invest", "style"),
           Output("text_d0_dd", "children"), Output("text_d0_dd", "style")], 
          [Input("select_action_simu", "value"), Input("date_achat", "value"),
           Input("date_vente", "value"), Input("text_nb_action", "value"),
           Input("store_dic_company", "data")])
def compute_value(select_action_simu, date_achat, date_vente, text_nb_action, store_dic_company):
    if (select_action_simu is not None) and (date_achat != "") and (date_vente != "") and (text_nb_action != ""):
        _, _, cloture, _, _, _ = get_data(select_action_simu, store_dic_company, date_achat, date_vente)
        achat, vente = cloture[0] * int(text_nb_action), cloture[-1] * int(text_nb_action)
        gain = f"gain: {round(vente - achat, 2)} €"
        color = "green" if round(vente - achat, 2) > 0 else "red"
        invest = f"investissement: {round(achat, 2)} €"
        d0_dd = f"{round(cloture[0], 2)} - {round(cloture[-1], 2)}"
        return gain, {"display": "block", "color": color}, invest, {"display": "block"}, d0_dd, {"display": "block"}
    else:
        return "", {"display": "none"}, "", {"display": "none"}, "", {"display": "none"}
    
#callback pour afficher ACP
@callback([Output("final-figure_analyse", "figure", allow_duplicate=True),
           Output("final-figure_analyse", "style", allow_duplicate=True)],
          [Input("date_debut_analyse", "value"),
           Input("date_fin_analyse", "value"),
           Input("store_dic_company", "data")],
          prevent_initial_call=True)
def show_acp(date_debut_analyse, date_fin_analyse, store_dic_company):
    list_acp = []
    for company in store_dic_company.keys():
        jour, ouverture, cloture, bas, haut, vol = get_data(company, store_dic_company, date_debut_analyse, date_fin_analyse)
        #centrer réduire
        cloture = (cloture - np.mean(cloture)) / np.std(cloture)
        #variables pour ACP
        diff_max_min = max(cloture) - min(cloture)
        diff_fin_deb = cloture[-1] - cloture[0]
        #diff_fin_max = cloture[-1] - max(cloture)
        quartiles = np.percentile(cloture, np.arange(0, 100, 25))
        ecart_inter_quartile = quartiles[3] - quartiles[1]
        #formater les données
        array = np.concatenate([[diff_max_min], [diff_fin_deb], [ecart_inter_quartile]])
        list_acp.append(array)
    
    #mettre sous forme de data frame
    df_acp = pd.DataFrame(list_acp, index=store_dic_company.keys())
    df_acp = df_acp.dropna()
    #df_acp.to_csv("./df_acp.csv", index=True)

    #réaliser ACP
    acp = PCA(n_components=2)
    pc_df = pd.DataFrame(acp.fit_transform(df_acp), columns=["PC1", "PC2"])
    pc_df["Index"] = df_acp.index
    #réaliser KMeans
    kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(np.array([pc_df["PC1"], pc_df["PC2"]]).T)
    pc_df["Cluster"] = kmeans.labels_.astype(str)
    #les couleurs
    pc_df["Cluster"] = pc_df["Cluster"].apply(lambda x: "cornflowerblue" if x == "0" else "crimson" if x == "1" else "darkviolet" if x == "2" else "purple")
    #visualisation
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pc_df["PC1"], y=pc_df["PC2"], mode="markers+text", text=pc_df["Index"], marker=dict(color=pc_df["Cluster"], opacity=0.5, showscale=False, size=12)))
    fig.update_layout(title=f"ACP & Clustering", title_font=dict(size=30), xaxis=dict(showticklabels=False, showgrid=True, zeroline=True), yaxis=dict(showticklabels=False, showgrid=True, zeroline=True),)
    return fig, {"display": "block"}