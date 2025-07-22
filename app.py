import streamlit as st
from datetime import datetime
import pandas as pd
from db import get_db
from auth import autenticar
from utils import alerta_estoque, enviar_email, enviar_whatsapp, registrar_entrega
from relatorios import gerar_pdf_estoque, gerar_pdf_entregas

st.set_page_config(page_title="Sistema de Fardas", layout="wide")

st.title("Sistema de Controle de Fardas")

db = get_db()
usuarios_col = db["usuarios"]
cadastro_col = db["cadastro"]
produtos_col = db["produtos"]
movimentacao_col = db["movimentacao"]
alunos_col = db["alunos"]
movimentacao_aluno_col = db["movimentacao_aluno"]

# LOGIN
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.subheader("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar(usuario.strip(), senha.strip()):
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

# MENU
opcoes = [
    "Cadastro de Peças",
    "Movimentação de Estoque",
    "Relatório de Estoque",
    "Alunos",
    "Histórico de Entregas"
]
menu = st.sidebar.radio("Menu", opcoes)

# CADASTRO DE PEÇAS
if menu == "Cadastro de Peças":
    st.subheader("Cadastro de Peças")
    nome = st.text_input("Nome da peça")
    imagem = st.file_uploader("Imagem da peça", type=["png", "jpg", "jpeg"])
    if st.button("Cadastrar"):
        if nome:
            cadastro_col.insert_one({"nome": nome, "imagem": imagem.name if imagem else ""})
            st.success("Peça cadastrada com sucesso!")
        else:
            st.warning("Preencha o nome da peça")

# MOVIMENTAÇÃO DE ESTOQUE
elif menu == "Movimentação de Estoque":
    st.subheader("Movimentação de Estoque")
    produtos = [p["nome"] for p in cadastro_col.find()]
    if not produtos:
        st.warning("Nenhuma peça cadastrada!")
    else:
        produto = st.selectbox("Peça", produtos)
        tipo = st.radio("Tipo de movimentação", ["Entrada", "Saída"])
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        if st.button("Registrar Movimentação"):
            movimentacao_col.insert_one({
                "produto": produto,
                "tipo": tipo,
                "quantidade": quantidade,
                "data": datetime.now().strftime("%Y-%m-%d")
            })
            st.success("Movimentação registrada com sucesso!")

# RELATÓRIO DE ESTOQUE
elif menu == "Relatório de Estoque":
    st.subheader("Relatório de Estoque")
    pipeline = [
        {"$group": {
            "_id": "$produto",
            "entrada": {"$sum": {"$cond": [{"$eq": ["$tipo", "Entrada"]}, "$quantidade", 0]}},
            "saida": {"$sum": {"$cond": [{"$eq": ["$tipo", "Saída"]}, "$quantidade", 0]}}
        }}
    ]
    resultados = list(movimentacao_col.aggregate(pipeline))
    df = pd.DataFrame(resultados)
    if not df.empty:
        df["saldo"] = df["entrada"] - df["saida"]
        df.rename(columns={"_id": "produto"}, inplace=True)
        st.dataframe(df)
        
        if st.button("Gerar PDF do Estoque"):
            nome_pdf = gerar_pdf_estoque(df)
            with open(nome_pdf, "rb") as f:
                st.download_button("📥 Baixar PDF do Estoque", f, file_name=nome_pdf)

# ALUNOS (simplificado para registro entrega)
elif menu == "Alunos":
    st.subheader("Registro de Entrega de Fardas aos Alunos")

    alunos = list(alunos_col.find())
    nomes_alunos = [a["nome"] for a in alunos] if alunos else []

    if not nomes_alunos:
        st.warning("Nenhum aluno cadastrado.")
    else:
        aluno_nome = st.selectbox("Aluno", nomes_alunos)
        aluno_selecionado = next((a for a in alunos if a["nome"] == aluno_nome), None)
        if aluno_selecionado:
            cgm = aluno_selecionado.get("cgm", "")
            turma = aluno_selecionado.get("turma", "")
            st.write(f"**CGM:** {cgm}")
            st.write(f"**Turma:** {turma}")

            pecas = list(cadastro_col.find())
            entrega = {}
            for peca in pecas:
                col1, col2, col3 = st.columns([2, 2, 2])
                with col1:
                    st.image(f"images/{peca['imagem']}", width=80)
                with col2:
                    qtd = st.number_input(f"{peca['nome']} - Quantidade", min_value=0, step=1, key=f"qtd_{peca['nome']}")
                with col3:
                    tam = st.selectbox("Tamanho", ["", "P", "M", "G", "GG", "EGG"], key=f"tam_{peca['nome']}")
                entrega[peca["nome"]] = {"quantidade": qtd, "tamanho": tam}

            if st.button("Salvar Entrega"):
                registros_salvos = registrar_entrega(aluno_nome, cgm, turma, entrega, movimentacao_aluno_col)
                if registros_salvos > 0:
                    st.success(f"{registros_salvos} peça(s) registrada(s) com sucesso!")
                else:
                    st.info("Nenhuma alteração realizada.")

# HISTÓRICO DE ENTREGAS
elif menu == "Histórico de Entregas":
    st.subheader("Histórico de Entregas de Fardas")
    registros = list(movimentacao_aluno_col.find())
    if registros:
        df = pd.DataFrame(registros)
        st.dataframe(df)
        
        if st.button("Gerar PDF do Histórico"):
            nome_pdf = gerar_pdf_entregas(df)
            with open(nome_pdf, "rb") as f:
                st.download_button("📥 Baixar PDF do Histórico", f, file_name=nome_pdf)
    else:
        st.info("Nenhum registro de entrega encontrado.")
