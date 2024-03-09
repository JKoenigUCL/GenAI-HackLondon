from ProductReviewFinder import ProductReviewFinder
from SupplementaryArticlePlanner import SupplementaryArticlePlanner
from ArticlePlanGenerator import ArticlePlanGenerator
from webscraping import Source_Finder
from typing import List, Dict
import pandas as pd

block_list = ["reddit", "4chan"]

class Orchestrator:
    def __init__(self, openai_key, asin_data_api_key, google_api_key, cse_id):
        self.product_review_finder = ProductReviewFinder(openai_key, asin_data_api_key)
        self.supplementary_article_planner = SupplementaryArticlePlanner(openai_key)
        self.source_finder = Source_Finder(google_api_key, cse_id, block_list)
        self.article_plan_generator = ArticlePlanGenerator(openai_key)


    def run(self, topic: str) -> List[Dict]:
        product_reviews = self.product_review_finder.createArticleList(topic)
        supplementary_articles = self.supplementary_article_planner.generateSupplementaryArticles(topic)

        all_articles = product_reviews + supplementary_articles

        articles_with_sources = []
        for i, article in enumerate(all_articles):
            sources = self.source_finder.find_sources(article["title"], article["description"])
            article["sources"] = sources
            article["index"] = i  # Add the index to the article dictionary
            articles_with_sources.append(article)

        articles_with_sources = list(articles_with_sources)  # Convert to list

        planned_articles = []
        for article in articles_with_sources:
            article_plan = self.article_plan_generator.generateSupplementaryArticles(article["title"], article["description"])
            article["article_plan"] = article_plan
            planned_articles.append(article)

        return planned_articles

def fudgeBrownie(topic):

    orchestrator = Orchestrator(openai_key, asin_data_api_key, google_api_key, cse_id)
    articles_with_sources = orchestrator.run(topic)

    # Print the articles with sources
    for article in articles_with_sources:
        print(f"Index: {article['index']}")
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"Sources: {article['sources']}")
        print("---")
    
    return pd.DataFrame(articles_with_sources)