from django.views.generic import ListView
from django.db.models import Q
from blogs.models import BlogPost
from .forms import SearchForm
from django.shortcuts import render
from django.http import JsonResponse


class SearchView(ListView):
    model = BlogPost
    template_name = 'search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            return BlogPost.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
        return BlogPost.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET or None)
        return context








def search_ajax(request):
    query = request.GET.get('query', '')
    form = SearchForm(initial={'query': query})

    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        posts = BlogPost.objects.none()

    context = {
        'form': form,
        'posts': posts,
        'is_paginated': False,  # No pagination for AJAX results
    }
    
    html = render_to_string('search_results.html', context, request=request)
    return JsonResponse({'html': html})

