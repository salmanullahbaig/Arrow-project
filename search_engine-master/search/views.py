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

bing_api_key = s.API_KEY 
API_KEY = s.API_KEY

def index(request):
    return render(request, 'index.html',locals())




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
    elif 'c:' in query or ':'  not in query:
        # Get the current page number from the GET parameters
        results_concurrent = concurrent_search(query, all_sites, bing_search_custom, max_workers=len(all_sites))

        all_results = []
        for site_group in results_concurrent:
            try:
                #print(len(site_group["webPages"]["value"]))
                all_results.extend(site_group["webPages"]["value"])
            except:
                pass
            
        url_order = []
        [[url_order.append(x) for x in group] for group in all_sites if group]
        

        def sort_by_url_order(result):
            for i, base_url in enumerate(url_order):
                if result['url'].startswith(base_url):
                    return i
            return len(url_order)

        sorted_results = sorted(all_results, key=sort_by_url_order)
        main_words_list = get_main_words(query)
        main_words = ' '.join(main_words_list)
        # # Replace with your search function, e.g., bing_search or google_search
        results = sorted_results
        # # Filter the results by relevance
        relevance_threshold = 1
        filtered_results = filter_results_by_relevance(results, main_words, relevance_threshold)

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
    elif 'I:' in query:
        query = query.replace('I:', '')
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
        if not query.startswith('I:'):
            query = f'I:{query}'
        limite_I = "Limited I: search"
        return render(request, 'google_images_search.html', locals())
    else:
        results_concurrent = concurrent_search(query, all_sites, bing_search_custom_imgage, max_workers=len(all_sites)) 

        all_results = []
        for site_group in results_concurrent:
            try:all_results.extend(site_group["value"])
            except:pass

        images = [ { 'url': x['contentUrl'], 'hostUrl' : x['hostPageUrl'] } for x in  all_results]

        #bing_result_images = bing_search_images(query, bing_api_key, pignation_no = 0)
        #print("bing_result_images", bing_result_images)

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
    elif 'I:' in query:
        query = query.replace('I:', '')
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
        bing_api_key = API_KEY  # Replace with your Bing API key
        videos = []
        page_number = int(request.GET.get('page', 1))

        # Call Bing API with pagination
        for offset in range((page_number - 1) * 50, page_number * 50, 50):
            bing_results = bing_search_videos(query, bing_api_key, offset)
            print("bing_results v ", bing_results)
            for item in bing_results.get("value", []):
                name = item["name"]
                url = item["contentUrl"]
                videos.append({"name": name, "url": url})
        print(videos)
        # Use Django's built-in paginator to paginate the results
        paginator = Paginator(videos, 10)
        page_obj = paginator.get_page(page_number)




    #bing_video_list    = bing_video(query)
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
    else:
        # Get the current page number from the GET parameters
        results_concurrent = concurrent_search(query, all_sites, bing_search_custom, max_workers=len(all_sites))

        all_results = []
        for site_group in results_concurrent:
            try:
                #print(len(site_group["webPages"]["value"]))
                all_results.extend(site_group["webPages"]["value"])
            except:
                pass
        url_order = []
        [[url_order.append(x) for x in group] for group in all_results]

        def sort_by_url_order(result):
            for i, base_url in enumerate(url_order):
                if result['url'].startswith(base_url):
                    return i
            return len(url_order)

        sorted_results = sorted(all_results, key=sort_by_url_order)
        main_words_list = get_main_words(query)
        main_words = ' '.join(main_words_list)
        # # Replace with your search function, e.g., bing_search or google_search
        results = sorted_results
        # # Filter the results by relevance
        relevance_threshold = 1
        filtered_results = filter_results_by_relevance(results, main_words, relevance_threshold)


    return render(request, 'news.html', locals())




