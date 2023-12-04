from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")


# Criando uma lista de Opçôes baseada nas lojas disponíveis
op = list(df['ID Loja'].unique())  # O Parâmetro "unique" serve para que não se repitam as opçôes
op.append('Todas as lojas')  # Adicionando à minha lista "Todas as Lojas"

app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children='Gráfico com o faturamento de Todos os Produtos separados por Loja'),
    html.Div(children='''
        Obs: Esse Gráfico mostra a quantidade de produtos vendidos, não o faturamento
    ''', id="obs"),
    dcc.Dropdown(op, 'Todas as lojas', id='lista_lojas'),
    dcc.Graph(
        id='grafico_qtd_vendas',
        figure=fig
    )
])


@app.callback(
    Output('grafico_qtd_vendas', 'figure'),
    Input('lista_lojas', 'value')

)
def update_output(value):
    if value == "Todas as lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja'] == value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
