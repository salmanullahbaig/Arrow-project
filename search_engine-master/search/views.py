from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


#############   Start  Specific searches    ##########################

main_sites = ['https://www.Conservapedia.com',
               'https://www.Ballotpedia.com',
               'https://www.Trumpttrainnews.com',
               'https://www.AmericanActionNews.com',
                'https://www.AmericanDefenseNews.com',
                'https://americanbriefing.com',
                'https://goppresidential.com',
                'https://americanupdate.com', #(also for lifestyle/celebrity key-terms)
                'https://thehollywoodconservative.us', #(also for lifestyle/celebrity key-terms)
                'https://prolifeupdate.com'
]
all_sites = [[x] for x in main_sites ]
news_sites  = [
    'https://www.foxnews.com',
    'https://www.theepochtimes.com',
    'https://www.washingtonexaminer.com',
    'https://www.theblaze.com',
    'https://www.newsmax.com',
    'https://www.westernjournal.com',
    'https://www.dailywire.com',
    'https://www.nationalreview.com',
    'https://www.thegatewaypundit.com',
    'https://www.dailycaller.com',
    'https://www.washingtontimes.com',
    'https://www.townhall.com',
    'https://www.breitbart.com',
    'https://www.freebeacon.com',
    'https://www.thefederalist.com',
    'https://www.dailysignal.com',
    'https://www.nypost.com',
    'https://www.pjmedia.com',
    'https://www.zerohedge.com',
    'https://www.wsj.com',
    'https://www.oann.com',
    'https://www.realclearpolitics.com',
    'https://americasvoice.news',
    'https://www..AIM.org '
]


social_site = [
    'facebook.com',
    'twitter.com',
    'instagram.com',
    'tiktok.com/en/',
]

other_sites  = [
    "drudgereport.com",
    "foxbusiness.com",
    "americanthinker.com",
    "twitchy.com",
    "wnd.com",
    "hotair.com",
    "thelibertydaily.com",
    "justthenews.com",
    "theconservativetreehouse.com",
    "Waynedupree.com",
    "ocregister.com",
    "reason.com",
    "freerepublic.com",
    "bizpacreview.com",
    "powerlineblog.com",
    "amgreatness.com",
    "newsbusters.org",
    "nationalinterest.org",
    "blog.heritage.org",
    "cbn.com",
    "weaselzippers.us",
    "100percentfedup.com",
    "therightscoop.com",
    "lucianne.com",
    "theamericanconservative.com",
    "frontpagemag.com",
    "spectator.org",
    "cnsnews.com",
    "ijr.com",
    "Cato.org",
    "legalinsurrection.com",
    "hannity.com",
    "city-journal.org",
    "thefederalistpapers.org",
    "aei.org",
    "wattsupwiththat.com",
    "fee.org",
    "mises.org",
    "independentsentinel.com",
    "judicialwatch.org",
    "bearingarms.com",
    "amren.com",
    "chicksonright.com",
    "freedomworks.org",
    "firstthings.com",
    "thepoliticalinsider.com",
    "ricochet.com",
    "hoover.org",
    "sharylattkisson.com",
    "linkiest.com",
    "gopbriefingroom.com",
    "crisismagazine.com",
    "lifenews.com",
    "lifezette.com",
    "humanevents.com",
    "christianitytoday.com",
    "redstatewatcher.com",
    "conservativereview.com",
    "strategypage.com",
    "libertynation.com",
    "atr.org",
    "marklevinshow.com",
    "algemeiner.com",
    "rushlimbaugh.com",
    "steynonline.com",
    "cis.org",
    "weeklystandard.com",
    "independent.org",
    "blog.independent.org",
    "muckrock.com",
    "cagle.com",
    "anncoulter.com",
    "borderlandbeat.com"
]

[all_sites.append(x) for x in   [social_site, news_sites, other_sites]]

all_sites = [[x.replace("https://www.", '') for x in list_url] for list_url in all_sites]
all_sites = [[x.replace("https://", '') for x in list_url] for list_url in all_sites]



########## Start  Code #######################

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')


def get_main_words(query):
    # Tokenize the query
    words = word_tokenize(query)

    # Convert words to lowercase
    words = [word.lower() for word in words]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    main_words = [word for word in words if word not in stop_words and word.isalnum()]

    return main_words


def calculate_relevance_score(result, query_terms):
    title = result.get("title", "").lower()
    snippet = result.get("snippet", "").lower()

    score = 0
    for term in query_terms:
        if term in title:
            score += 1
        if term in snippet:
            score += 1

    return score


def filter_results_by_relevance(results, query, relevance_threshold):
    query_terms = query.lower().split()
    filtered_results = []

    for result in results:
        score = calculate_relevance_score(result, query_terms)
        if score >= relevance_threshold:
            filtered_results.append(result)

    return filtered_results


import requests
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures


def bing_search(query, api_key='0d41c358d3054032848a866956b9a9f5', sites=None):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    if sites:
        site_query = " OR ".join([f"site:{site}" for site in sites])
        query = f"{query} {site_query}"
    # print(len(str(query)))
    params = {"q": query, "count": 10, "offset": 0}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # print(params)
        # response = requests.get(url, headers=headers, params=params)
        # if response.status_code == 200:
        #     return response.json()
        print(f"Error: {response.status_code}")
        return None


def concurrent_search(query, websites, search_fn, max_workers):
    bing_api_key = "79407ee4a67041b5a12cbe23c684dbe5"
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        search_tasks = [executor.submit(search_fn, query, bing_api_key, sites=site) for site in websites]
        results = [task.result() for task in futures.as_completed(search_tasks)]

    return results

######### End Code #####################







#############   End  Specific searches    ##########################







from django.http import JsonResponse
from .models import Main_sites, News_sites, Social_sites, Other_sites

def create_sites(request):
    main_sites_list = ['https://www.Conservapedia.com',
               'https://www.Ballotpedia.com',
               'https://www.Trumpttrainnews.com',
               'https://www.AmericanActionNews.com',
                'https://www.AmericanDefenseNews.com',
                'https://americanbriefing.com',
                'https://goppresidential.com',
                'https://americanupdate.com', #(also for lifestyle/celebrity key-terms)
                'https://thehollywoodconservative.us', #(also for lifestyle/celebrity key-terms)
                'https://prolifeupdate.com']

    news_sites_list = ['https://www.foxnews.com',
    'https://www.theepochtimes.com',
    'https://www.washingtonexaminer.com',
    'https://www.theblaze.com',
    'https://www.newsmax.com',
    'https://www.westernjournal.com',
    'https://www.dailywire.com',
    'https://www.nationalreview.com',
    'https://www.thegatewaypundit.com',
    'https://www.dailycaller.com',
    'https://www.washingtontimes.com',
    'https://www.townhall.com',
    'https://www.breitbart.com',
    'https://www.freebeacon.com',
    'https://www.thefederalist.com',
    'https://www.dailysignal.com',
    'https://www.nypost.com',
    'https://www.pjmedia.com',
    'https://www.zerohedge.com',
    'https://www.wsj.com',
    'https://www.oann.com',
    'https://www.realclearpolitics.com',
    'https://americasvoice.news',
    'https://www.AIM.org ']

    social_sites_list = ['https://www.facebook.com',
    'https://www.twitter.com',
    'https://www.instagram.com',
    'https://www.tiktok.com/en/',]


    other_sites_list = ["https://www.drudgereport.com",
    "https://www.foxbusiness.com",
    "https://www.americanthinker.com",
    "https://www.twitchy.com",
    "https://www.wnd.com",
    "https://www.hotair.com",
    "https://www.thelibertydaily.com",
    "https://www.justthenews.com",
    "https://www.theconservativetreehouse.com",
    "https://www.Waynedupree.com",
    "https://www.ocregister.com",
    "https://www.reason.com",
    "https://www.freerepublic.com",
    "https://www.bizpacreview.com",
    "https://www.powerlineblog.com",
    "https://www.amgreatness.com",
    "https://www.newsbusters.org",
    "https://www.nationalinterest.org",
    "https://blog.heritage.org",
    "https://www.cbn.com",
    "https://www.weaselzippers.us",
    "https://www.100percentfedup.com",
    "https://www.therightscoop.com",
    "https://www.lucianne.com",
    "https://www.theamericanconservative.com",
    "https://www.frontpagemag.com",
    "https://www.spectator.org",
    "https://www.cnsnews.com",
    "https://www.ijr.com",
    "https://www.Cato.org",
    "https://www.legalinsurrection.com",
    "https://www.hannity.com",
    "https://www.city-journal.org",
    "https://www.thefederalistpapers.org",
    "https://www.aei.org",
    "https://www.wattsupwiththat.com",
    "https://www.fee.org",
    "https://www.mises.org",
    "https://www.independentsentinel.com",
    "https://www.judicialwatch.org",
    "https://www.bearingarms.com",
    "https://www.amren.com",
    "https://www.chicksonright.com",
    "https://www.freedomworks.org",
    "https://www.firstthings.com",
    "https://www.thepoliticalinsider.com",
    "https://www.ricochet.com",
    "https://www.hoover.org",
    "https://www.sharylattkisson.com",
    "https://www.linkiest.com",
    "https://www.gopbriefingroom.com",
    "https://www.crisismagazine.com",
    "https://www.lifenews.com",
    "https://www.lifezette.com",
    "https://www.humanevents.com",
    "https://www.christianitytoday.com",
    "https://www.redstatewatcher.com",
    "https://www.conservativereview.com",
    "https://www.strategypage.com",
    "https://www.libertynation.com",
    "https://www.atr.org",
    "https://www.marklevinshow.com",
    "https://www.algemeiner.com",
    "https://www.rushlimbaugh.com",
    "https://www.steynonline.com",
    "https://www.cis.org",
    "https://www.weeklystandard.com",
    "https://www.independent.org",
    "https://blog.independent.org",
    "https://www.muckrock.com",
    "https://www.cagle.com",
    "anncoulter.com",
    "borderlandbeat.com"
]

    for site in main_sites_list:
        Main_sites.objects.create(site=site)

    for site in news_sites_list:
        News_sites.objects.create(site=site)

    for site in social_sites_list:
        Social_sites.objects.create(site=site)

    for site in other_sites_list:
        Other_sites.objects.create(site=site)

    response_data = {'success': True, 'message': 'Objects created successfully.'}
    return JsonResponse(response_data)





#############   Start  I: searches    ##########################


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

### Start Scrape  sites ####

count = 0  # initialize count to 0

def get_page_content(url):
    global count  # use the global count variable inside this function
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Create and save new Webpage objects
            title = soup.find('title').get_text()
            link = url
            snippet = soup.get_text()[:100] + "..."
            content = soup.get_text()

            # Get the first image with an "https" URL
            image_url = None
            for img in soup.find_all("img"):
                src = img.get("src")
                if src.startswith("https"):
                    image_url = src
                    break  # Stop after finding the first image with "https"

            # Get the first video source with an "https" URL
            video_src = None
            video_tags = soup.find_all('video')
            for video_tag in video_tags:
                sources = video_tag.find_all('source')
                for source_tag in sources:
                    src = source_tag.get('src')
                    if src.startswith("https"):
                        video_src = src
                        break  # Stop after finding the first video source with "https"
                if video_src:
                    break  # Stop iterating over video tags if a video source is found

            webpage, created = Scraped_news_webpages.objects.get_or_create(
                title=title,
                link=link,
                content=content,
                snippet=snippet,
                image_url=image_url,
                video_src=video_src
            )

            if created:
                print(f"-- New Scraped --")
                count += 1  # increment count every time an object is created

                # Print the count
                print(f"Count: {count} == {image_url}", "vid src ==", video_src)
            else:
                print(f"### -- Already exists -- ###")
            return soup
        else:
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


def crawl_website(url, max_depth=2, current_depth=1):
    if current_depth > max_depth:
        return {}

    content_map = {}
    soup = get_page_content(url)
    if soup:
        content_map[url] = soup.get_text()
        # tile_map[url] = soup.find('title').get_text()
        internal_links = find_internal_links(soup, url)
        for link in internal_links:
            content_map.update(crawl_website(link, max_depth, current_depth + 1))

    return content_map



def scrape_sites_list(request):

    # List of websites to crawl
    urls = [

        'https://www.foxnews.com',
        # 'https://www.theepochtimes.com',
        # 'https://www.washingtonexaminer.com',
        # 'https://www.theblaze.com',
        # 'https://www.newsmax.com',
        # 'https://www.westernjournal.com',
        # 'https://www.dailywire.com',
        # 'https://www.nationalreview.com',
        # 'https://www.thegatewaypundit.com',
        # 'https://www.dailycaller.com',
        # 'https://www.washingtontimes.com',
        # 'https://www.townhall.com',
        # 'https://www.breitbart.com',
        # 'https://www.freebeacon.com',
        # 'https://www.thefederalist.com',
        # 'https://www.dailysignal.com',
        # 'https://www.nypost.com',
        # 'https://www.pjmedia.com',
        # 'https://www.zerohedge.com',
        # 'https://www.wsj.com',
        # 'https://www.oann.com',
        # 'https://www.realclearpolitics.com',
        # 'https://americasvoice.news',
        # 'https://www.AIM.org ',
        # 'https://www.bbc.com'


         # General sites

        # "https://www.drudgereport.com",
        # "https://www.foxbusiness.com",
        # "https://www.americanthinker.com",
        # "https://www.twitchy.com",
        # "https://www.wnd.com",
        # "https://www.hotair.com",
        # "https://www.thelibertydaily.com",
        # "https://www.justthenews.com",
        # "https://www.theconservativetreehouse.com",
        # "https://www.Waynedupree.com",
        # "https://www.ocregister.com",
        # "https://www.reason.com",
        # "https://www.freerepublic.com",
        # "https://www.bizpacreview.com",
        # "https://www.powerlineblog.com",
        # "https://www.amgreatness.com",
        # "https://www.newsbusters.org",
        # "https://www.nationalinterest.org",
        # "https://blog.heritage.org",
        # "https://www.cbn.com",
        # "https://www.weaselzippers.us",
        # "https://www.100percentfedup.com",
        # "https://www.therightscoop.com",
        # "https://www.lucianne.com",
        # "https://www.theamericanconservative.com",
        # "https://www.frontpagemag.com",
        # "https://www.spectator.org",
        # "https://www.cnsnews.com",
        # "https://www.ijr.com",
        # "https://www.Cato.org",
        # "https://www.legalinsurrection.com",
        # "https://www.hannity.com",
        # "https://www.city-journal.org",
        # "https://www.thefederalistpapers.org",
        # "https://www.aei.org",
        # "https://www.wattsupwiththat.com",
        # "https://www.fee.org",
        # "https://www.mises.org",
        # "https://www.independentsentinel.com",
        # "https://www.judicialwatch.org",
        # "https://www.bearingarms.com",
        # "https://www.amren.com",
        # "https://www.chicksonright.com",
        # "https://www.freedomworks.org",
        # "https://www.firstthings.com",
        # "https://www.thepoliticalinsider.com",
        # "https://www.ricochet.com",
        # "https://www.hoover.org",
        # "https://www.sharylattkisson.com",
        # "https://www.linkiest.com",
        # "https://www.gopbriefingroom.com",
        # "https://www.crisismagazine.com",
        # "https://www.lifenews.com",
        # "https://www.lifezette.com",
        # "https://www.humanevents.com",
        # "https://www.christianitytoday.com",
        # "https://www.redstatewatcher.com",
        # "https://www.conservativereview.com",
        # "https://www.strategypage.com",
        # "https://www.libertynation.com",
        # "https://www.atr.org",
        # "https://www.marklevinshow.com",
        # "https://www.algemeiner.com",
        # "https://www.rushlimbaugh.com",
        # "https://www.steynonline.com",
        # "https://www.cis.org",
        # "https://www.weeklystandard.com",
        # "https://www.independent.org",
        # "https://www.blog.independent.org",
        # "https://www.muckrock.com",
        # "https://www.cagle.com",
        # "https://www.anncoulter.com",
        # "https://www.borderlandbeat.com"


    ]

    # Crawl each website and store the content
    content_map = {}
    test_list = []
    for url in urls:
        crawl_website(url, max_depth=2)
    print("Script finished running 1.")
    for url, content in content_map.items():
        print(f"URL: {url}")  # tilte : {content}")
    print("Script finished running 2.")


### end Scrape sites ####



# ## Preprocess

import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
#from crawler.models import Website

# Download the NLTK stopwords corpus
nltk.download('stopwords')
nltk.download('punkt')

# Tokenization function
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if token not in string.punctuation]
    return tokens

# Remove stopwords function
def remove_stopwords(tokens):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    return [token for token in tokens if token not in stopwords]

# Preprocessing function
def preprocess(text):
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    return tokens


def pre(request):
    # Fetch the crawled data from the Django database
    websites = Scraped_general_sites_webpages.objects.all()
    news_websites = Scraped_news_webpages.objects.all()
    urls = [website.link for website in websites]  # Access the 'link' field
    news_urls = [website.link for website in news_websites]  # Access the 'link' field
    urls = urls + news_urls
    contents = [website.content for website in websites]  # Access the 'content' field
    news_contents = [website.content for website in news_websites]  # Access the 'content' field
    contents = contents + news_contents

    # Preprocess the content
    preprocessed_contents = [' '.join(preprocess(content)) for content in contents]

    # Create the TF-IDF index
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_contents)

    # Save the vectorizer and TF-IDF matrix for later use
    import pickle

    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    with open('tfidf_matrix.pkl', 'wb') as f:
        pickle.dump(tfidf_matrix, f)

    response_data = {'success': True, 'message': 'Objects created successfully.'}
    return JsonResponse(response_data)





##########################################################

import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity


def I_search(query, top_n=30):
    # Fetch the crawled data from the Django database
    general_sites = Scraped_general_sites_webpages.objects.all()
    news_sites = Scraped_news_webpages.objects.all()

    # Combine the results from both models
    #
    #general_sites = []
    websites = list(general_sites) + list(news_sites)

    # Extract the required fields from each website object
    urls = [website.link for website in websites]
    titles = [website.title for website in websites]
    snippets = [website.snippet for website in websites]
    video_srcs = [website.video_src for website in websites]
    image_urls = [website.image_url for website in websites]

    # Preprocess the query
    preprocessed_query = ' '.join(preprocess(query))
    # Load the vectorizer and tfidf_matrix from disk
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('tfidf_matrix.pkl', 'rb') as f:
        tfidf_matrix = pickle.load(f)
    # Transform the query using the vectorizer
    query_vector = vectorizer.transform([preprocessed_query])

    # Calculate the cosine similarity between the query and documents
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)

    # Get the indices of the top_n most similar documents
    most_similar_indices = np.argsort(similarity_scores[0])[-top_n:][::-1]

    # Retrieve the fields of the most similar documents
    most_similar_urls = [urls[i] for i in most_similar_indices]
    most_similar_titles = [titles[i] for i in most_similar_indices]
    most_similar_snippets = [snippets[i] for i in most_similar_indices]
    most_similar_video_srcs = [video_srcs[i] for i in most_similar_indices]
    most_similar_image_urls = [image_urls[i] for i in most_similar_indices]

    # Return the most similar documents and their similarity scores
    return [(most_similar_titles[i], most_similar_urls[i], most_similar_snippets[i],most_similar_video_srcs[i],most_similar_image_urls[i], similarity_scores[0][i]) for i in range(len(most_similar_indices))]




def I_search_news(query, top_n=20):
    # Fetch the crawled data from the Django database
    #general_sites = Scraped_general_sites_webpages.objects.all()
    news_sites = Scraped_news_webpages.objects.all()

    # Combine the results from both models
    websites = list(news_sites)

    # Extract the required fields from each website object
    urls = [website.link for website in websites]
    titles = [website.title for website in websites]
    snippets = [website.snippet for website in websites]

    # Preprocess the query
    preprocessed_query = ' '.join(preprocess(query))
    # Load the vectorizer and tfidf_matrix from disk
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('tfidf_matrix.pkl', 'rb') as f:
        tfidf_matrix = pickle.load(f)
    # Transform the query using the vectorizer
    query_vector = vectorizer.transform([preprocessed_query])

    # Calculate the cosine similarity between the query and documents
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)

    # Get the indices of the top_n most similar documents
    most_similar_indices = np.argsort(similarity_scores[0])[-top_n:][::-1]

    # Retrieve the fields of the most similar documents
    most_similar_urls = [urls[i] for i in most_similar_indices]
    most_similar_titles = [titles[i] for i in most_similar_indices]
    most_similar_snippets = [snippets[i] for i in most_similar_indices]


    # Return the most similar documents and their similarity scores
    return [(most_similar_titles[i], most_similar_urls[i], most_similar_snippets[i],similarity_scores[0][i]) for i in range(len(most_similar_indices))]




#############   End  I: searches    ##########################












def index(request):
    pass
    return render(request, 'index.html',locals())


def web_bing(query):
    url = f"https://www.bing.com/search?q={query}&setlang=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    search_results = soup.find_all("li", class_="b_algo")
    results = []
    for result in search_results:
        title = result.find("h2").text
        url = result.find("a")["href"]
        snippet = result.find("div", class_="b_caption").find("p").text
        results.append({"title": title, "url": url, "snippet": snippet})
    return results




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


def bing_news(query):
    url = f"https://www.bing.com/news/search?q={query}&setlang=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_cards = soup.find_all("div", class_="news-card")
    news_list = []
    for card in news_cards:
        title = card.find("a", class_="title").text
        link = card.find("a", class_="title")["href"]
        news_list.append({'title': title, 'link': link})
    return news_list



def bing_video(query):
    url = f"https://www.bing.com/videos/search?q={query}&setlang=en"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all video results
    video_results = soup.find_all('div', {'class': 'dg_u'})

    # extract the aria-label and href attributes for each a tag inside the class="mc_vtvc"
    results = []
    for video in video_results:
        mc_vtvc_div = video.find('div', {'class': 'mc_vtvc'})
        a_tags = mc_vtvc_div.find_all('a')

        for a_tag in a_tags:
            aria_label = a_tag.get('aria-label', '')
            url = a_tag.get('href', '')

            results.append({'aria_label': aria_label, 'url': url})

    return results



def get_news(query):
    url = f"https://www.google.com/search?q={query}&tbm=nws"

    # Set the headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_div = soup.find('div', class_='MjjYud')

    news_list = []
    # Loop through all the news articles and add their details to the list
    for article in news_div.find_all('div', class_='SoaBEf'):
        headline = article.find('div', class_='vJOb1e').get_text()
        link = article.find('a')['href']
        news_dict = {'headline': headline, 'link': link}
        news_list.append(news_dict)

    return news_list


def get_video_results(query):
    url = f"https://www.google.com/search?q={query}&tbm=vid"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    video_links = soup.find_all("div", class_="DhN8Cf")

    results = []
    for link in video_links:
        href_link = link.a['href']
        title = link.h3.text
        results.append({'link': href_link, 'title': title})

    return results



def google_search_images(query, search_type='image'):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": 'AIzaSyDxBnA4Wwhh1sH3gFOZ2nQl_smU3uO3BBA',
        "cx": "c772d9b1605014105",
        "searchType": search_type,
    }
    response = requests.get(url, params=params)
    return response.json()


def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": 'AIzaSyDxBnA4Wwhh1sH3gFOZ2nQl_smU3uO3BBA',
        "cx": "c772d9b1605014105",
    }
    response = requests.get(url, params=params)
    return response.json()
from django.core.paginator import Paginator
from search.models import *


def search(request):
    query = request.GET.get('q') or request.POST.get('query')
    Searches.objects.create(query=query)

    if 'B:' in query:
        # Do something if the query has B:
        print('Query has B:',query)
        query = query.replace('B:', '')
        bing_result_web = web_bing(query)
        items = bing_result_web
        for i, item in enumerate(items):
            item['id_'] = i + 1

            # Check if this item exists in the SearchResult model
            try:
                search_result = SearchResult.objects.get(title=item['title'])
                position = search_result.position
                # Calculate the new index of the item based on its position
                new_index = position - 1
                # If the new index is different from the default index, swap the item with the one at the new index
                if new_index != i:
                    items[i], items[new_index] = items[new_index], items[i]
                    # Update the ID of the item that was swapped with the current item
                    items[new_index]['id_'] = new_index + 1
                    # Update the ID of the current item
                    item['id_'] = i + 1
            except SearchResult.DoesNotExist:
                pass

            # Check if this item is blocked
            if Blocked.objects.filter(title=item['title'], link=item['url']).exists():
                items.remove(item)

        bing_result_web = items
        direct_bing = "Direct bing"
        if not query.startswith('B:'):
            query = f'B:{query}'
        return render(request, 'search.html', locals())
    elif 'I:' in query:
        query = query.replace('I:', '')
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
    else:
        # Do something else if the query does not have B:
        print('Query does not have B:')
        #############   Start  Specific searches    ##########################
        results_concurrent = concurrent_search(query, all_sites, bing_search, max_workers=len(all_sites))
        #print(results_concurrent)

        all_results = []
        for site_group in results_concurrent:
            try:
                print(len(site_group["webPages"]["value"]))
                all_results.extend(site_group["webPages"]["value"])
            except:
                pass

        # print("all_results",all_results)
        # for page in all_results:
        #     print(page['url'])
        #     print(page['snippet'])

        url_order = []
        [[url_order.append(x) for x in group] for group in all_results]

        def sort_by_url_order(result):
            for i, base_url in enumerate(url_order):
                if result['url'].startswith(base_url):
                    return i
            return len(url_order)

        sorted_results = sorted(all_results, key=sort_by_url_order)

        # for page in sorted_results:
        #     print(page['url'])
        #     print(page['snippet'])

        main_words_list = get_main_words(query)
        main_words = ' '.join(main_words_list)
        # print(main_words)

        # # Replace with your search function, e.g., bing_search or google_search
        results = sorted_results

        # # Filter the results by relevance
        relevance_threshold = 1
        filtered_results = filter_results_by_relevance(results, main_words, relevance_threshold)
        #print(filtered_results)
        # # Print the filtered results
        for idx, result in enumerate(filtered_results):
            print(f"{idx + 1}: {result['snippet']} - {result['url']}")
        #############   End  Specific searches    ##########################




    #Google
    # result = google_search(query)
    # items = result["items"]
    # total_results = result["searchInformation"]["totalResults"]

    # page = request.GET.get('page', 1)
    #
    # url = "https://www.googleapis.com/customsearch/v1"
    # params = {
    #     "q": query,
    #     "key": 'AIzaSyDxBnA4Wwhh1sH3gFOZ2nQl_smU3uO3BBA',
    #     "cx": "c772d9b1605014105",
    #     "start": (int(page) - 1) * 10 + 1
    # }
    # response = requests.get(url, params=params)
    # result = response.json()
    # items = result["items"]
    # total_results = result["searchInformation"]["totalResults"]
    #
    # for i, item in enumerate(items):
    #     item['id_'] = i + 1
    #
    #     # Check if this item exists in the SearchResult model
    #     try:
    #         search_result = SearchResult.objects.get(title=item['title'])
    #         position = search_result.position
    #         # Calculate the new index of the item based on its position
    #         new_index = position - 1
    #         # If the new index is different from the default index, swap the item with the one at the new index
    #         if new_index != i:
    #             items[i], items[new_index] = items[new_index], items[i]
    #             # Update the ID of the item that was swapped with the current item
    #             items[new_index]['id_'] = new_index + 1
    #             # Update the ID of the current item
    #             item['id_'] = i + 1
    #     except SearchResult.DoesNotExist:
    #         pass
    #
    #     # Check if this item is blocked
    #     if Blocked.objects.filter(title=item['title'], link=item['link']).exists():
    #         items.remove(item)
    #
    # paginator = Paginator(items, 10)
    # page_obj = paginator.get_page(page)




    #images
    # result_images = google_search_images(query, search_type="image")
    # images_items = result_images.get("items", [])
    # image_urls = [item.get("link", "") for item in images_items]

    # #news
    # news_list = get_news(query)

    # #videos
    # video_results = get_video_results(query)


    #Bing

    # bing_result_images = bing_images(query)
    # bing_news_list = bing_news(query)
    # bing_video_list    = bing_video(query)


    return render(request, 'search.html', locals())


def adminsearch(request):
    pass
    return render(request, 'adminsearch.html',locals())


def adminsearchindexing(request):
    query = request.GET.get('q') or request.POST.get('query')
    Searches.objects.create(query=query)

    if 'B:' in query:
        # Do something if the query has B:
        print('Query has B:',query)
        query = query.replace('B:', '')
        bing_result_web = web_bing(query)
        print(type(bing_result_web))
        items = bing_result_web
        for i, item in enumerate(items):
            item['id_'] = i + 1

            # Check if this item exists in the SearchResult model
            try:
                search_result = SearchResult.objects.get(title=item['title'])
                position = search_result.position
                # Calculate the new index of the item based on its position
                new_index = position - 1
                # If the new index is different from the default index, swap the item with the one at the new index
                if new_index != i:
                    items[i], items[new_index] = items[new_index], items[i]
                    # Update the ID of the item that was swapped with the current item
                    items[new_index]['id_'] = new_index + 1
                    # Update the ID of the current item
                    item['id_'] = i + 1
            except SearchResult.DoesNotExist:
                pass

            # Check if this item is blocked
            if Blocked.objects.filter(title=item['title'], link=item['url']).exists():
                items.remove(item)

        bing_result_web = items



        direct_bing = "Direct bing"
        if not query.startswith('B:'):
            query = f'B:{query}'
        return render(request, 'adminsearchindexing.html', locals())
    elif 'I:' in query:
        query = query.replace('I:', '')
        top_n = 5
        results = I_search(query, top_n)
        items = list(results)
        print(type(items))

        for i, item in enumerate(items):
            item_dict = {'id_': i + 1, 'title': item[0], 'url': item[1]}
            search_result = SearchResult.objects.filter(title=item_dict['title']).first()

            if search_result:
                position = search_result.position
                new_index = position - 1

                if new_index != i:
                    items[i], items[new_index] = items[new_index], items[i]
                    items[i] = (i + 1, items[i][1])  # Create a new tuple with the updated id_
                    items[new_index] = (new_index + 1, items[new_index][1])  # Create a new tuple with the updated id_

            if Blocked.objects.filter(title=item_dict['title'], link=item_dict['url']).exists():
                items.remove(item)

        results = items

        for item in results:
            print(f"id_: {item[0]}, url: {item[1]}")

        limite_I = "Limited I: search"
        if not query.startswith('I:'):
            query = f'I:{query}'
        return render(request, 'adminsearchindexing.html', locals())
    else:
        # Do something else if the query does not have B:
        print('Query does not have B:')
        #############   Start  Specific searches    ##########################
        results_concurrent = concurrent_search(query, all_sites, bing_search, max_workers=len(all_sites))
        #print(results_concurrent)

        all_results = []
        for site_group in results_concurrent:
            try:
                print(len(site_group["webPages"]["value"]))
                all_results.extend(site_group["webPages"]["value"])
            except:
                pass

        # print("all_results",all_results)
        # for page in all_results:
        #     print(page['url'])
        #     print(page['snippet'])

        url_order = []
        [[url_order.append(x) for x in group] for group in all_results]

        def sort_by_url_order(result):
            for i, base_url in enumerate(url_order):
                if result['url'].startswith(base_url):
                    return i
            return len(url_order)

        sorted_results = sorted(all_results, key=sort_by_url_order)

        # for page in sorted_results:
        #     print(page['url'])
        #     print(page['snippet'])

        main_words_list = get_main_words(query)
        main_words = ' '.join(main_words_list)
        # print(main_words)

        # # Replace with your search function, e.g., bing_search or google_search
        results1 = sorted_results

        # # Filter the results by relevance
        relevance_threshold = 1
        filtered_results = filter_results_by_relevance(results1, main_words, relevance_threshold)
        #print(filtered_results)
        # # Print the filtered results
        for idx, result in enumerate(filtered_results):
            print(f"{result['name']} - {result['url']}")


        return render(request, 'adminsearchindexing.html', locals())



        #############   End  Specific searches    ##########################




    #Google
    # result = google_search(query)
    # items = result["items"]
    # total_results = result["searchInformation"]["totalResults"]

    # page = request.GET.get('page', 1)
    #
    # url = "https://www.googleapis.com/customsearch/v1"
    # params = {
    #     "q": query,
    #     "key": 'AIzaSyDxBnA4Wwhh1sH3gFOZ2nQl_smU3uO3BBA',
    #     "cx": "c772d9b1605014105",
    #     "start": (int(page) - 1) * 10 + 1
    # }
    # response = requests.get(url, params=params)
    # result = response.json()
    # items = result["items"]
    # total_results = result["searchInformation"]["totalResults"]
    #
    # for i, item in enumerate(items):
    #     item['id_'] = i + 1
    #
    #     # Check if this item exists in the SearchResult model
    #     try:
    #         search_result = SearchResult.objects.get(title=item['title'])
    #         position = search_result.position
    #         # Calculate the new index of the item based on its position
    #         new_index = position - 1
    #         # If the new index is different from the default index, swap the item with the one at the new index
    #         if new_index != i:
    #             items[i], items[new_index] = items[new_index], items[i]
    #             # Update the ID of the item that was swapped with the current item
    #             items[new_index]['id_'] = new_index + 1
    #             # Update the ID of the current item
    #             item['id_'] = i + 1
    #     except SearchResult.DoesNotExist:
    #         pass
    #
    #     # Check if this item is blocked
    #     if Blocked.objects.filter(title=item['title'], link=item['link']).exists():
    #         items.remove(item)
    #
    # paginator = Paginator(items, 10)
    # page_obj = paginator.get_page(page)




    #images
    # result_images = google_search_images(query, search_type="image")
    # images_items = result_images.get("items", [])
    # image_urls = [item.get("link", "") for item in images_items]

    # #news
    # news_list = get_news(query)

    # #videos
    # video_results = get_video_results(query)


    #Bing

    # bing_result_images = bing_images(query)
    # bing_news_list = bing_news(query)
    # bing_video_list    = bing_video(query)


    #return render(request, 'adminsearchindexing.html', locals())










def bing_search_images_2(query, api_key):
    url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 50, "offset": 0, "imageType": "photo"}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def google_images_search(request,query):

    #images
    # result_images = google_search_images(query, search_type="image")
    # images_items = result_images.get("items", [])
    # image_urls = [item.get("link", "") for item in images_items]
    # print("image_urls",image_urls)
    # bing_api_key = "0d41c358d3054032848a866956b9a9f5"  # Replace with your Bing API key
    # bing_results = bing_search_images_2(query, bing_api_key)
    # image_urls = []
    # for item in bing_results.get("value", []):
    #     image_urls.append(item['contentUrl'])

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


def google_search_news_2(query):
    url = "https://www.googleapis.com/customsearch/v1"
    all_results = []
    num_results=10
    for start in range(1, num_results, 10):
        params = {
            "q": query,
                  "key": "AIzaSyDxBnA4Wwhh1sH3gFOZ2nQl_smU3uO3BBA",
                  "cx": "c772d9b1605014105",
            "start": start,
            "tbm": "nws",
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            all_results.extend(response.json()["items"])
        else:
            print(f"Error: {response.status_code}")
            break

    return all_results




def bing_search_news_2(query, api_key, offset=0):
    url = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 50, "offset": offset}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def news(request, query):
    # news
   # news_list = get_news(query)
    #news_list = google_search_news_2(query)
    #bing_news_list = bing_news(query)
    # bing_api_key = "0d41c358d3054032848a866956b9a9f5"  # Replace with your Bing API key
    #
    # page_number = request.GET.get('page', 1)
    # offset = (int(page_number) - 1) * 50
    # bing_news_list = bing_search_news_2(query, bing_api_key, offset)
    #
    # paginator = Paginator(bing_news_list['value'], 10)
    #
    # page_obj = paginator.get_page(page_number)
    #
    # context = {
    #     'bing_results': page_obj,
    #     #'news_list': news_list,
    #     'query': query,
    # }
    top_n = 30
    results = I_search(query, top_n)
    # Set the number of results per page
    results_per_page = 10

    # Create a paginator object
    paginator = Paginator(results, results_per_page)

    # Get the current page number from the GET parameters
    page_number = request.GET.get('page')

    # Get the results for the current page
    page_obj = paginator.get_page(page_number)


    return render(request, 'news.html', locals())



def bing_search_videos_2(query, api_key, offset=0):
    url = "https://api.bing.microsoft.com/v7.0/videos/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 50, "offset": offset, "responseFilter": "Video"}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def videos(request,query):
    #videos
    #video_results = get_video_results(query)
    if 'B:' in query:
        query = query.replace('B:', '')
        bing_api_key = "79407ee4a67041b5a12cbe23c684dbe5"  # Replace with your Bing API key
        videos = []
        page_number = int(request.GET.get('page', 1))

        # Call Bing API with pagination
        for offset in range((page_number - 1) * 50, page_number * 50, 50):
            bing_results = bing_search_videos_2(query, bing_api_key, offset)
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
        bing_api_key = "79407ee4a67041b5a12cbe23c684dbe5"  # Replace with your Bing API key
        videos = []
        page_number = int(request.GET.get('page', 1))

        # Call Bing API with pagination
        for offset in range((page_number - 1) * 50, page_number * 50, 50):
            bing_results = bing_search_videos_2(query, bing_api_key, offset)
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


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SearchResult,Blocked

@csrf_exempt
def update_position(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        position = payload.get('position')
        itemId = payload.get('id_')
        title = payload.get('title')
        link = payload.get('link')
        print("__Data__")
        print("Target index : ",position)
        print("itemId : ",itemId)
        print(title)
        print(link)

        try:
            get_position = SearchResult.objects.get(title=title)
            get_position.position = position
            get_position.save()
        except SearchResult.DoesNotExist:
            # If a SearchResult object with the specified title does not exist, create a new one
            search_result = SearchResult.objects.create(title=title, link=link, position=position)


        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


from django.shortcuts import redirect
from django.urls import reverse


@csrf_exempt
def block_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        query = request.POST.get('query')
        Blocked.objects.create(title=title, link=link, is_blocked=True)
        return redirect(reverse('adminsearchindexing') + f'?q={query}')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


















#google search scrape :





#web
#
#
# import requests
# from bs4 import BeautifulSoup
#
# query = "web scraping with python"
# url = f"https://www.google.com/search?q={query}"
#
# # Set the headers to mimic a browser request
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# }
#
# # Send a GET request to the Google search results page
# response = requests.get(url, headers=headers)
#
# # Create a BeautifulSoup object
# soup = BeautifulSoup(response.content, "html.parser")
#
# # Find all search result links and titles
# search_results = soup.select(".yuRUbf a")
# for result in search_results:
#     link = result.get("href")
#     title = result.find("h3").get_text()
#     print("Link:", link)
#     print("Title:", title)
#
#
#
#
#
# #images
#
#
# import requests
# from bs4 import BeautifulSoup
#
# query = "apple"
# url = f"https://www.google.com/search?q={query}&tbm=isch"
#
# # Set the headers to mimic a browser request
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# }
#
# # Send a GET request to the Google Images search results page
# response = requests.get(url, headers=headers)
#
# # Create a BeautifulSoup object
# soup = BeautifulSoup(response.content, "html.parser")
#
# # Find all image URLs and display them
# image_links = soup.select(".rg_i")
# for link in image_links:
#     try:
#         image_url = link["data-src"]
#     except KeyError:
#         image_url = link["src"]
#     print("Image URL:", image_url)
#
#
#
# #news:
#
# import requests
# from bs4 import BeautifulSoup
#
# query = "apple"
# url = f"https://www.google.com/search?q={query}&tbm=nws"
#
# # Set the headers to mimic a browser request
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# }
#
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.content, 'html.parser')
# news_div = soup.find('div', class_='MjjYud')
#
#
# # Loop through all the news articles and print their details
# for article in news_div.find_all('div', class_='SoaBEf'):
#     headline = article.find('div', class_='vJOb1e').get_text()
#     link = article.find('a')['href']
#     print("Headline and Link:", [headline, link])
#
#
#
#
#
#
#
# #videos :
#
#
#
# import requests
# from bs4 import BeautifulSoup
#
# query = "apple"
# url = f"https://www.google.com/search?q={query}&tbm=vid"
#
# # Set the headers to mimic a browser request
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# }
#
# # Send a GET request to the URL with headers
# response = requests.get(url, headers=headers)
#
# # Parse the HTML content of the response with BeautifulSoup
# soup = BeautifulSoup(response.content, "html.parser")
#
# # Find all the links with class "DhN8Cf" inside the video section
# video_links = soup.find_all("div", class_="DhN8Cf")
#
# # Loop through the links and extract the href links and the text inside the h3 tag
# for link in video_links:
#     href_link = link.a['href']
#     title = link.h3.text
#     print(f"Link: {href_link}")
#     print(f"Title: {title}\n")
#
#
