# ===============================
# APP DE INVESTIMENTOS - STREAMLIT
# ===============================

import streamlit as st
import yfinance as yf
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Investimentos", layout="wide")
st.title("💰 Simulador de Investimentos para Iniciantes")

# ===============================
# DADOS SIMULADOS / API
# ===============================

st.header("Top 3 Ações")
acoes = ["PETR4.SA", "VALE3.SA", "ITUB4.SA"]
dados_acoes = {}
for acao in acoes:
    ticker = yf.Ticker(acao)
    hist = ticker.history(period="30d")
    dados_acoes[acao] = hist['Close'][-1]

top3_acoes = sorted(dados_acoes.items(), key=lambda x: x[1], reverse=True)[:3]
for i, (acao, valor) in enumerate(top3_acoes, 1):
    st.write(f"{i}. {acao}: R$ {valor:.2f}")

st.header("Top 3 Criptomoedas")
url = "https://api.coingecko.com/api/v3/simple/price"
params = {"ids": "bitcoin,ethereum,cardano", "vs_currencies": "brl"}
resposta = requests.get(url, params=params).json()
top3_cripto = sorted(resposta.items(), key=lambda x: x[1]['brl'], reverse=True)[:3]
for i, (nome, valor) in enumerate(top3_cripto, 1):
    st.write(f"{i}. {nome.capitalize()}: R$ {valor['brl']:.2f}")

st.header("Top 3 Renda Fixa (Simulada)")
renda_fixa = [
    {"nome": "CDB 110% CDI", "rentabilidade": 0.11},
    {"nome": "LCI 100% CDI", "rentabilidade": 0.10},
    {"nome": "CDB 120% CDI", "rentabilidade": 0.12},
]
top3_renda_fixa = sorted(renda_fixa, key=lambda x: x['rentabilidade'], reverse=True)
for i, rf in enumerate(top3_renda_fixa, 1):
    st.write(f"{i}. {rf['nome']}: {rf['rentabilidade']*100:.1f}% a.m.")

st.header("Top 3 Fundos (Simulados)")
fundos = [
    {"nome": "Fundo Ações", "rentabilidade": 0.08},
    {"nome": "Fundo Renda Fixa", "rentabilidade": 0.05},
    {"nome": "Fundo Multimercado", "rentabilidade": 0.07},
]
top3_fundos = sorted(fundos, key=lambda x: x['rentabilidade'], reverse=True)
for i, f in enumerate(top3_fundos, 1):
    st.write(f"{i}. {f['nome']}: {f['rentabilidade']*100:.1f}% a.m.")

# ===============================
# SIMULADOR DE CARTEIRA
# ===============================
st.header("Simulador de Carteira")
valor_total = st.number_input("Quanto deseja investir (R$)?", min_value=1.0, value=1000.0, step=50.0)

# Distribuição simples igualitária
ativos = [*top3_acoes, *top3_cripto, *top3_renda_fixa, *top3_fundos]
valor_por_ativo = valor_total / len(ativos)

st.subheader("💸 Distribuição sugerida")
for ativo in ativos:
    if isinstance(ativo, tuple):
        nome = ativo[0]
    else:
        nome = ativo['nome']
    st.write(f"{nome}: R$ {valor_por_ativo:.2f}")

# ===============================
# GRÁFICO SIMULAÇÃO
# ===============================
st.subheader("📈 Evolução da Carteira (30 dias)")

dias = list(range(1, 31))
plt.figure(figsize=(10,5))

for ativo in ativos:
    if isinstance(ativo, tuple):
        nome = ativo[0]
        taxa = 0.001  # simulação ações/cripto pequena
    elif 'rentabilidade' in ativo:
        nome = ativo['nome']
        taxa = ativo['rentabilidade']/30  # mensal → diário
    else:
        nome = str(ativo)
        taxa = 0.001

    evolucao = [valor_por_ativo * (1 + taxa)**i for i in dias]
    plt.plot(dias, evolucao, label=nome)

plt.xlabel("Dias")
plt.ylabel("Valor (R$)")
plt.legend()
plt.grid(True)
st.pyplot(plt)
