from django.urls import path
from search.views import  search as main_search,  google_images_search as img_search , videos
from search.bing_search import *
#from search.views1 import *
from search.views  import *
from search.views import  news

urlpatterns = [
    path('', index, name='index'),
    path('search', main_search, name='search'),
    path('google_images_search/<str:query>',img_search, name='google_images_search'),

    path('videos/<str:query>', videos, name='videos'),
    path('news/<str:query>', news, name='news'),

]