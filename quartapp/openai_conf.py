from openai import AsyncOpenAI

organization = ""
api_key = ""
base_model = "gpt-4o"
base_temperature = 0.000000001
base_n = 1

openai_client = AsyncOpenAI(api_key=api_key, organization=organization)