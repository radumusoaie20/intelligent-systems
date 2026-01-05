from langchain_ollama import OllamaLLM

mixtralOllama = OllamaLLM(
    model="ollama/mistral",
    base_url="http://localhost:11434"
)

