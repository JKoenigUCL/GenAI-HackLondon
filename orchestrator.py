# orchestrator class
from ProductReviewFinder import ProductReviewFinder
from webscraping import Source_Finder


class Orchestrator:

    def __init__(self, OpenAI_API_KEY, asin_data_api_key, Google_API_KEY, CSE_ID, block_list):
        self.product_review_finder = ProductReviewFinder(OpenAI_API_KEY, asin_data_api_key)
        self.source_finder = Source_Finder(Google_API_KEY, CSE_ID, block_list)

