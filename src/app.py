import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:latest"

# ============ CAMINHO DOS ARQUIVOS ============
PASTA = r"C:\Users\User\Documents"

# ============ CARREGAR DADOS ============
with open(f"{PASTA}\\perfil_investidor.json", "r", encoding="utf-8") as f:
    perfil = json.load(f)

transacoes = pd.read_csv(f"{PASTA}\\transacoes.csv")

historico = pd.read_csv(f"{PASTA}\\historico_atendimento.csv")

with open(f"{PASTA}\\produtos_financeiros.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """
Você é o Wemerson, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
- Nunca recomende investimentos específicos, apenas explique como funcionam.
- Responda apenas sobre educação financeira.
- Use os dados do cliente para dar exemplos personalizados.
- Linguagem simples e objetiva.
- Se não souber algo, diga que não possui essa informação e explique o conceito relacionado.
- Sempre pergunte se o cliente entendeu.
- Responda em no máximo 3 parágrafos.
"""

# ============ CHAMAR O OLLAMA ============
def perguntar(msg):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

Pergunta do cliente:
{msg}
"""

    resposta = requests.post(
        OLLAMA_URL,
        json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False
        }
    )

    resposta.raise_for_status()

    return resposta.json()["response"]

# ============ INTERFACE STREAMLIT ============
st.set_page_config(page_title="Wemerson - Educador Financeiro")

st.title("🎓 Wemerson - Educador Financeiro")

pergunta = st.chat_input("Digite sua dúvida sobre finanças...")

if pergunta:
    st.chat_message("user").write(pergunta)

    with st.spinner("Pensando..."):
        try:
            resposta = perguntar(pergunta)
            st.chat_message("assistant").write(resposta)
        except Exception as e:
            st.error(f"Erro ao consultar o modelo: {e}")
#cd C:\Users\User >> streamlit run app.py    
