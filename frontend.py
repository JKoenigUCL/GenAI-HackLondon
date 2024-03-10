import streamlit as st
import pandas as pd
import json
import markdown2 as markdown
import os
import re

from orchestrator import Orchestrator
from api_secrets import SecretManager

secrets = SecretManager()
orchestrator = Orchestrator(secrets.openai_key, secrets.asin_data_api_key, secrets.google_api_key, secrets.cse_id)

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
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for article in articles.to_dict(orient="records"):
        file_path = os.path.join(folder_path, article["title"] + '.json')
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
        "### Sources  \n" +
        sourcesTomarkdown(json_article["sources"])
    )

def generateArticles(Product, Article=None):
    folder_path = os.path.join(os.getcwd(), "ContentPlan", Product)
    st.write("Product: ", Product)

    if os.path.exists(folder_path):
        # st.write("Folder exists")
        articles = createDataFrame(folder_path)
    else:
        with st.status("Orchestrating Content...", expanded=True) as status:
            st.write("Generating Content Plan...")
            orchestrator.generateContentPlan(Product)
            st.write("Finding Article Sources...")
            orchestrator.addSources()
            st.write("Writing Article Plans...")
            planned_articles = orchestrator.planArticles()
            st.write("Saving...")
            for article in planned_articles:
                article["title"] = re.sub(r'[\\/*?:"<>|]', '', article["title"])

            articles = pd.DataFrame(planned_articles)
            saveContentPlan(articles, folder_path)
            status.update(label="Orchestration Complete", state="complete", expanded=False)


    # Re order the articles so that all articles that start with review are last
    articles = articles.sort_values(by="title", key=lambda x: x.str.startswith("Review"))
    return articles[["title", "description", "article_plan", "sources"]]

# This function displays the article details correctly by using a unique identifier
def show_article_details(article_title, articles):
    selected_article = articles.loc[articles['title'] == article_title].iloc[0]
    st.markdown("### Description")
    st.markdown(selected_article['description'])
    st.markdown("## Article Plan")
    st.markdown(selected_article['article_plan'])
    st.markdown("## Sources")
    st.markdown(sourcesTomarkdown(selected_article['sources']))

# Improved function to display articles as cards and handle selection
def display_articles_as_cards(articles):
    cols_per_row = 3
    for i in range(0, len(articles), cols_per_row):
        cols = st.columns(cols_per_row)
        for idx, col in enumerate(cols):
            if i+idx < len(articles):
                article = articles.iloc[i+idx]
                with col:
                    st.markdown(f"### {article['title']}")
                    st.write(f"{article['description']}")
                    show_more_key = f"show_more_{i+idx}"  # Unique key for each button
                    if st.button("Show more", key=show_more_key):
                        # Store the title of the selected article as a unique identifier
                        st.session_state['selected_article_title'] = article['title']
                        # Rerun to show the selected article
                        st.rerun()

product = st.text_input("Product")

if product:
    articles = generateArticles(product)
    st.session_state['articles'] = articles

    if 'selected_article_title' not in st.session_state:
        st.session_state['selected_article_title'] = ""

    if st.session_state['selected_article_title'] == "":
        # Display articles in a card-like format
        display_articles_as_cards(articles)
    else:
        # Show enlarged article details based on the selected article's title stored in session state
        show_article_details(st.session_state['selected_article_title'], articles)

        if st.button("Back"):
            # Clear the selected article title to return to the card view
            st.session_state['selected_article_title'] = ""
            # Rerun to show the card view
            st.rerun()
