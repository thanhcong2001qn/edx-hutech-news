"""
Celery tasks để thu thập tin tức HUTECH.
"""
import logging
from celery import shared_task
from django.db import transaction

from .models import HutechNewsArticle
from .scraper import HutechNewsScraper

logger = logging.getLogger(__name__)


@shared_task
def fetch_hutech_news():
    """
    Celery task để thu thập và cập nhật tin tức HUTECH.
    """
    try:
        scraper = HutechNewsScraper()
        news_items = scraper.get_latest_news(limit=10)
        
        with transaction.atomic():
            for item in news_items:
                # Kiểm tra xem bài viết đã tồn tại chưa dựa trên URL
                article, created = HutechNewsArticle.objects.update_or_create(
                    url=item['url'],
                    defaults={
                        'title': item['title'],
                        'summary': item['summary'],
                        'image_url': item['image_url'],
                        'published_date': item['published_date'],
                    }
                )
                
                # Nếu là bài viết mới, thu thập nội dung đầy đủ
                if created:
                    content = scraper.fetch_article_content(item['url'])
                    if content:
                        article.content = content
                        article.save()
        
        logger.info(f"Successfully fetched {len(news_items)} HUTECH news articles")
        return f"Successfully fetched {len(news_items)} HUTECH news articles"
    except Exception as e:
        logger.error(f"Error fetching HUTECH news: {e}")
        raise