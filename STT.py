import whisper
import torch

def transcribe_audio(audio_file, model_size="small"):
    model = whisper.load_model(model_size)  # Escolha: tiny, base, small, medium, large
    model = model.to(dtype=torch.float32)  # Converte os pesos do modelo para FP32
    result = model.transcribe(audio_file)
    return result["text"]