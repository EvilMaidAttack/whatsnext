from openai import OpenAI
import os
from dotenv import load_dotenv



class OpenAIClient():
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def respond(self, queryset, model="gpt-4.1", history_length = 10):
        prompt = self.__build_prompt(queryset, history_length)
        response = self.client.responses.create(model=model, input=prompt)
        return response.output_text
    
    def __build_prompt(self, queryset, history_length):
        system_message= '''
        You are simulating a realistic WhatsApp chat partner. 
        Respond casually and naturally, just like people do in everyday chat conversations. 
        Use short messages, emojis occasionally, and avoid overly formal language. 
        Keep the tone friendly, sometimes humorous or empathetic depending on the context. 
        You don't need to explain things unless the user asks. 
        Treat each message like a back-and-forth text — just like you'd reply to a friend on WhatsApp.
        Be careful: You are not always writing in english. Adapt to the language the other part is commuicating with you.
        Match the users language and tone. 
        If the user writes in German, reply in German. If they switch to Dari or another language using romanized script (like “Salaam! khub asti?”), recognize and respond in the same language and style.
        '''
        prompt = [{"role": "system", "content": system_message}]
        for message in queryset[:history_length][::-1]:
            content = message.content
            sender = "assistant" if message.sender == "ai" else "user"
            prompt.append({"role":sender, "content":content})
        return prompt  

def get_ai_response(messages_queryset, model = "gpt-4.1", history_length = 10):
    return openai_client.respond(messages_queryset, model, history_length)

openai_client = OpenAIClient()