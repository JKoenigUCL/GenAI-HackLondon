from ProductReviewFinder import ProductReviewFinder
from SupplementaryArticlePlanner import SupplementaryArticlePlanner
from ArticlePlanGenerator import ArticlePlanGenerator
import concurrent.futures
from webscraping import Source_Finder
from typing import List, Dict

block_list = ["reddit", "4chan"]

class Orchestrator:
    def __init__(self, openai_key, asin_data_api_key, google_api_key, cse_id):
        self.product_review_finder = ProductReviewFinder(openai_key, asin_data_api_key)
        self.supplementary_article_planner = SupplementaryArticlePlanner(openai_key)
        self.source_finder = Source_Finder(google_api_key, cse_id, block_list)
        self.article_plan_generator = ArticlePlanGenerator(openai_key)
        self.review_articles = []
        self.supplementary_articles = []
        self.articles_with_sources = []

    def reset(self):
        self.review_articles = []
        self.supplementary_articles = []
        self.articles_with_sources = []

    def generateContentPlan(self, topic: str):
        self.review_articles = self.product_review_finder.createArticleList(topic)
        self.supplementary_articles = self.supplementary_article_planner.generateSupplementaryArticles(topic)

        return self.review_articles + self.supplementary_articles
    
    def addSources(self):
        articles_with_sources = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i, article in enumerate(self.supplementary_articles):
                future = executor.submit(self.source_finder.find_sources, article["title"], article["description"])
                futures.append((future, article, i))
            for future, article, i in futures:
                sources = future.result()
                article["sources"] = sources
                article["index"] = i  # Add the index to the article dictionary
                articles_with_sources.append(article)
        self.supplementary_articles = list(articles_with_sources)
        self.articles_with_sources = self.supplementary_articles + self.review_articles
        
        return self.articles_with_sources
    
    def planArticles(self):
        planned_articles = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for article in self.articles_with_sources:
                future = executor.submit(self.article_plan_generator.generateSupplementaryArticles, article["title"], article["description"])
                futures.append((future, article))
            for future, article in futures:
                article_plan = future.result()
                article["article_plan"] = article_plan
                planned_articles.append(article)

        return planned_articles

    def run(self, topic: str) -> List[Dict]:
        self.generateContentPlan(topic)
        self.addSources()
        return self.planArticles()