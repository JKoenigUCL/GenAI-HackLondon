# class supposed to get articles from frontend and save them to airtable
from pyairtable import Api
from api_secrets import SecretManager
import json
import requests


class AirTable:
    def __init__(self):
        self.secrets = SecretManager()

    def saveArticle(self, article_json):
        self.airtable.create(article_json)

    def saveArticles(self):
        with open('final_table_format.json') as f:
            dataJson = json.load(f)
            # Replace with your actual API key
            api_key = self.secrets.airtable_personal_access_token

            url = f"https://api.airtable.com/v0/app{self.secrets.airtable_base_id}/tbl{self.secrets.airtable_id}"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {"records": []}
            for article in dataJson:
                temp = {
                    "fields": {
                        "Title": article["title"],
                        "Description": article["description"],
                        "Article Plan": article["article_plan"]
                    }
                }
                data["records"].append(temp)

            print(data)

            response = requests.post(url, headers=headers, data=data)

            # Check for successful response (optional)
            if response.status_code == 200:
                print("Article added successfully!")
            else:
                print(f"Error adding article: {response.text}")

            print(url)
            response = requests.post(url)
            print(response)



if __name__ == "__main__":
    airtable = AirTable()
    airtable.saveArticles()
