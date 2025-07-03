import dspy

llm = dspy.LM('ollama_chat/llama3.2', 
  api_base='http://localhost:11434', 
  api_key='', temperature = 0.3)
dspy.configure(lm=llm)

simple_model = dspy.Predict("question -> answer: int")

simple_model(
  question="""I have 5 different balls and I randomly select 4. 
    How many possible combinations of the balls I can get?"""
)