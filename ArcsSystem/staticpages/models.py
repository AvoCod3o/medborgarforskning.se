from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf import settings

class Page(models.Model):
    '''Defines a basic page'''

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    slug = models.SlugField()
    category = models.SlugField(default="uncategorized")
    title = models.CharField(max_length=100, default='title')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=1,
        ) # Deleting the user accout assoicated will change author to "ID default which should be set to ARCS or other generic value"
    published = models.DateField()
    content = models.TextField()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('staticpages:static_pages',
                       kwargs={
                                'category' : self.category,
                                'slug' : self.slug
                               })

    def __str__(self):
        return self.title

class Author(models.Model):
    '''Basic author placeholder in the blog'''
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class TermsPage(models.Model):
    ''' basic page for terms '''

    template = 'staticpages/terms-cookies-privacy_detail.html'

    terms_title = models.CharField(max_length=100, default='title')
    version_number = models.CharField(max_length=100, default='v01')
    terms_content = models.TextField()
    max_count = 1

class PressPage(models.Model):
    ''' basic page for Press '''

    template = 'staticpages/press_list.html'

    slug = models.SlugField()
    press_title = models.CharField(max_length=100, default='title')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=1,
        ) # Deleting the user accout assoicated will change author to "ID default which should be set to ARCS or other generic value"
    contact_Email = models.EmailField()
    pressPublishedDate = models.DateField(
        db_index=True,
        )# todo make name more focused on date like datapublished - could be confused with published status
    pressTags = TaggableManager()
    press_body = models.TextField()

    def get_absolute_url(self):
        return reverse('staticpages:archive_date_detail',
                       kwargs={'year' : self.pressPublishedDate.year,
                               'month' : self.pressPublishedDate.month,
                               'day' : self.pressPublishedDate.day,
                               'slug' : self.slug #change from pk id
                               })
