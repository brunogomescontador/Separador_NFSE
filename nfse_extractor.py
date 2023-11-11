import tkinter as tk
from tkinter import filedialog
import os
import re
import shutil
import logging
import pdfplumber
import pytesseract
from PIL import Image
import pdf2image
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path


# Variável global para armazenar o caminho da pasta selecionada
pasta_selecionada = None

def configurar_logging(caminho_pasta):
    log_filename = os.path.join(caminho_pasta, 'log.txt')
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def extrair_texto_pdf_ocr(caminho_pdf):
    paginas = pdf2image.convert_from_path(caminho_pdf)
    texto = ''
    for pagina in paginas:
        texto += pytesseract.image_to_string(pagina)
    return texto

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto += texto_pagina
            else:
                # Se a página não contém texto legível, usa OCR
                texto += extrair_texto_pdf_ocr(caminho_pdf)
                break  # Assumindo que se uma página precisa de OCR, todas precisarão
    return texto


def identificar_notas_servico(texto_pdf):
    padroes = [
        r'Nota Fiscal (Eletrônica de Serviços|de serviço eletrônica - NFS-e|de Serviços Eletrônica - NFS-e)',
        r'Número (da Nota|do documento)\s*[\d]+',
        r'Código de Verificação\s*[\w\d-]+',
        r'(Prestador de Serviços|PRESTADOR DOS SERVIÇOS)'
    ]
    return any(re.search(padrao, texto_pdf) for padrao in padroes)


def verificar_retencao_impostos(texto_pdf):
    # Primeiro, verifique se o texto está no contexto de uma nota fiscal de serviço
    if not re.search(r'(Nota Fiscal|NFSe|Serviços)', texto_pdf, re.IGNORECASE | re.DOTALL):
        return False  # Não é uma nota fiscal de serviço

    # Se for uma nota fiscal de serviço, verifique a presença de retenções de impostos
    padroes_retencao = [
        r'(PIS|COFINS|IRRF|CSLL|Retenções Federais|Retenções de impostos).*?R\$[\s]*[\d.,]+'
    ]
    return any(re.search(padrao, texto_pdf, re.IGNORECASE | re.DOTALL) for padrao in padroes_retencao)

def extrair_e_salvar_pagina(caminho_pdf, numero_pagina, pasta_destino):
    reader = PdfReader(caminho_pdf)
    writer = PdfWriter()
    writer.add_page(reader.pages[numero_pagina])
    novo_nome_pdf = f"{os.path.splitext(os.path.basename(caminho_pdf))[0]}_pagina_{numero_pagina + 1}.pdf"
    novo_caminho_pdf = os.path.join(pasta_destino, novo_nome_pdf)
    with open(novo_caminho_pdf, 'wb') as f:
        writer.write(f)

def processar_pdf(caminho_pdf, pasta_destino):
    texto_pdf = extrair_texto_pdf(caminho_pdf)
    for i, page in enumerate(PdfReader(caminho_pdf).pages):
        if identificar_notas_servico(texto_pdf):
            extrair_e_salvar_pagina(caminho_pdf, i, pasta_destino)
            break  # Ou remova para verificar todas as páginas


def processar_arquivo_pdf():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if caminho_arquivo:
        label_processamento["text"] = "Processando arquivo..."
        pasta_destino = os.path.join(os.path.dirname(caminho_arquivo), 'Serviços Tomados')
        os.makedirs(pasta_destino, exist_ok=True)
        processar_pdf(caminho_arquivo, pasta_destino)
        label_processamento["text"] = "Arquivo processado com sucesso."
    else:
        label_processamento["text"] = "Nenhum arquivo selecionado."

def identificar_nfse_pdf():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if caminho_arquivo:
        pasta_destino = os.path.join(os.path.dirname(caminho_arquivo), 'Serviços Tomados')
        os.makedirs(pasta_destino, exist_ok=True)
        processar_pdf(caminho_arquivo, pasta_destino)
        # Atualizar interface ou indicar conclusão, se necessário

def organizar_arquivos(caminho_pasta, arquivos_servico, arquivos_retencao):
    # Cria as pastas se não existirem
    pasta_servicos = os.path.join(caminho_pasta, 'Serviços Tomados')
    pasta_retencao = os.path.join(pasta_servicos, 'Notas com Retenção')
    os.makedirs(pasta_servicos, exist_ok=True)
    os.makedirs(pasta_retencao, exist_ok=True)

    # Move os arquivos para as respectivas pastas
    for arquivo in arquivos_servico:
        shutil.move(arquivo, pasta_servicos)
    for arquivo in arquivos_retencao:
        shutil.move(arquivo, pasta_retencao)

def processar_pasta(caminho_pasta):
    arquivos_servico = []
    arquivos_retencao = []

    # Etapa 1: Identificar todas as Notas de Serviço
    for root, dirs, files in os.walk(caminho_pasta):
        for file in files:
            if file.endswith('.pdf'):
                caminho_completo = os.path.join(root, file)
                texto_pdf = extrair_texto_pdf(caminho_completo)
                
                if identificar_notas_servico(texto_pdf):
                    arquivos_servico.append(caminho_completo)

    # Mover todas as notas de serviço para "Serviços Tomados"
    pasta_servicos_tomados = os.path.join(caminho_pasta, 'Serviços Tomados')
    organizar_arquivos(caminho_pasta, arquivos_servico, [])

    # Etapa 2: Verificar as Notas de Serviço em "Serviços Tomados" para Retenção
    for file in os.listdir(pasta_servicos_tomados):
        if file.endswith('.pdf'):
            caminho_completo = os.path.join(pasta_servicos_tomados, file)
            texto_pdf = extrair_texto_pdf(caminho_completo)
            if verificar_retencao_impostos(texto_pdf):
                arquivos_retencao.append(caminho_completo)

    # Mover notas com retenção para "Notas com Retenção"
    organizar_arquivos(pasta_servicos_tomados, [], arquivos_retencao)
    
    logging.info("Processamento concluído")



def escolher_pasta():
    global pasta_selecionada
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:  # Garantir que uma pasta foi selecionada
        configurar_logging(pasta_selecionada)
        label_selecao["text"] = f"Pasta selecionada: {pasta_selecionada}"
    else:
        label_selecao["text"] = "Nenhuma pasta selecionada"

def iniciar_processamento():
    if pasta_selecionada:
        label_processamento["text"] = "Analisando a pasta..."
        processar_pasta_selecionada(pasta_selecionada)
        label_processamento["text"] = "Processamento concluído"
    else:
        label_processamento["text"] = "Por favor, selecione uma pasta primeiro."

def processar_pasta_selecionada(caminho_pasta):
    processar_pasta(caminho_pasta)



# Configuração da janela principal
root = tk.Tk()
root.title("Selecionador de Pasta para Análise de Notas Fiscais")

# Rótulo com instruções
label_instrucao = tk.Label(root, text="Selecione uma pasta para analisar as Notas Fiscais de Serviço", font=("Helvetica", 12))
label_instrucao.pack(pady=10)

# Botão para selecionar a pasta
botao_selecionar = tk.Button(root, text="Selecionar Pasta", command=escolher_pasta, font=("Helvetica", 12))
botao_selecionar.pack(pady=5)

# Rótulo para mostrar a pasta selecionada
label_selecao = tk.Label(root, text="Nenhuma pasta selecionada", font=("Helvetica", 12))
label_selecao.pack(pady=10)

# Botão para processar um arquivo PDF
botao_processar_pdf = tk.Button(root, text="Processar Arquivo PDF", command=processar_arquivo_pdf, font=("Helvetica", 12))
botao_processar_pdf.pack(pady=5)


# Botão para iniciar o processamento
botao_processar = tk.Button(root, text="Processar Pasta", command=iniciar_processamento, font=("Helvetica", 12))
botao_processar.pack(pady=5)



# Rótulo para mostrar o status do processamento
label_processamento = tk.Label(root, text="", font=("Helvetica", 12))
label_processamento.pack(pady=10)

# Executar a janela
root.mainloop()
