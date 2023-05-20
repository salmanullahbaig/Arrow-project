from django.urls import path
from search.views import *
from search.bing_search import *
from search.views1 import *

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('google_images_search/<str:query>',google_images_search, name='google_images_search'),

    path('videos/<str:query>', videos, name='videos'),
    path('news/<str:query>', news, name='news'),

]