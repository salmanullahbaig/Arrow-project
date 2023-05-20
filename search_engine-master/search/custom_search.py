from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import requests





def bing_search_custom(query, api_key='0d41c358d3054032848a866956b9a9f5', sites=None):
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




