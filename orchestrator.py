import ProductReviewFinder

class Orchestrator:
    def __init__(self, openai_key, asin_data_api_key):
        self.review_finder = ProductReviewFinder(openai_key, asin_data_api_key)

    def generate_product_reviews(self, topic):
        # Get the top products from Amazon
        top_products = self.review_finder.getAmazonTop(topic)

        # Generate related products using OpenAI
        related_products = self.review_finder.generateRelatedProducts(topic)

        # Create a list of product reviews with descriptions
        product_reviews = self.review_finder.createArticleList(topic)

        # Combine the top products, related products, and product reviews
        combined_data = []
        for product, review in zip(top_products, product_reviews):
            product_data = {
                'title': product['title'],
                'review_title': review['title'],
                'review_description': review['description'],
                'related_products': related_products
            }
            combined_data.append(product_data)

        return combined_data

    def run(self, topic):
        # Execute the entire workflow
        product_data = self.generate_product_reviews(topic)

        # Process or display the product_data as needed
        openai_key = 'your_openai_key'
        asin_data_api_key = 'your_asin_data_api_key'

        orchestrator = Orchestrator(openai_key, asin_data_api_key)
        topic = 'E-Bikes'
        product_data = orchestrator.run(topic)

        # Print the product data
        for data in product_data:
            print(f"Title: {data['title']}")
            print(f"Review Title: {data['review_title']}")
            print(f"Review Description: {data['review_description']}")
            print(f"Related Products: {', '.join(data['related_products'])}")
            print("---")

        return product_data