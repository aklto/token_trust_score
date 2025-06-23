import openai
from config import OPENAI_KEY

client = openai.OpenAI(api_key=OPENAI_KEY)

def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
