"""Create a plasmid template string, which will get converted to a sequence by string_to_sequence.py
What are the choices that we need to make?

Create plasmid template string
- First, identify gene responsible for the behavior that the user wants and the target organism.
- Second, identify the relevant plasmid backbone
- Choose the best restriction enzyme to use at the MCS
- Choose the relevant promoter

GENE-BACKBONE-RESTRICTION_ENZYME-PROMOTER

Choose recepient strain and create experiment annotation to pass to next step.
"""

# How do we configure the action set?
from openai import OpenAI
import requests


client = OpenAI(api_key="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")


def gpt_call(query, string):
    # Grab context from file
    with open(string, 'r') as file:
        context = file.read()

    completion = client.chat.completions.create(
        model="gpt-4-0613",
        temperature=0,  # Change to mess with determinism
        messages=[
            {"role": "system",
             "content": context},
            {"role": "user", "content": query}
        ]
    )
    return completion.choices[0].message.content


def novelty_check(query):
    # Base URL for Semantic Scholar API
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # Parameters for the API call
    params = {
        "query": query,
        "fields": "title,abstract,authors,year",
        "limit": 5  # Number of results to return (can be adjusted)
    }

    # Make the request to the API
    response = requests.get(base_url, params=params)

    # Initialize an empty string to store the results
    result_string = ""

    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        if results.get("data"):
            result_string += f"Found {len(results['data'])} papers related to the query '{query}':\n\n"
            for i, paper in enumerate(results['data']):
                result_string += f"{i + 1}. Title: {paper['title']}\n"
                result_string += f"   Authors: {', '.join([author['name'] for author in paper['authors']])}\n"
                result_string += f"   Year: {paper['year']}\n\n"
        else:
            result_string += f"No relevant papers found for the query '{query}'.\n"
    else:
        result_string += f"Failed to fetch data from Semantic Scholar API. Status code: {response.status_code}\n"

    return result_string


sequence_string = gpt_call("Create a plasmid to make E. Coli synthesize insulin", "string_assembly.txt")
annotation = gpt_call(sequence_string, "design_reasoning.txt")
abstract = gpt_call(sequence_string, "experiment_abstract.txt")
ss_results = novelty_check("test")

# Now pass this to semantic scholar and to a check in literature


print(sequence_string + "\n" + annotation)
