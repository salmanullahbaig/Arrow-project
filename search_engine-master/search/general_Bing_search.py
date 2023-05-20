from django.shortcuts import render
from search.models import *
import requests
from bs4 import BeautifulSoup


def bing_search(query, api_key ='79407ee4a67041b5a12cbe23c684dbe5', pignation_no = 0):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}

    params = {"q": query, "count": 10, "offset": pignation_no * 10}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        print("called")
        return result['webPages']['value']
    else:
        list1 =[]
        return list1

def bing_images(query):
    image_url = f"https://www.bing.com/images/search?q={query}&setlang=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(image_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    search_results = soup.find_all("div", class_="imgpt")

    # Create an empty list to store the image links
    links = []

    # Loop through the search results and get the src attribute of each img tag
    for result in search_results:
        img = result.find("img")
        if img:
            # Use a try-except block to handle the KeyError
            try:
                link = img["src"]
                # Append the link to the list
                links.append(link)
            except KeyError:
                # Skip the tag if it does not have a src attribute
                pass
    return links