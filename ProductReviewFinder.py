import requests
import json
import pandas as pd
import openai

class ProductReviewFinder:
    """"""

    def __init__(self, openai_key: str, asin_data_api_key: str):
        self.client = openai.Client(api_key=openai_key)
        self.asin_data_api_key = asin_data_api_key

    def getAmazonTop(self, topic: str):
        # set up the request parameters
        params = {
            'api_key': f'{self.asin_data_api_key}',
            'type': 'search',
            'amazon_domain': 'amazon.co.uk',
            'search_term': f'{topic}',
            'sort_by': 'featured',
            'exclude_sponsored': 'false',
            'output': 'json'
        }

        # make the http GET request to ASIN Data API
        api_result = requests.get('https://api.asindataapi.com/request', params).json()

        return api_result["search_results"]

    def generateRelatedProducts(self, topic: str):
        # Get the top 5 related products for the proposed topic using an LLM. For example 'E-Bikes' would returne top e-bike battiers, top bike helmets, top bike tires
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": 'You are a related products generator. Please give me the top 5 related products for a provided topic. For example, "E-Bikes" would return top e-bike batteries, top bike helmets, top bike tires. "Smartphones" would return top smartphone cases, top smartphone chargers, top smartphone screen protectors. You should give your response in a JSON list of the following format: ["Product1", "Product2", "Product3", "Product4", "Product5"]'
                },
                {
                    "role": "user",
                    "content": "E-Bikes"
                },
                {
                    "role": "assistant",
                    "content": '{"related_products": ["Top E-Bike batteries", "Top E-Bike helmets", "Top E-Bike tires", "Top E-Bike chargers", "Top E-Bike locks"]}'
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
        related_products = json.loads(json_string)["related_products"]
        return related_products
    
    def createDescription(self, title):
        description = f'This is a product review of the {title}.'

        return description
    
    def createArticleList(self, topic):
        # Should return a DF with the title of the product review, the description, and the top 5 related products title's and descriptions
        top_products = self.getAmazonTop(topic)
        related_products = self.generateRelatedProducts(topic)
        product_reviews = []
        for product in top_products:
            title = f'Review of {product["title"]}'
            description = self.createDescription(title)
            product_reviews.append({'title': title, 'description': description})
