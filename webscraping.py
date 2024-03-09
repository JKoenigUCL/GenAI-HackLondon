from googleapiclient.discovery import build

# comment out / add hosts
block_list = ["reddit",
              "4chan"]


class Source_Finder:

    def __init__(self, API_KEY, CSE_ID, block_list):
        self.API_KEY = API_KEY
        self.CSE_ID = CSE_ID
        self.block_list = block_list

    def google_search(self, query, num=10):
        service = build("customsearch", "v1", developerKey=self.API_KEY)
        result = service.cse().list(
            q=query,
            cx=self.CSE_ID,
            num=num
        ).execute()
        return result['items']


    def filter_results(self, r):
        results = r.copy()
        for r in results:
            for b in block_list:
                if b in r['link']:
                    results.remove(r)
        return results


    def result_to_list(self, r):
        res = []
        for i in r:
            dictElem = {'title': i['title'], 'link': i['link']}
            res.append(dictElem)
        return res


    def find_sources(self, title, description):
        query = title + " " + description
        results = self.google_search(query)
        filtered = self.filter_results(results)
        return self.result_to_list(filtered)


## Example usage
API_KEY = ""
CSE_ID = ""
SF = Source_Finder(API_KEY, CSE_ID, block_list)
print(SF.find_sources("ELECTRIC BIKES: PROS AND CONS", "An article discussing the advantages and disadvantages of using E-bikes"))