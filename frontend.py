import gradio as gr
import pandas as pd
import json
import markdown
import os

from orchestrator import fudgeBrownie

dummy_data = pd.read_json("final_table_format.json")


# Create a DataFrame from the articles in the folder
def createDataFrame(folder_path):
    articles = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as json_file:
            article = json.load(json_file)
            articles.append(article)

    return pd.DataFrame(articles)

# Save Content Plan to a folder
def saveContentPlan(articles, folder_path):
    # Create new folder for the product
    os.makedirs(folder_path)

    # Save articles 
    for article in articles.to_dict(orient="records"):
        file_path = os.path.join(folder_path, article["title"]+'.json')
        with open(file_path, 'w') as json_file:
            json.dump(article, json_file, indent=4)

def sourcesTomarkdown(sources):
    return "  \n".join([f"[{source['title']}]({source['link']})" for source in sources])
    

# Convert JSON article to markdown
def jsonArticleToHtml(json_article):
    return markdown.markdown(
        "## " + json_article["title"] + "  \n" +
        json_article["description"] + "  \n" +
        json_article["article_plan"] + "  \n" +
        "### Sources  \n"+
        sourcesTomarkdown(json_article["sources"])
    )


def generateArticles(Product, Article=None):
    folder_path = os.path.join(os.getcwd(), "ContentPlan", Product)
    print("Product: ", Product)

    if os.path.exists(folder_path):
        print("Folder exists")
        articles = createDataFrame(folder_path)
    else:
        articles = fudgeBrownie(Product)
        saveContentPlan(articles, folder_path)

    json_article = {}
    article = ""

    print("Articles:  ")
    print(articles)

    # Get article
    if Article:
        file_path = os.path.join(folder_path, Article+'.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                json_article = json.load(json_file)
                article = jsonArticleToHtml(json_article)

    return [articles[["title", "description"]].head(5).values.tolist(), json_article, article]

with gr.Blocks() as app:
    product = gr.Textbox(label="Product")
    article = gr.Textbox(label="Article")
    
    outputArticles = gr.DataFrame(
        headers=["Title", "Description"],
        type="pandas",
        label="Articles"
    )

    with gr.Row():
        outputArticleJson = gr.Json(label="Article JSON")
        outputArticle = gr.HTML(label="Article")

    process_btn = gr.Button("Request")
    process_btn.click(fn=generateArticles, inputs=[product,article], outputs=[outputArticles, outputArticleJson, outputArticle])

app.launch(share=True)