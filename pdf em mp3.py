from gtts import gTTS
from PyPDF2 import PdfReader

def pdf_to_text(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as f:
        reader = PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def text_to_audio(text, output_file, lang='pt'):
    tts = gTTS(text, lang=lang)
    tts.save(output_file)

# Exemplo de uso
pdf_file = "pdf.pdf"
output_audio_file = "pdf_audio.mp3"

text = pdf_to_text(pdf_file)
text_to_audio(text, output_audio_file, lang='pt')
