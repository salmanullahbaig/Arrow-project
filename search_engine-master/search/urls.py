from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('adminsearch', views.adminsearch, name='adminsearch'),
    path('adminsearchindexing', views.adminsearchindexing, name='adminsearchindexing'),
    path('google_images_search/<str:query>', views.google_images_search, name='google_images_search'),
    path('news/<str:query>', views.news, name='news'),
    path('videos/<str:query>', views.videos, name='videos'),
    path('update_position', views.update_position, name='update_position'),
    path('block_item', views.block_item, name='block_item'),
    path('create_sites', views.create_sites, name='create_sites'),
    path('scrape_sites_list', views.scrape_sites_list, name='scrape_sites_list'),
    path('pre', views.pre, name='pre'),

]