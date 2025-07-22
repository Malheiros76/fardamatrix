# relatorios.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import datetime
import os

def gerar_pdf_estoque(df, nome_arquivo=None):
    """Gera um PDF com o relatório de estoque"""
    if nome_arquivo is None:
        nome_arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    cpdf = canvas.Canvas(nome_arquivo, pagesize=A4)

    try:
        cpdf.drawImage("cabeca.png", 2 * cm, 27 * cm, width=16 * cm, height=3 * cm)
    except:
        pass

    cpdf.setFont("Helvetica-Bold", 16)
    cpdf.drawString(2 * cm, 24 * cm, "Relatório de Estoque")

    y = 22 * cm
    for _, row in df.iterrows():
        texto = (
            f"{row['produto']} - Entrada: {row['entrada']} - "
            f"Saída: {row['saida']} - Saldo: {row['saldo']}"
        )
        cpdf.drawString(2 * cm, y, texto)
        y -= 0.6 * cm

        if y < 2 * cm:
            cpdf.showPage()
            try:
                cpdf.drawImage("cabeca.png", 2 * cm, 27 * cm, width=16 * cm, height=3 * cm)
            except:
                pass
            cpdf.setFont("Helvetica-Bold", 16)
            cpdf.drawString(2 * cm, 24 * cm, "Relatório de Estoque (Continuação)")
            y = 22 * cm

    cpdf.save()
    return nome_arquivo

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def gerar_pdf_entregas(df, nome_arquivo=\"historico_entregas.pdf\"):
    doc = SimpleDocTemplate(nome_arquivo, pagesize=landscape(A4))
    elementos = []

    estilos = getSampleStyleSheet()
    elementos.append(Paragraph(\"Histórico de Entregas de Fardas\", estilos['Title']))
    elementos.append(Spacer(1, 12))

    dados = [df.columns.to_list()] + df.values.tolist()
    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elementos.append(tabela)
    doc.build(elementos)
    return nome_arquivo

