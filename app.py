from smolagents import CodeAgent, HfApiModel,load_tool
import yaml
from tools.final_answer import FinalAnswerTool
from mytools import *
import os,subprocess,sys


# Imports para melhorar a interação com o agent:
from readMic import ReadMic, read_audio
from STT import transcribe_audio
from TTS import text_to_speech
from time import time


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    # model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
    model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud',
    custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# Carrega templates do prompt
with open(r"C:\Users\amori\Documents\Codigos\Assistent\Agent\prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

    
agent = CodeAgent(
    model=model,
    tools=[final_answer, image_generation_tool, ## add your tools here (don't remove final answer)
           get_current_time_in_timezone,math_operation,
           internet_search, get_stock_info,
           get_stock_price, compare_stocks,
           get_index_price], 
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)

def main():
    print("=== Bem-vindo ao Agente Interativo ===")
    # Cria a instância com o dispositivo correto (índice 2 para o microfone do headset)
    read_mic = ReadMic(device_index=3, output_file="audio_gravado.wav", duration=5, sample_rate=44100, channels=1)
    print("Mic conectado")

    # Grava o áudio e salva no arquivo "audio_gravado.wav"
    read_mic.gravar_com_dispositivo(indice_dispositivo=3)
    print("Áudio gravado")

    # Transcreve o áudio utilizando o arquivo salvo
    entry = transcribe_audio(read_mic.output_file)
    print("Áudio transcrito")


    response = agent.run(entry)
    print("\nResposta do agente:")
    print(response)

    if isinstance(response, list):  # Verifica se é uma lista
        text = "\n".join(response)  # Junta os elementos com quebra de linha
    else:
        text = response

    audio_path = text_to_speech(text, "output.wav")
    print("Áudio gerado")
    
    if audio_path:
        read_audio(audio_path)


if __name__ == "__main__":
    main()