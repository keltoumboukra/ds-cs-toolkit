import dspy
llm = dspy.LM('ollama_chat/llama3.2', 
  api_base='http://localhost:11434', 
  api_key='', temperature = 0.3)
dspy.configure(lm=llm)