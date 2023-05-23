from django.http import JsonResponse

from search.models import *

##########################################################

import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity












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






