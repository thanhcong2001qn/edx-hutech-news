"""
Views for edx_hutech_news.
"""
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from opaque_keys.edx.keys import CourseKey
from lms.djangoapps.courseware.courses import get_course_with_access

from .models import HutechNewsArticle

logger = logging.getLogger(__name__)


@cache_page(60 * 15)  # Cache for 15 minutes
def hutech_news_fragment(request):
    """
    Render HUTECH news as a fragment that can be included in a page.
    """
    latest_news = HutechNewsArticle.objects.all()[:5]
    context = {
        'news_items': latest_news,
    }
    return render(request, 'edx_hutech_news/hutech_news_fragment.html', context)


def hutech_news_json(request):
    """
    Return HUTECH news as JSON for AJAX requests.
    """
    latest_news = HutechNewsArticle.objects.all()[:5]
    news_list = []
    
    for news in latest_news:
        news_list.append({
            'title': news.title,
            'url': news.url,
            'summary': news.summary,
            'image_url': news.image_url,
            'published_date': news.published_date.isoformat(),
        })
    
    return JsonResponse({'news': news_list})


def hutech_news_page(request):
    """
    Full page view for HUTECH news.
    """
    news_items = HutechNewsArticle.objects.all()[:20]
    context = {
        'news_items': news_items,
    }
    return render(request, 'edx_hutech_news/hutech_news_page.html', context)


def hutech_news_detail(request, article_id):
    """
    Display a single news article in detail.
    """
    try:
        article = HutechNewsArticle.objects.get(id=article_id)
        context = {
            'article': article,
        }
        return render(request, 'edx_hutech_news/hutech_news_detail.html', context)
    except HutechNewsArticle.DoesNotExist:
        return render(request, 'edx_hutech_news/article_not_found.html', {})