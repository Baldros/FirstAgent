from transformers import pipeline
import numpy as np
import scipy.io.wavfile as wav

def text_to_speech(text, audio_path="output.wav", speed_factor=1.0):
    tts = pipeline("text-to-speech", model="facebook/mms-tts-por")
    result = tts(text)
    
    audio_bytes = result["audio"]
    original_sample_rate = result["sampling_rate"]
    
    # Converte os bytes em um array NumPy de float32
    audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
    
    # Se speed_factor > 1, o áudio será reproduzido mais rápido
    new_sample_rate = int(original_sample_rate * speed_factor)
    
    # Salva como WAV (aqui, o áudio é tocado mais rápido devido ao sample_rate aumentado)
    wav.write(audio_path, new_sample_rate, audio_array)
    
    print(f"Áudio salvo em '{audio_path}' com sample_rate {new_sample_rate}.")
    
    return audio_path
