from flask import Flask, jsonify, request
import asyncio
import logging
import favicon
from duckduckgo_search import AsyncDDGS
import json
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to my API'



async def aget_results(query,region,safesearch,timelimit):
    results = await AsyncDDGS(proxy=None).text(query,region=region, safesearch=safesearch, timelimit=timelimit, max_results=5)
    return results

@app.route('/api/search/', methods=['POST'])
async def search():
    data = request.json
    query = data.get('query')
    region = data.get('region')
    safesearch = data.get('safesearch')
    timelimit = data.get('timelimit')
    
    
    url = "https://google.serper.dev/search"

    payload = json.dumps({
    "q": query,
    "location": "Paris, Paris, Ile-de-France, France",
    "gl": "fr"
    })
    headers = {
    'X-API-KEY': 'a03f57dd9d8efebe0c765fc7d49b13cc40dc30bc',
    'Content-Type': 'application/json'
    }
    modified_results = []

    response = requests.request("POST", url, headers=headers, data=payload)
    searchresult=response.text
    results = await aget_results(query,region,safesearch,timelimit)
    data = json.loads(searchresult)

    # Separate into three different arrays
    search_parameters = data.get('searchParameters', {})
    knowledge_graph = data.get('knowledgeGraph', {})
    organic_results = data.get('organic', [])
    related_searches = data.get('relatedSearches', [])

    # Print separated arrays
    print("Search Parameters:", search_parameters)
    print("\nKnowledge Graph:", knowledge_graph)
    print("\nOrganic Results:", organic_results)
    print("\nRelated Searches:", related_searches)
    
    
    return jsonify(searchresult)
   


@app.route('/api/images/', methods=['POST'])
async def image():
    data = request.json
    query = data.get('query')
    region = data.get('region')
    safesearch = data.get('safesearch')
    timelimit = data.get('timelimit')
    results = await AsyncDDGS().images(query, region=region,timelimit=timelimit, safesearch=safesearch, max_results=20)
    print(results)
    return results



async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Run the Flask app within an asynchronous event loop
    loop = asyncio.get_event_loop()
    loop.create_task(app.run(debug=True))

if __name__ == '__main__':
    asyncio.run(main())
