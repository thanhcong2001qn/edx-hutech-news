from setuptools import setup

setup(
    name="edx-hutech-news",
    version="0.1.0",
    description="Open edX plugin để thu thập và hiển thị tin tức từ trang web HUTECH",
    author="ThanhCong",
    author_email="thanhcong2001qn@example.com",
    packages=["edx_hutech_news"],
    install_requires=[
        "Django",
        "beautifulsoup4",
        "requests",
        "celery",
        "lxml",
    ],
    entry_points={
        "lms.djangoapp": [
            "edx_hutech_news = edx_hutech_news.apps:HutechNewsConfig",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)