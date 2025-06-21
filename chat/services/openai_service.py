from openai import OpenAI
import os

class OpenAIClient():
    def __init__(self):
        self.client = OpenAI(os.getenv("OPENAI_API_KEY"))
    
    def respond(self, input, model="gpt-4.1"):
        response = self.client.responses.create(model, input)
        return response.output_text