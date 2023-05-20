from django.urls import path
from . import views1
from search.general_Bing_search import *


urlpatterns = [
    #path('', views1.index, name='index'),
   # path('search', views1.search, name='search'),
    path('adminsearch', views1.adminsearch, name='adminsearch'),
    path('adminsearchindexing', views1.adminsearchindexing, name='adminsearchindexing'),
    #path('google_images_search/<str:query>', views1.google_images_search, name='google_images_search'),
    #path('news/<str:query>', views1.news, name='news'),
    #path('videos/<str:query>', views1.videos, name='videos'),
    path('update_position', views1.update_position, name='update_position'),
    path('block_item', views1.block_item, name='block_item'),
    path('create_sites', views1.create_sites, name='create_sites'),
    path('scrape_sites_list', views1.scrape_sites_list, name='scrape_sites_list'),
    path('pre', views1.pre, name='pre'),

]