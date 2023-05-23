from django.shortcuts import render
from search.models import *
import requests
from bs4 import BeautifulSoup

from search_engine import settings as s #API_KEY

API_KEY = s.API_KEY


def bing_search(query, api_key =API_KEY, pignation_no = 0):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}

    params = {"q": query, "count": 10, "offset": pignation_no * 10}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        print("called")
        try:
            return result['webPages']['value']
        except:
            print(result)
            return []
    else:
        print("Unable to fetch, response status : ",response.status_code )
        return []
    
    
def bing_search_images(query, api_key ,  pignation_no = 0):
    url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 10, "offset": int(pignation_no) * 10, "imageType": "photo"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return []
    return response.json()


# def bing_news_search(query, api_key ,  pignation_no = 0):
#     url = "https://api.bing.microsoft.com/v7.0/news/search"
#     headers = {"Ocp-Apim-Subscription-Key": api_key}
#     params = {"q": query, "count": 10, "offset": int(pignation_no) * 10}
#     print("request bing for news")
#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         result = response.json()
#         return result
#     else:
#         print("error: ", response)
#         return []
def bing_news_search(query, api_key ,  pignation_no = 0):
    url = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 10, "offset": int(pignation_no) * 10 }
    print("request bing for news")
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print("error: ", response)
        return []




def bing_search_videos(query, api_key, offset=0):
    url = "https://api.bing.microsoft.com/v7.0/videos/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 50, "offset": offset, "responseFilter": "Video"}

    response = requests.get(url, headers=headers, params=params)
    return response.json()





# def bing_images(query):
#     image_url = f"https://www.bing.com/images/search?q={query}&setlang=en"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#     }
#     response = requests.get(image_url, headers=headers)
#     soup = BeautifulSoup(response.content, "html.parser")
#     search_results = soup.find_all("div", class_="imgpt")

#     # Create an empty list to store the image links
#     links = []

#     # Loop through the search results and get the src attribute of each img tag
#     for result in search_results:
#         img = result.find("img")
#         if img:
#             # Use a try-except block to handle the KeyError
#             try:
#                 link = img["src"]
#                 # Append the link to the list
#                 links.append(link)
#             except KeyError:
#                 # Skip the tag if it does not have a src attribute
#                 pass
#     return links