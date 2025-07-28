CELERYBEAT_SCHEDULE = {
    'fetch-hutech-news': {
        'task': 'edx_hutech_news.tasks.fetch_hutech_news',
        'schedule': 3600,  # Chạy hàng giờ (3600 giây)
        'options': {'queue': 'default'},
    },
}