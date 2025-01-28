import PyPDF2 as deleanpdf
from googletrans import Translator as deleantradutor
from gtts import gTTS as deleangs

# Função para extrair texto do PDF
def extrair_texto_pdf(caminho_pdf):
    leitor_pdf = deleanpdf.PdfFileReader(caminho_pdf)
    texto = ""
    for pagina in range(leitor_pdf.numPages):
        pagina_pdf = leitor_pdf.getPage(pagina)
        texto += pagina_pdf.extractText()
    return texto

# Função para traduzir texto
def traduzir_texto(texto, idioma_destino='pt'):
    tradutor = deleantradutor()
    traducao = tradutor.translate(texto, dest=idioma_destino)
    return traducao.text

# Função para converter texto em áudio
def texto_para_audio(texto, caminho_audio):
    tts = deleangs(text=texto, lang='pt')
    tts.save(caminho_audio)

# Caminho do arquivo PDF e do arquivo de áudio
caminho_pdf = 'seu_arquivo.pdf'
caminho_audio = 'saida_audio.mp3'

# Extrair texto do PDF
texto_pdf = extrair_texto_pdf(caminho_pdf)

# Traduzir texto
texto_traduzido = traduzir_texto(texto_pdf, 'pt')

# Converter texto traduzido em áudio
texto_para_audio(texto_traduzido, caminho_audio)

print("Processo concluído! O áudio foi salvo em", caminho_audio)
