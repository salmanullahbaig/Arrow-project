from django.db import models


class SearchResult(models.Model):
    link = models.URLField(null=True,blank=True)
    title = models.CharField(null=True,blank=True,max_length=100)
    position = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.link})"

class Blocked(models.Model):
    link = models.URLField(null=True,blank=True)
    title = models.CharField(null=True,blank=True,max_length=100)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.link})"

class Searches(models.Model):
    query = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} ({self.timestamp})"


class Main_sites(models.Model):
    site = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return f"{self.site}"


class News_sites(models.Model):
    site = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return f"{self.site}"

class Social_sites(models.Model):
    site = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return f"{self.site}"


class Other_sites(models.Model):
    site = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return f"{self.site}"



class Scraped_news_webpages(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    content = models.TextField()
    snippet = models.TextField()
    video_src = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title



class Scraped_general_sites_webpages(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    content = models.TextField()
    snippet = models.TextField()
    video_src = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title