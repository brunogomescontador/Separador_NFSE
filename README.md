# Selecionador de Pasta para Análise de Notas Fiscais de Serviço

Este projeto é uma aplicação em Python com interface gráfica que permite a seleção de uma pasta para analisar e processar Notas Fiscais de Serviço em formato PDF. O objetivo é identificar e organizar essas notas, bem como verificar a presença de retenções de impostos. O projeto utiliza bibliotecas como `tkinter` para a interface gráfica, `pdfplumber` para a extração de texto de PDFs e `pytesseract` para OCR (Reconhecimento Óptico de Caracteres) em páginas que não possuem texto legível.

## Funcionalidades

- **Seleção de Pasta:** Permite ao usuário selecionar uma pasta para analisar todos os arquivos PDF contidos nela.
- **Processamento de Arquivos PDF:** Identifica Notas Fiscais de Serviço em arquivos PDF e move esses arquivos para uma subpasta chamada "Serviços Tomados".
- **Verificação de Retenção de Impostos:** Analisa as Notas Fiscais de Serviço para verificar se há retenção de impostos e organiza essas notas em uma subpasta chamada "Notas com Retenção".
- **Extração de Texto de PDFs:** Extrai texto de arquivos PDF, utilizando OCR para páginas que não possuem texto embutido.

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seuusuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Execute o script principal:**

   ```bash
   python nome_do_arquivo.py
   ```

2. **Selecione uma pasta:** Clique no botão "Selecionar Pasta" para escolher a pasta que deseja analisar.

3. **Processar Arquivo PDF:** Se preferir processar um arquivo PDF individualmente, clique no botão "Processar Arquivo PDF" e selecione o arquivo desejado.

4. **Iniciar Processamento da Pasta:** Após selecionar a pasta, clique no botão "Processar Pasta" para iniciar a análise dos arquivos PDF na pasta escolhida.

5. **Verificação de Retenção:** O programa automaticamente verifica e organiza as notas fiscais que possuem retenção de impostos.

## Estrutura do Projeto

- **`main.py`:** Arquivo principal que contém a interface gráfica e lógica de processamento.
- **`requirements.txt`:** Lista de dependências necessárias para executar o projeto.
- **`log.txt`:** Arquivo gerado automaticamente que contém os logs do processamento, localizado na pasta selecionada pelo usuário.

## Dependências

- `tkinter`: Interface gráfica
- `pdfplumber`: Extração de texto de PDFs
- `pytesseract`: OCR para extração de texto de imagens
- `PyPDF2`: Manipulação de arquivos PDF
- `pdf2image`: Conversão de páginas de PDF em imagens

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).
