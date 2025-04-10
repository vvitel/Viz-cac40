import pandas as pd
from dash import Dash
from folder_code.layout import create_layout
from folder_code.callbacks import *

#récuperer nom des actions
cac40 = pd.read_html("https://en.wikipedia.org/wiki/CAC_40")[4]
company, tickers = list(cac40.Company), list(cac40.Ticker)
dic_company = dict(zip(company, tickers))
dic_action = [{"value": entreprise, "label": entreprise} for entreprise, _ in dic_company.items()]

#récupérer le front
front = create_layout(dic_action, dic_company)

#code de l'application
app = Dash(__name__)
server = app.server
app.layout = front

#lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
