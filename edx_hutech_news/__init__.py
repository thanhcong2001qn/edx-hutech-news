"""
Plugin lấy tin tức HUTECH cho Open edX.

Plugin này thu thập tin tức từ trang web HUTECH (https://www.hutech.edu.vn/homepage/tin-tuc/tin-hutech)
và hiển thị chúng trên nền tảng Open edX.
"""
import logging
from django.conf import settings
from django.utils.module_loading import import_module

__version__ = '0.1.0'

default_app_config = 'edx_hutech_news.apps.HutechNewsConfig'

logger = logging.getLogger(__name__)


def is_hutech_news_enabled():
    """
    Kiểm tra xem tính năng HUTECH News có được kích hoạt không.
    
    Returns:
        bool: True nếu HUTECH News được kích hoạt, False nếu không.
    """
    return getattr(settings, 'FEATURES', {}).get('ENABLE_HUTECH_NEWS', False)


def get_hutech_news_settings():
    """
    Lấy cấu hình cho HUTECH News.
    
    Returns:
        dict: Cấu hình HUTECH News.
    """
    return getattr(settings, 'HUTECH_NEWS_SETTINGS', {
        'refresh_interval': 3600,  # Thời gian làm mới tin tức (giây)
        'max_news_items': 10,      # Số lượng tin tức tối đa hiển thị
        'news_url': 'https://www.hutech.edu.vn/homepage/tin-tuc/tin-hutech',
        'enable_dashboard_widget': True,  # Hiển thị widget trên dashboard
    })


def register_signals():
    """
    Đăng ký các signal handlers cho plugin.
    """
    try:
        import_module('edx_hutech_news.signals')
        logger.debug('HUTECH News signals registered successfully')
    except ImportError as exc:
        logger.error(f'Error registering HUTECH News signals: {exc}')


def manual_fetch_news():
    """
    Kích hoạt việc thu thập tin tức thủ công.
    
    Returns:
        str: Kết quả của việc thu thập tin tức.
    """
    try:
        from .tasks import fetch_hutech_news
        return fetch_hutech_news()
    except ImportError:
        logger.error("Could not import fetch_hutech_news task")
        return "Error: Could not fetch news"


# Nếu plugin được kích hoạt, tự động đăng ký signals
if is_hutech_news_enabled():
    register_signals()