from langchain_openai import ChatOpenAI

def load_llm(config: dict):
    provider = config['provider'].lower()
    model = config[provider]['model']
    temperature = config[provider]['temperature']
    max_completion_tokens = config[provider]['max_completion_tokens']
    
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens
    )
    
    return llm