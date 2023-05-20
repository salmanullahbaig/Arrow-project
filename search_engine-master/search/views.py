from django.shortcuts import render
from search.models import *
import requests
from bs4 import BeautifulSoup
from search.general_Bing_search import *
from django.core.paginator import Paginator
from search.custom_search import *


def index(request):
    pass
    return render(request, 'index.html',locals())




def search(request):
    query = request.GET.get('q') or request.POST.get('query')
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
        bing_results = bing_search(query,pignation_no=int(page_number))
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
        return render(request, 'search.html', locals())
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


    return render(request, 'search.html', locals())





def google_images_search(request,query):

    if 'B:' in query:
        query = query.replace('B:', '')
        bing_result_images = bing_images(query)
        print("bing_result_images", bing_result_images)
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
        bing_result_images = bing_images(query)
        print("bing_result_images", bing_result_images)

    return render(request, 'google_images_search.html', locals())