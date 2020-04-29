from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import DetailView
from publications.models import Article

from django.db.models import Q




class ArticleListView(ListView):
    '''
    '''
    model = Article
    template_name = 'publications/article_list.html'


class ArticleDetailView(DetailView):
    '''
    '''
    model = Article
    template_name = 'publications/article_detail.html'



class SearchResultsView(ListView):
    model = Article
    template_name = 'publications/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('x')
        #
        object_list = Article.objects.filter(
            Q(title__icontains=query))
            #Q(keywords__keyword__icontains=query) |
            #Q(abstract__icontains=query
            #))
        return object_list
