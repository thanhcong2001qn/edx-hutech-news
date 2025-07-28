"""
Mã nguồn thu thập tin tức từ trang web HUTECH.
"""
import logging
import datetime
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.utils.dateparse import parse_datetime

logger = logging.getLogger(__name__)

HUTECH_NEWS_URL = "https://www.hutech.edu.vn/homepage/tin-tuc/tin-hutech"


class HutechNewsScraper:
    """
    Thu thập tin tức từ trang web HUTECH.
    """

    def fetch_news_page(self, url: str = HUTECH_NEWS_URL) -> Optional[str]:
        """
        Tải trang web tin tức.
        
        Args:
            url: URL trang tin tức cần thu thập
            
        Returns:
            Nội dung HTML của trang hoặc None nếu có lỗi
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.content
        except requests.RequestException as e:
            logger.error(f"Error fetching HUTECH news: {e}")
            return None

    def parse_news_list(self, html_content: str) -> List[Dict]:
        """
        Phân tích HTML để trích xuất danh sách tin tức.
        
        Args:
            html_content: Nội dung HTML của trang
            
        Returns:
            Danh sách tin tức đã được trích xuất
        """
        if not html_content:
            return []

        news_items = []
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Điều chỉnh selector theo cấu trúc thực tế của trang web HUTECH
        # Đây là ví dụ và cần thay đổi cho phù hợp với HTML thực tế
        news_containers = soup.select('.news-list .news-item')
        
        for item in news_containers:
            try:
                # Điều chỉnh selectors này theo cấu trúc HTML thực tế
                title_elem = item.select_one('.news-title a')
                image_elem = item.select_one('.news-image img')
                date_elem = item.select_one('.news-date')
                summary_elem = item.select_one('.news-summary')
                
                if not title_elem or not title_elem.get('href'):
                    continue
                
                # Xây dựng URL đầy đủ từ đường dẫn tương đối
                url = title_elem.get('href')
                if not url.startswith('http'):
                    url = f"https://www.hutech.edu.vn{url}" if not url.startswith('/') else f"https://www.hutech.edu.vn{url}"
                
                # Trích xuất ngày từ định dạng thông thường (ví dụ: "DD/MM/YYYY")
                published_date = None
                if date_elem:
                    date_text = date_elem.text.strip()
                    try:
                        # Điều chỉnh định dạng phân tích ngày theo định dạng thực tế
                        # Ví dụ: "27/07/2025" -> datetime(2025, 7, 27)
                        day, month, year = map(int, date_text.split('/'))
                        published_date = timezone.make_aware(
                            datetime.datetime(year, month, day)
                        )
                    except (ValueError, AttributeError):
                        published_date = timezone.now()
                else:
                    published_date = timezone.now()
                
                image_url = ""
                if image_elem and image_elem.get('src'):
                    image_url = image_elem.get('src')
                    if not image_url.startswith('http'):
                        image_url = f"https://www.hutech.edu.vn{image_url}" if not image_url.startswith('/') else f"https://www.hutech.edu.vn{image_url}"
                
                summary = ""
                if summary_elem:
                    summary = summary_elem.text.strip()
                
                news_items.append({
                    'title': title_elem.text.strip(),
                    'url': url,
                    'image_url': image_url,
                    'published_date': published_date,
                    'summary': summary
                })
                
            except Exception as e:
                logger.error(f"Error parsing news item: {e}")
                continue
        
        return news_items

    def fetch_article_content(self, url: str) -> Optional[str]:
        """
        Tải và trích xuất nội dung của một bài viết cụ thể.
        
        Args:
            url: URL của bài viết
            
        Returns:
            Nội dung HTML đã trích xuất hoặc None nếu có lỗi
        """
        html_content = self.fetch_news_page(url)
        if not html_content:
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            # Điều chỉnh selector này để trỏ đến phần tử chứa nội dung bài viết
            article_content = soup.select_one('.article-content')
            
            if article_content:
                return str(article_content)
            return None
        except Exception as e:
            logger.error(f"Error fetching article content: {e}")
            return None

    def get_latest_news(self, limit: int = 5) -> List[Dict]:
        """
        Thu thập tin tức mới nhất từ trang web HUTECH.
        
        Args:
            limit: Số lượng tin tức tối đa cần lấy
            
        Returns:
            Danh sách tin tức mới nhất
        """
        html_content = self.fetch_news_page()
        if not html_content:
            return []
        
        news_items = self.parse_news_list(html_content)
        return news_items[:limit]