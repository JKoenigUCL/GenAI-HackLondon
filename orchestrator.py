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


    def run(self, topic: str) -> List[Dict]:
        product_reviews = self.product_review_finder.createArticleList(topic)
        supplementary_articles = self.supplementary_article_planner.generateSupplementaryArticles(topic)

        all_articles = product_reviews + supplementary_articles

        articles_with_sources = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i, article in enumerate(all_articles):
                future = executor.submit(self.source_finder.find_sources, article["title"], article["description"])
                futures.append((future, article, i))
            for future, article, i in futures:
                sources = future.result()
                article["sources"] = sources
                article["index"] = i  # Add the index to the article dictionary
                articles_with_sources.append(article)

        articles_with_sources = list(articles_with_sources)  # Convert to list

        planned_articles = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for article in articles_with_sources:
                future = executor.submit(self.article_plan_generator.generateSupplementaryArticles, article["title"], article["description"])
                futures.append((future, article))
            for future, article in futures:
                article_plan = future.result()
                article["article_plan"] = article_plan
                planned_articles.append(article)

        return planned_articles

# Example usage
if __name__ == "__main__":

    orchestrator = Orchestrator(openai_key, asin_data_api_key, google_api_key, cse_id)

    topic = "E-Bikes"
    articles_with_sources = orchestrator.run(topic)

    # Print the articles with sources
    for article in articles_with_sources:
        print(f"Index: {article['index']}")
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"Sources: {article['sources']}")
        print("---")