from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import TildaArticle


def article(request, pk):
    article = get_object_or_404(TildaArticle, id=pk)
    return render(request, 'tilda/article.html', {'article': article})
