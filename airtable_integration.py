# class supposed to get articles from frontend and save them to airtable
import json
import requests

class AirTableManager:
    def __init__(self, aritable_base_id, airtable_id, airtable_personal_access_token):
        self.airtable_base_id = aritable_base_id
        self.airtable_id = airtable_id
        self.airtable_personal_access_token = airtable_personal_access_token

    def saveArticles(self, articleList: list):
        dataJson = articleList

        url = f"https://api.airtable.com/v0/app{self.airtable_base_id}/tbl{self.airtable_id}"

        headers = {
            "Authorization": f"Bearer {self.airtable_personal_access_token}",
            "Content-Type": "application/json"
        }

        data = {"records": []}
        for article in dataJson:
            temp = {
                "fields": {
                    "Name": article["title"],
                    "Description": article["description"],
                    "Article Plan": article["article_plan"]
                }
            }
            data["records"].append(temp)

        response = requests.post(url, headers=headers, data=json.dumps(data))
        # check if the request was successful
        if response.status_code == 200:
            print("Success")
        else:
            print(f"Failed to save articles to Airtable. \
            Status code: {response.status_code}, Response: {response.text}")

