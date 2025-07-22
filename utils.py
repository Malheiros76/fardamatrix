# utils.py

import urllib.parse
import smtplib
from email.mime.text import MIMEText
import streamlit as st

def enviar_email(destinatario, mensagem):
    """Envia um e-mail de alerta"""
    try:
        msg = MIMEText(mensagem)
        msg['Subject'] = 'Alerta de Estoque Baixo'
        msg['From'] = 'bibliotecaluizcarlos@gmail.com'
        msg['To'] = destinatario

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            # Substitua por uma senha de aplicativo ou variável de ambiente
            server.login('bibliotecaluizcarlos@gmail.com', 'terra166')
            server.send_message(msg)

    except Exception as e:
        st.error(f"Erro ao enviar email: {e}")

def enviar_whatsapp(numero, mensagem):
    """Gera link de WhatsApp com mensagem"""
    numero = numero.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    texto = urllib.parse.quote(mensagem)
    url = f"https://wa.me/55{numero}?text={texto}"
    st.markdown(f"[Abrir WhatsApp]({url})")

def alerta_estoque(movimentacao_col):
    """Verifica produtos com estoque abaixo do limite"""
    pipeline = [
        {
            "$group": {
                "_id": "$produto",
                "entrada": {
                    "$sum": {"$cond": [{"$eq": ["$tipo", "Entrada"]}, "$quantidade", 0]}
                },
                "saida": {
                    "$sum": {"$cond": [{"$eq": ["$tipo", "Saída"]}, "$quantidade", 0]}
                }
            }
        }
    ]
    resultados = list(movimentacao_col.aggregate(pipeline))
    mensagens = []
    for r in resultados:
        saldo = r["entrada"] - r["saida"]
        limite = r["entrada"] * 0.2
        if saldo < limite:
            mensagens.append(f"Produto {r['_id']} está abaixo do limite. Saldo atual: {saldo}")
    return mensagens
# utils.py (adicionar no final)

from datetime import datetime

def registrar_entrega(aluno_nome, cgm, turma, entrega, movimentacao_aluno_col):
    """Registra ou atualiza entregas de fardas no MongoDB"""
    registros_salvos = 0
    data_hoje = datetime.now().strftime("%Y-%m-%d")

    for peca, dados in entrega.items():
        qtd = dados["quantidade"]
        tam = dados["tamanho"]
        if qtd > 0:
            filtro = {
                "aluno": aluno_nome,
                "cgm": cgm,
                "turma": turma,
                "peca": peca.replace(".png", ""),
                "data": data_hoje
            }

            dados_novos = {
                "$set": {
                    "quantidade": qtd,
                    "tamanho": tam
                }
            }

            resultado = movimentacao_aluno_col.update_one(filtro, dados_novos, upsert=True)
            if resultado.modified_count > 0 or resultado.upserted_id:
                registros_salvos += 1

    return registros_salvos
