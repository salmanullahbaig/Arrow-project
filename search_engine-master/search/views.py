from django.shortcuts import render
from search.models import *
from search.models import Main_sites 

import requests
from bs4 import BeautifulSoup
from search.general_Bing_search import *
from django.core.paginator import Paginator
from search.custom_search import *
from search.general_Bing_search import bing_search_images , bing_news_search , bing_search_videos

from search_engine import settings as s #API_KEY
from search.self_indexing import I_search
from search.ElasticSearch import elasticsearch_images,elasticsearch_news,elasticsearch_web

bing_api_key = s.API_KEY 
API_KEY = s.API_KEY
import urllib

def index(request):
    return render(request, 'index.html',locals())


import urllib

def sort_by_url_order(result):
    for i, base_url in enumerate(all_sites):  # all_sites should be list of all URLs
        if isinstance(base_url, str) and result['url'].startswith(base_url):
            return i
    return len(all_sites)


def filter_results(search_results):
    visited_domains = set()
    filtered_results = []
    result_to_add_end = []

    for result in search_results:
        domain  = urllib.parse.urlparse(result['url']).hostname # get_domain(result['url'])
        if domain not in visited_domains:
            visited_domains.add(domain)
            filtered_results.append(result)
        else:
            result_to_add_end.append(result)
    return filtered_results + result_to_add_end


def search(request):
    query = request.GET.get('q') or request.POST.get('query')
    Searches.objects.create(query=query)
    # Get the current page number from the GET parameters
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 0
    #print("dir(request) = ",dir(request))
    #print("query = ",query)
    if 'B:' in query or 'b:' in query:
        # Do something if the query has B:
        print('Query has B:',query)
        query = query.replace('B:', '')
        query = query.replace('b:', '')
        print("page_number",page_number)
        bing_results = bing_search(query,pignation_no=int(page_number))
        print("number of results ", len(bing_results))
        # Set the number of results per page
        results_per_page = 1
        # Create a paginator object
        paginator = Paginator(bing_results, results_per_page)
        # Get the results for the current page
        page_obj = paginator.get_page(page_number)
        #bing_results = page_obj
        direct_bing = "Direct bing"
        if not query.startswith('B:'):
            query = f'B:{query}'
        return render(request, 'search.html', locals())
    elif 'I:' in query or 'i:' in query:
        query = query.replace('I:', '')
        query = query.replace('i:', '')
        top_n = 20
        results = I_search(query, top_n)
            # Set the number of results per page
        results_per_page = 5

            # Create a paginator object
        paginator = Paginator(results, results_per_page)

            # Get the current page number from the GET parameters
        page_number = request.GET.get('page')

            # Get the results for the current page
        page_obj = paginator.get_page(page_number)
        results = page_obj
        limite_I = "Limited I: search"
        if not query.startswith('I:'):
            query = f'I:{query}'
        return render(request, 'search.html', locals())
    elif 'E:' in query or 'e:' in query:
        query = query.replace('E:', '')
        query = query.replace('e:', '')

        res = elasticsearch_web(query)

        #sort url
        all_results = []
        for hit in res['hits']['hits']:
            hit_data = {"url": hit['_source']['url'], "title": hit['_source']['title'],
                        "content": hit['_source']['snippet'] + '...',  # Limit content to 100 characters
                        "timestamp": hit['_source']['time']
                        }
            all_results.append(hit_data)

        sorted_results = sorted(all_results, key=sort_by_url_order)  # all_results should be list of dict of results
        hits = filter_results(sorted_results)



        # # Process search results
        # hits = []
        # for hit in res['hits']['hits']:
        #     hit_data = {
        #         "url": hit['_source']['url'],
        #         "title": hit['_source']['title'],
        #         "content": hit['_source']['content'][:100] + '...',  # Limit content to 100 characters
        #         "timestamp": hit['_source']['time']
        #     }
        #     hits.append(hit_data)




        # for hit in res['hits']['hits']:
        #     print(f"URL: {hit['_source']['url']}")
        #     print(f"Title: {hit['_source']['title']}")
        #     print(f"Content: {hit['_source']['content'][:100]}...")  # print the first 100 characters
        #     print(f"Timestamp: {hit['_source']['time']}")
        #     print("===============================================")

        Elasticsearch = "Elastic search"
        if not query.startswith('E:'):
            query = f'E:{query}'
        return render(request, 'search.html', locals())



    # elif 'c:' in query or ':'  not in query:
    #     # Get the current page number from the GET parameters
    #     results_concurrent = concurrent_search(query, all_sites, bing_search_custom, max_workers=len(all_sites))
    #
    #     all_results = []
    #     for site_group in results_concurrent:
    #         try:
    #             #print(len(site_group["webPages"]["value"]))
    #             all_results.extend(site_group["webPages"]["value"])
    #         except:
    #             pass
    #
    #     url_order = []
    #     [[url_order.append(x) for x in group] for group in all_sites if group]
    #
    #
    #     def sort_by_url_order(result):
    #         for i, base_url in enumerate(url_order):
    #             if result['url'].startswith(base_url):
    #                 return i
    #         return len(url_order)
    #
    #     sorted_results = sorted(all_results, key=sort_by_url_order)
    #     main_words_list = get_main_words(query)
    #     main_words = ' '.join(main_words_list)
    #     # # Replace with your search function, e.g., bing_search or google_search
    #     results = sorted_results
    #     # # Filter the results by relevance
    #     relevance_threshold = 1
    #     filtered_results = filter_results_by_relevance(results, main_words, relevance_threshold)
    else:
        results_concurrent = search_custom_web_concurrent_search(query, all_sites, search_custom_web,
                                                                 max_workers=len(all_sites))

        all_results = []
        for site_group in results_concurrent:
            try:
                all_results.extend(site_group["webPages"]["value"])
            except:
                pass

        sites = [{'url': x['url'], 'displayUrl': x['displayUrl'], 'name': x['name'], 'snippet': x['snippet']} for x in all_results]
        for i in sites:
            print("URL:", i['url'])
            print("displayUrl:", i['displayUrl'])
            print("name:", i['name'])
            print("snippet:", i['snippet'])
            print()

    return render(request, 'search.html', locals())



def google_images_search(request,query):
    bing_api_key = API_KEY

    if 'B:' in query or "b:" in query:
        query = query.replace('B:', '')

        # Get the current page number from the GET parameters
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 0
        bing_api_key = API_KEY  # Replace with your Bing API key
        print("searching bing for images")
        bing_results = bing_search_images(query, bing_api_key,pignation_no=int(page_number))
        print("Got the results")
        print(bing_results)
        images = []
        if len(bing_results['value']) > 0:
            for image in bing_results['value']:
                images.append({'url': image['thumbnailUrl'], 'hostUrl': image['hostPageUrl']})
        else:
            for image in bing_results['queryExpansions']:
                images.append({ 'url': image['thumbnail']['thumbnailUrl'] , 'hostUrl': image['webSearchUrl'] })
    
        print(len(images))
        #print(images)

        # Set the number of results per page
        results_per_page = 1
        # Create a paginator object
        paginator = Paginator(images, results_per_page)
        # Get the results for the current page
        page_obj = paginator.get_page(page_number)



        #bing_result_images = bing_images(query)
        #print("bing_result_images", bing_result_images)
        direct_bing = "Direct bing"
        if not query.startswith('B:'):
            query = f'B:{query}'
        return render(request, 'google_images_search.html', locals())
    elif 'E:' in query or 'e:' in query:
        query = query.replace('E:', '')
        query = query.replace('e:', '')

        res = elasticsearch_images(query)
        # Process image search results
        hits = []
        for hit in res["hits"]["hits"]:
            hit_data = {
                "title": hit["_source"]["title"],
                "url": hit["_source"]["url"],
                "host_url": hit["_source"]["hostUrl"]
            }
            hits.append(hit_data)
        # for hit in res["hits"]["hits"]:
        #     print(hit["_source"]["title"])
        #     print(hit["_source"]["url"])
        #     print(hit["_source"]["hostUrl"])

        Elasticsearch = "Elastic search"
        if not query.startswith('E:'):
            query = f'E:{query}'
        return render(request, 'google_images_search.html', locals())
    elif 'I:' in query or 'i:' in query:
        query = query.replace('I:', '')
        query = query.replace('i:', '')
        top_n = 20
        results = I_search(query, top_n)
        # Convert the results to a list of lists
        results = [list(result) for result in results]

        # Convert the image URLs to strings
        for result in results:
            title, url, snippet, video_src, image_url, similarity_score = result
            if isinstance(image_url, list):
                result[4] = image_url[0] if image_url else None
            else:
                result[4] = image_url

        # Print the modified results
        for result in results:
            print("Title:", result[0])
            print("URL:", result[1])
            print("Snippet:", result[2])
            print("Video Source:", result[3])
            print("Image URL:", result[4])
            print("Similarity Score:", result[5])
            print()  # Adding an empty line for better readability

        if not query.startswith('I:'):
            query = f'I:{query}'
        limite_I = "Limited I: search"
        return render(request, 'google_images_search.html', locals())
    else:
        # query = "apple"
        results_concurrent = concurrent_search_for_custom_images_search(query, all_sites, custom_search_images,max_workers=len(all_sites))

        all_results = []
        for site_group in results_concurrent:
            try:
                all_results.extend(site_group["value"])
            except:
                pass

        images = [{'url': x['contentUrl'], 'hostUrl': x['hostPageUrl']} for x in all_results]

        # for image in images:
        #     print("Image URL:", image['url'])
        #     print("Host URL:", image['hostUrl'])
        #     print()  # Adding an empty line for better readability

    return render(request, 'google_images_search.html', locals())




def videos(request,query):
    #videos
    #video_results = get_video_results(query)
    if 'B:' in query or 'b:' in query:
        query = query.replace('B:', '')
        global API_KEY
        bing_api_key = API_KEY  # Replace with your Bing API key
        videos = []
        page_number = int(request.GET.get('page', 1))

        # Call Bing API with pagination
        for offset in range((page_number - 1) * 50, page_number * 50, 50):
            bing_results = bing_search_videos(query, bing_api_key, offset)
            print("bing_results v ",bing_results)
            for item in bing_results.get("value", []):
                name = item["name"]
                url = item["contentUrl"]
                videos.append({"name": name, "url": url})
        print(videos)
        # Use Django's built-in paginator to paginate the results
        paginator = Paginator(videos, 10)
        page_obj = paginator.get_page(page_number)

        direct_bing = "Direct bing"
        if not query.startswith('B:'):
            query = f'B:{query}'
        return render(request, 'videos.html', locals())
    elif 'I:' in query or 'i:' in query:
        query = query.replace('I:', '')
        query = query.replace('i:', '')
        top_n = 20
        results = I_search(query, top_n)
        print("results : ",results)
        filtered_results = []

        for result in results:
            title, url, snippet, video_src, image_url, similarity_score = result
            try:
                if video_src.startswith("https"):
                    filtered_results.append(result)
            except:
                pass
        if not query.startswith('I:'):
            query = f'I:{query}'
        limite_I = "Limited I: search"
        return render(request, 'videos.html', locals())
    else:
        # bing_api_key = API_KEY  # Replace with your Bing API key
        # videos = []
        # page_number = int(request.GET.get('page', 1))
        #
        # # Call Bing API with pagination
        # for offset in range((page_number - 1) * 50, page_number * 50, 50):
        #     bing_results = bing_search_videos(query, bing_api_key, offset)
        #     print("bing_results v ", bing_results)
        #     for item in bing_results.get("value", []):
        #         name = item["name"]
        #         url = item["contentUrl"]
        #         videos.append({"name": name, "url": url})
        # print(videos)
        # # Use Django's built-in paginator to paginate the results
        # paginator = Paginator(videos, 10)
        # page_obj = paginator.get_page(page_number)

        x_sites = []
        for x in all_sites:
            for y in x: x_sites.append(y)

        results_concurrent = concurrent_search_custom_search_for_videos(query, [x_sites], custom_search_for_videos,
                                                                        max_workers=len([0]))

        all_results = []
        for site_group in results_concurrent:
            try:
                all_results.extend(site_group["value"])
            except:
                pass
        custom_videos = [{'url': x['contentUrl'], 'hostUrl': x['hostPageUrl'], 'name': x['name']} for x in all_results]

        for image in custom_videos:
            print("name  URL:", image['name'])
            print("video  URL:", image['url'])
            print("video URL:", image['hostUrl'])
            print()  # Adding an empty line for better readability


    return render(request, 'videos.html', locals())



def news(request , query):
    #query = request.GET.get('q') or request.POST.get('query')
    bing_api_key = "a43dbec193c74e6f9d2041820d7dd47e"

    Searches.objects.create(query=query)
    #print("dir(request) = ",dir(request))
    #print("query = ",query)
    if 'B:' in query or 'b:' in query:
        # Do something if the query has B:
        print('Query has B:',query)
        query = query.replace('B:', '')
        query = query.replace('b:', '')

        # Get the current page number from the GET parameters
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 0
        print("page_number",page_number)
        bing_results = bing_news_search(query,    bing_api_key  , pignation_no=int(page_number))
        news_list = []
        print(bing_results)
        if len(bing_results) != 0:
            for new in bing_results['value']:
                news_list.append({ 'name': new['name'] , 'url': new['url'] , 'description': new['description'] })

        bing_results = news_list 
        print(len(bing_results))
        # Set the number of results per page
        results_per_page = 1
        # Create a paginator object
        paginator = Paginator(bing_results, results_per_page)
        # Get the results for the current page
        page_obj = paginator.get_page(page_number)
        #bing_results = page_obj


        direct_bing = "Direct bing"
        if not query.startswith('B:'):
            query = f'B:{query}'
        return render(request, 'news.html', locals())
    elif 'E:' in query or 'e:' in query:
        query = query.replace('E:', '')
        query = query.replace('e:', '')

        res = elasticsearch_news(query)

        # sort url
        all_results = []
        for hit in res['hits']['hits']:
            hit_data = {"url": hit['_source']['url'], "title": hit['_source']['title'],
                        "content": hit['_source']['snippet'] + '...',  # Limit content to 100 characters
                        "timestamp": hit['_source']['time']
                        }
            all_results.append(hit_data)

        sorted_results = sorted(all_results, key=sort_by_url_order)  # all_results should be list of dict of results
        hits = filter_results(sorted_results)
        print(hits)

        # # Process news search results
        # hits = []
        # for hit in res["hits"]["hits"]:
        #     snippet = hit["_source"]["snippet"]
        #     snippet_words = snippet.split()[:20]  # Limit to the first 50 words
        #     snippet_shortened = " ".join(snippet_words)
        #
        #     hit_data = {
        #         "title": hit["_source"]["title"],
        #         "url": hit["_source"]["url"],
        #         "snippet": snippet_shortened
        #     }
        #     hits.append(hit_data)

        Elasticsearch = "Elastic search"
        if not query.startswith('E:'):
            query = f'E:{query}'
        return render(request, 'news.html', locals())
    elif 'I:' in query or 'i:' in query:
        query = query.replace('I:', '')
        query = query.replace('i:', '')
        top_n = 20
        results = I_search(query, top_n)
        # Set the number of results per page
        results_per_page = 5

        # Create a paginator object
        paginator = Paginator(results, results_per_page)

        # Get the current page number from the GET parameters
        page_number = request.GET.get('page')

        # Get the results for the current page
        page_obj = paginator.get_page(page_number)
        results = page_obj
        limite_I = "Limited I: search"
        if not query.startswith('I:'):
            query = f'I:{query}'
        return render(request, 'news.html', locals())
    else:
        # # Get the current page number from the GET parameters
        # results_concurrent = concurrent_search(query, all_sites, bing_search_custom, max_workers=len(all_sites))
        #
        # all_results = []
        # for site_group in results_concurrent:
        #     try:
        #         #print(len(site_group["webPages"]["value"]))
        #         all_results.extend(site_group["webPages"]["value"])
        #     except:
        #         pass
        # url_order = []
        # [[url_order.append(x) for x in group] for group in all_results]
        #
        # def sort_by_url_order(result):
        #     for i, base_url in enumerate(url_order):
        #         if result['url'].startswith(base_url):
        #             return i
        #     return len(url_order)
        #
        # sorted_results = sorted(all_results, key=sort_by_url_order)
        # main_words_list = get_main_words(query)
        # main_words = ' '.join(main_words_list)
        # # # Replace with your search function, e.g., bing_search or google_search
        # results = sorted_results
        # # # Filter the results by relevance
        # relevance_threshold = 1
        # filtered_results = filter_results_by_relevance(results, main_words, relevance_threshold)

        results_concurrent = concurrent_search_custom_news_search(query, [news_sites], custom_news_search,
                                                                  max_workers=len([0]))

        all_results = []
        for site_group in [results_concurrent]:
            try:
                # print(len(site_group["webPages"]["value"]))
                all_results.extend(site_group["webPages"]["value"])
            except:
                pass

        url_order = []
        [[url_order.append(x) for x in group] for group in news_sites if group]

        # results_concurrent[0]['webPages']['value']

        # for result in results_concurrent[0]['webPages']['value']:
        #     print("Name:", result['name'])
        #     print("URL:", result['url'])
        #     print("Snippet:", result['snippet'])
        #     print("Display URL:", result['displayUrl'])
        #     print()  # Adding an empty line for better readability
        custom_s = "Custom Search"

    return render(request, 'news.html', locals())




##########################################################################################################
                    #Elastic search



# Import the Elasticsearch library
#Elasticsearch(['406fe72a0b1e4a979516909b134d4e98'])
from elasticsearch import Elasticsearch
from dateutil import parser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures

# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = "aOId1OZ0SEYyJ2HW52XEGRSl"

# Found in the 'Manage Deployment' page
CLOUD_ID = "Elastic_search_R:d2VzdHVzMi5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo0NDMkNDA2ZmU3MmEwYjFlNGE5Nzk1MTY5MDliMTM0ZDRlOTgkNDY2YzdhMTJlYzQ3NDUzNTlmNWYxZmRjYjg5YzBiOWM="

# Create the client instance
client = Elasticsearch(cloud_id=CLOUD_ID,basic_auth=("elastic", ELASTIC_PASSWORD))



def save_content_to_database(url , soup ):
    try : page_date = parser.parse(timestamp =soup.find('time').text)
    except: page_date=parser.parse('2021-1-1')
    client.index(index="websites", id=url, body={
        'url': url,
        "title": soup.title.text,
        "content": soup.text,
        'snippet' : ' '.join(soup.text.split()[:100]) ,
        "images": [image.get("src") for image in soup.find_all("img")],
        "videos": [video.get("src") for video in soup.find_all("video")],
        'time' : page_date,
     })

def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:save_content_to_database(url , soup)
            except Exception as e: print("Error in save data : ", e)
            return soup
        else:
            time.sleep(60)
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                try:save_content_to_database(url , soup)
                except Exception as e: print(f"Error in save data :  error {e}  and url {url} ")
                return soup
                print(f"Error {response.status_code}: Unable to fetch {url}")
    except Exception as e:
        print(f"Error: Unable to fetch {url} due to {e}")

def find_internal_links(soup, base_url):
    internal_links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not href.startswith('http') and not href.startswith('mailto'):
            full_url = urljoin(base_url, href)
            internal_links.add(full_url)
    return internal_links

def crawl_website(url, max_depth=3, current_depth=1):
    print(url)
    if current_depth > max_depth:
        return {}

    content_map = {}
    soup = get_page_content(url)
    if soup:
        content_map[url] = soup.get_text()
        #tile_map[url] = soup.find('title').get_text()
        internal_links = find_internal_links(soup, url)
        for link in internal_links:
            content_map.update(crawl_website(link, max_depth, current_depth + 1))

    return content_map


def concurrent_search( websites, search_fn, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        search_tasks = [executor.submit(search_fn,site,  max_depth = 100) for site in websites]
        results = [task.result() for task in futures.as_completed(search_tasks)]

    return results


def fetch(request):

    all_websites = get_sites()
    all_sites = []
    for group_websties in all_websites:
        for site in group_websties:
            all_sites.append(site)
    #all_sites = all_sites[:2]
    all_sites = [ "https://www." + x for x in all_sites]
    print("Fetching websites: ", all_sites)
    results_concurrent = concurrent_search(all_sites, crawl_website, max_workers= 20)
    return render(request, 'index.html',locals())

    



    
    
    