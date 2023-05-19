from django.contrib import admin
from search.models import *
# Register your models here.
admin.site.register(SearchResult)
admin.site.register(Blocked)
admin.site.register(Searches)

admin.site.register(Main_sites)
admin.site.register(News_sites)
admin.site.register(Social_sites)
admin.site.register(Other_sites)
admin.site.register(Scraped_news_webpages)
admin.site.register(Scraped_general_sites_webpages)