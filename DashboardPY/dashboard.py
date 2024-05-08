import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from io import StringIO

# Função para abrir o navegador com a aplicação web
def open_browser():
    url = 'http://localhost:8501'  # Substitua pela URL da sua aplicação Streamlit
    webbrowser.open_new_tab(url)

st.set_page_config(layout="wide")

# Chamando a função para abrir o navegador com a aplicação web
# Comente esta linha para evitar abrir o navegador automaticamente
# open_browser()

# Função para inserir o cabeçalho com imagem centralizada
def header_with_image(image_url, image_width):
    st.markdown(
        f"""
        <div style="background-color:#0054A5;padding:10px;border-radius:10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
        <img src="{image_url}" alt="header image" style="display:block;margin:auto;width:{image_width}px; height: 100px"/>
        </div>
        """,
        unsafe_allow_html=True,
    )

# URL da imagem
image_url = "http://marketing.mixd.com.br/admin/temp/user/128/mundial%20editora%20logotipo%20negativo%20(1).png"

# Largura desejada da imagem
image_width = "100%"

# Chamando a função para exibir o cabeçalho com imagem
header_with_image(image_url, image_width)

# Carregar o arquivo CSV diretamente do GitHub
url_csv = "https://raw.githubusercontent.com/Httpstheus/Streamlit-Python/main/DashboardPY/base_792.csv"
response = requests.get(url_csv)
csv_text = response.text

# Ler o CSV
df = pd.read_csv(StringIO(csv_text), encoding="latin-1", sep=";", decimal=".")

# Calculando a soma da coluna "Recebido"
soma_recebido = df['Recebido'].sum()

# Criando a figura para a soma da coluna "Recebido"
fig_recebido = go.Figure(go.Indicator(
    mode="number",
    value=soma_recebido,
    title="Soma do Recebido",
    number={'prefix': 'R$ ', 'valueformat': ',.2f'}
))

# Exibindo o gráfico do Recebido
st.plotly_chart(fig_recebido, use_container_width=True)

# Calculando os top usuários com os maiores recebimentos
top_users = df.nlargest(11, 'Recebido')

# Formatando a coluna "Recebido" como R$ com duas casas decimais
top_users['Recebido'] = top_users['Recebido'].apply(lambda x: f'R$ {x:.2f}')

# Calculando as contagens da coluna "condicao"
contagem_condicao = df['condicao'].value_counts()

# Criando o gráfico de contagem da coluna "condicao" usando Plotly Graph Objects
fig_contagem_condicao = go.Figure(go.Bar(
    x=contagem_condicao.index,
    y=contagem_condicao.values,
    text=contagem_condicao.values,  # Adicionando o texto dos valores no gráfico
    textposition='auto',  # Posição automática do texto
    marker_color='rgb(158,202,225)',  # Cor das barras
))

# Configurando o layout do gráfico
fig_contagem_condicao.update_layout(
    title="Contagem de Condição",
    xaxis=dict(title='Condição'),  # Título do eixo x
    yaxis=dict(title='Contagem', showgrid=True, showticklabels=True),  # Título e ticks do eixo y visíveis
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),  # Posição da legenda
)

# Calculando as somas das QUANTIDADES 
soma_QntPixGerado     = df['QntPixGerado'].sum()
soma_QntPixPendente   = df['QntPixPendente'].sum()
soma_QntCartãopassado = df['QntCartãopassado'].sum()
soma_BoletosEmitidos  = df['BoletosEmitidos'].sum()

# Definindo os valores de somas_qntds
somas_qntds = [soma_QntPixGerado, soma_QntPixPendente, soma_QntCartãopassado, soma_BoletosEmitidos]

# Criando a figura para as somas das QUANTIDADES
fig_qntds = go.Figure()
for categoria, soma in zip(['QntPixGerado', 'QntPixPendente', 'QntCartãopassado', 'BoletosEmitidos'], somas_qntds):
    fig_qntds.add_trace(go.Bar(x=[categoria], y=[soma], name=categoria, text=[(soma)], textposition='outside'))

fig_qntds.update_layout(title='Quantidades Geradas Hoje', yaxis_title='', legend_orientation="h")

# Calculando as somas dos VALORES
soma_pix_negociado = df['ValorPixNegociado'].sum()
soma_pix_pendente = df['ValorPixPendente'].sum()
soma_pix_recebido = df['ValorPixRecebido'].sum()
soma_cartao_recebido = df['RecebimentoCartão'].sum()

# Definindo os nomes e as somas
categorias_somas = ['ValorPixNegociado', 'ValorPixPendente', 'ValorPixRecebido', 'RecebimentoCartão']
somas_somas = [soma_pix_negociado, soma_pix_pendente, soma_pix_recebido, soma_cartao_recebido]

# Criando a figura para as somas dos VALORES
fig_somas = go.Figure()
for categoria, soma in zip(categorias_somas, somas_somas):
    fig_somas.add_trace(go.Bar(x=[categoria], y=[soma], name=categoria, text=['R$ {:.2f}'.format(soma)], textposition='auto'))

fig_somas.update_layout(title='Somas dos Valores', yaxis_title='Soma (R$)', legend_orientation="h")

# Organizando o layout conforme a sua solicitação
# Exibindo todos os elementos na mesma coluna
col1, col2 = st.columns(2)

with col1:
    st.write("Top 12 Usuários com Maiores Recebimentos:")
    st.table(top_users[['Usuario', 'Recebido']])
    st.plotly_chart(fig_qntds, use_container_width=True)

with col2:
    # Exibindo o gráfico de contagem da coluna "condicao"
    st.plotly_chart(fig_contagem_condicao, use_container_width=True)
    st.plotly_chart(fig_somas, use_container_width=True)
