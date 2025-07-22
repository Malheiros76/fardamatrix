from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import datetime

def gerar_pdf_estoque(df):
    nome_arquivo = f"relatorio_estoque_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, 28 * cm, "Relatório de Estoque")
    
    dados = [["Produto", "Entrada", "Saída", "Saldo"]]
    for _, row in df.iterrows():
        dados.append([row["produto"], str(row["entrada"]), str(row["saida"]), str(row["saldo"])])
    
    tabela = Table(dados, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
    estilo = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 12),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ])
    tabela.setStyle(estilo)
    
    largura, altura = A4
    tabela.wrapOn(c, largura, altura)
    tabela.drawOn(c, 2 * cm, 22 * cm - 20 * len(dados))
    
    c.save()
    return nome_arquivo


def gerar_pdf_entregas(df):
    nome_arquivo = f"historico_entregas_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=landscape(A4))
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, 19 * cm, "Histórico de Entregas de Fardas")
    
    dados = [list(df.columns)]
    for _, row in df.iterrows():
        linha = []
        for col in df.columns:
            valor = row[col]
            if isinstance(valor, (int, float)):
                valor = str(valor)
            linha.append(valor)
        dados.append(linha)
    
    col_widths = [4*cm] * len(df.columns)
    tabela = Table(dados, colWidths=col_widths)
    estilo = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 12),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
    ])
    tabela.setStyle(estilo)
    
    largura, altura = landscape(A4)
    tabela.wrapOn(c, largura, altura)
    altura_tabela = 18 * cm  # ajustar altura disponível
    
    tabela.drawOn(c, 1 * cm, altura - altura_tabela)
    
    c.save()
    return nome_arquivo
