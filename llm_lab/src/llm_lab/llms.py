from langchain_ollama import OllamaLLM

ollama_1b = OllamaLLM(
    model="ollama/gemma3:1b",
    base_url="http://localhost:11434"
)

ollama_270m = OllamaLLM(
    model="ollama/gemma3:270m",
    base_url="http://localhost:11434"
)
