"""
Django app configuration cho plugin tin tức HUTECH.
"""
from django.apps import AppConfig


class HutechNewsConfig(AppConfig):
    """
    Configuration cho ứng dụng edx_hutech_news.
    """
    name = 'edx_hutech_news'
    verbose_name = 'HUTECH News'
    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'hutech_news',
                'regex': r'^hutech-news/',
                'relative_path': 'urls',
            },
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'production': {'relative_path': 'settings.production'},
            },
        },
        'signals_config': {
            'lms.djangoapp': {
                'relative_path': 'signals',
                'receivers': [
                    {
                        'receiver_func_name': 'add_hutech_news_dashboard',
                        'signal_path': 'openedx.core.djangoapps.content.course_overviews.signals.COURSE_DASHBOARD_VIEWED',
                    },
                ],
            },
        },
    }

    def ready(self):
        """
        Khởi tạo khi app sẵn sàng.
        """
        # Import signals module để kết nối signal receivers
        import edx_hutech_news.signals  # pylint: disable=import-outside-toplevel