from ProductReviewFinder import ProductReviewFinder
from SupplementaryArticlePlanner import SupplementaryArticlePlanner
from webscraping import Source_Finder

# comment out / add hosts
block_list = ["reddit",
              "4chan"]


class Orchestrator:
    def __init__(self, openai_key, asin_data_api_key, google_api_key, cse_id, block_list):
        self.product_review_finder = ProductReviewFinder(openai_key, asin_data_api_key)
        self.supplementary_article_planner = SupplementaryArticlePlanner(openai_key)
        self.source_finder = Source_Finder(google_api_key, cse_id, block_list)

    def orchestrate(self, topic):
        article_list = self.product_review_finder.createArticleList(
            topic) + self.supplementary_article_planner.generateSupplementaryArticles(topic)

        # {"title": "Article1", "description": "Description1"}

        for (i, article) in enumerate(article_list):
            title, description = article["title"], article["description"]
            sources = self.source_finder.find_sources(title, description)
            article_list[i] = article.update["sources": sources]

        return article_list



o = Orchestrator(openAI_key, asin_key, google_key, cse_id, block_list)
topic = "E-Bikes"
articles = o.orchestrate(topic)
print(topic)