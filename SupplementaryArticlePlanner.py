import json
import openai
import multiprocessing

class SupplementaryArticlePlanner:
    def __init__(self, openai_key: str):
        self.openai_key = openai_key

    def generateSupplementaryArticles(self, topic: str):
        client = openai.Client(api_key=self.openai_key)
        # Get the top 5 related products for the proposed topic using an LLM. For example 'E-Bikes' would returne top e-bike battiers, top bike helmets, top bike tires
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": 'You are an online article planner. Your task is to generate a list of 10 supplementary articles to an e-commerce topic. For each article you should provide a title and a description. For example, the topic "e-bikes", you would generate articles such as "The Legality of E-Bikes" and "Taking a Bike vs Driving a Car". You should give your response in a JSON list of the following format: {"articles": [{"title": "Article1", "description": "Description1"}, {"title": "Article2", "description": "Description2"}, ...]}'
                },
                {
                    "role": "user",
                    "content": f"{topic}"
                }
            ],
            response_format={ "type": "json_object" },
            temperature=0
        )
        json_string = response.choices[0].message.content
        articles = json.loads(json_string)["articles"]
        return articles