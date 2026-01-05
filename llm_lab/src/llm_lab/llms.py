from langchain_ollama import OllamaLLM

ollama = OllamaLLM(
    model="ollama/gemma3:1b",
    base_url="http://localhost:11434"
)

