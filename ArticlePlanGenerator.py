import openai
import json

class ArticlePlanGenerator:
    """"""

    def __init__(self, openai_key: str):
        self.client = openai.Client(api_key=openai_key)

    def generateSupplementaryArticles(self, title: str, description: str):
        # Get the top 5 related products for the proposed topic using an LLM. For example 'E-Bikes' would returne top e-bike battiers, top bike helmets, top bike tires
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'Create a markdown article plan for an article titled "{title}", about "{description}". The article should have a title and subheadings for each section. Under each subheading should be a brief description of the content that should be in that section'
                }
            ],
            temperature=0.5
        )
        article_plan = response.choices[0].message.content
        return article_plan
    
if __name__ == "__main__":
    openai_key = "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"
    article_planner = ArticlePlanGenerator(openai_key)
    article_plan = article_planner.generateSupplementaryArticles("Tablet vs Laptop: Choosing the Right Device for Your Needs", "Compare the advantages and limitations of tablets and laptops to help you decide which device is better suited for your specific tasks and preferences.")
    print(article_plan)
