from ProductReviewFinder import ProductReviewFinder
from SupplementaryArticlePlanner import SupplementaryArticlePlanner
from webscraping import Source_Finder
from typing import List, Dict

block_list = ["reddit", "4chan"]

class Orchestrator:
    def __init__(self, product_review_finder, supplementary_article_planner, source_finder):
        self.product_review_finder = product_review_finder
        self.supplementary_article_planner = supplementary_article_planner
        self.source_finder = source_finder

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

        return articles_with_sources

# Example usage
if __name__ == "__main__":
    openai_key = ""
    asin_data_api_key = ""
    google_api_key = ""
    cse_id = ""

    product_review_finder = ProductReviewFinder(openai_key, asin_data_api_key)
    supplementary_article_planner = SupplementaryArticlePlanner(openai_key)
    source_finder = Source_Finder(google_api_key, cse_id, block_list)

    orchestrator = Orchestrator(product_review_finder, supplementary_article_planner, source_finder)

    topic = "E-Bikes"
    articles_with_sources = orchestrator.run(topic)

    # Print the articles with sources
    for article in articles_with_sources:
        print(f"Index: {article['index']}")
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"Sources: {article['sources']}")
        print("---")