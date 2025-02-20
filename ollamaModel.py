import ollama

class OllamaChatbotModel:
    def __init__(self, max_tokens=2096, temperature=0.5):
        self.max_tokens = max_tokens
        self.temperature = temperature

    def send_message(self, prompt: str) -> str:
        if isinstance(prompt, (list, dict)):
            prompt = str(prompt)
            
        resposta = ollama.chat(model='llama3.2:3b',
                       messages=[{
                           'role': 'user',
                           'content': prompt,
                       }])
        return resposta['message']['content']

    def generate(self, prompt: str, **kwargs) -> dict:
        resposta = self.send_message(prompt)
        # Aqui, encapsulamos a resposta num dict com a chave "generated_text" contendo outro dict com "content"
        print(resposta)
        return {"generated_text": resposta}

    def __call__(self, prompt: str, **kwargs) -> dict:
        return self.generate(prompt, **kwargs)

