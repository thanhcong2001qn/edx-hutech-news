"""
Signal handlers for HUTECH news integration.
"""
from django.template.loader import render_to_string
from web_fragments.fragment import Fragment
from openedx.core.djangoapps.plugin_api import PluginSettings, PluginSignals

from .models import HutechNewsArticle


def add_hutech_news_dashboard(sender, course, **kwargs):
    """
    Add HUTECH news to the dashboard.
    """
    # Không cần sender hoặc course, nhưng chúng được truyền bởi signal
    try:
        latest_news = HutechNewsArticle.objects.all()[:3]
        
        # Chuẩn bị context cho template fragment
        context = {
            'news_items': latest_news,
        }
        
        # Render template fragment
        html = render_to_string('edx_hutech_news/dashboard_news_fragment.html', context)
        
        # Tạo fragment để đưa vào dashboard
        fragment = Fragment(html)
        fragment.add_css_url('/static/edx_hutech_news/css/hutech_news.css')
        fragment.add_javascript_url('/static/edx_hutech_news/js/hutech_news.js')
        fragment.initialize_js('HutechNewsWidget')
        
        return fragment
    except Exception as e:
        # Log lỗi nhưng không làm crash trang dashboard
        import logging
        logging.getLogger(__name__).error(f"Error adding HUTECH news to dashboard: {e}")
        return None