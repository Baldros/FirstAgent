import yaml
from smolagents import CodeAgent, load_tool
from tools.final_answer import FinalAnswerTool
from ollamaModel import OllamaChatbotModel
from my_tools import math_operation, get_current_time_in_timezone, internet_search

# Carrega templates do prompt
with open(r"C:\Users\amori\Documents\Codigos\Assistent\Agent\prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

# Instância do seu modelo local (Ollama)
model = OllamaChatbotModel(max_tokens=2096, temperature=0.5)

# Instância dos tools
final_answer = FinalAnswerTool()
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

# Cria o agente com a lista de tools desejadas
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        image_generation_tool,
        get_current_time_in_timezone,
        math_operation,
        internet_search,
    ],
    max_steps=6,
    verbosity_level=1,
    prompt_templates=prompt_templates
)

def main():
    print("=== Bem-vindo ao Agente Interativo ===")
    while True:
        prompt = input("\nDigite seu comando (ou 'sair' para encerrar): ")
        if prompt.strip().lower() == "sair":
            break
        try:
            response = agent.run(prompt)
            print("\nResposta do agente:")
            print(response)
        except Exception as e:
            print("Erro ao processar o comando:", e)

if __name__ == "__main__":
    main()
