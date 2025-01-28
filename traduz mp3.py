import pytranscript as pt
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Transcrição do áudio
wav_file = pt.to_valid_wav("audio.mp3", "audio_novo.wav")
transcript = pt.transcribe(wav_file, model="/vosk-model-en-us-aspire-0.2")

# Verificar se a transcrição foi bem-sucedida
if not transcript.text:
    print("Erro: A transcrição falhou ou não retornou nenhum texto.")
else:
    # Limpar e preparar o texto para tradução
    text_to_translate = ' '.join(transcript.text)  # Junta os elementos da lista em uma string
    text_to_translate = ' '.join(text_to_translate.split())  # Remove espaços extras
    text_to_translate = text_to_translate[:500000]  # Limita a 500000 caracteres

    if text_to_translate:
        try:
            # Tradução do texto
            translated_text = GoogleTranslator(source='en', target='pt').translate(text_to_translate)

            # Conversão do texto para áudio
            tts = gTTS(translated_text, lang='pt')
            tts.save("audio_pt.mp3")

            # Remover arquivo temporário
            if os.path.exists("audio_novo.wav"):
                os.remove("audio_novo.wav")

            print("Tradução concluída e salva em 'audio_pt.mp3'")
        except Exception as e:
            print(f"Erro durante a tradução ou conversão para áudio: {str(e)}")
    else:
        print("Erro: O texto transcrito está vazio após a limpeza.")

print("Texto transcrito original:", transcript.text)
print("Texto preparado para tradução:", text_to_translate)
