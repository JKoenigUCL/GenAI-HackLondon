## Python class that finds sources for artciles based on article title and description
import openai

OPENAI_API_KEY = "HA HA"

client = openai.Client(api_key=OPENAI_API_KEY)


def source_finder(title, description):
    """
    :param title: title of article
    :param description: description of article
    :return: json formated list of [ (link,title) ]

    """
    bike_promt = (f"Generate a search query based on the title: 'ELECTRIC BIKES: PROS AND CONS' and description: "
                  f"'An article discussing the advantages and disadvantages of using E-bikes' ."
              f" Please return the results as a list of json objects with attributes title and link ")


    bike_output = (
        "[ {'title':'ELECTRIC BIKES: PROS AND CONS' , 'link' : "
        "'https://evelo.com/blogs/ebike-buyers-guide/electric-bikes-pros-and-cons'},"
        "{'title':'The Main Advantages and Disadvantages of Electric Bikes' , 'link' : "
        "'https://www.velospeed.co.uk/advantages-and-disadvantages-of-electric-bikes/'}]")

    prompt = (f"Generate a search query based on the title: '{title}' and description: '{description}'."
              f" Please return the results as a list of json objects with attributes title and link ")

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": " I am building an app that finds relevant sources given an article title and description."
                           "Return the results as a JSON response with a list of link lists, where each inner list "
                           "contains the title and URL of a relevant page."

            },
            {
                "role": "user",
                "content": bike_promt
            },
            {
                "role": "assistant",
                "content": bike_output
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    # Extract search query from model response
    json_string = response.choices[0].message.content
    return json_string
