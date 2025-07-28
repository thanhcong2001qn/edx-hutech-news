"""
Models cho việc lưu trữ tin tức HUTECH.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class HutechNewsArticle(models.Model):
    """
    Model lưu trữ bài viết tin tức từ trang web HUTECH.
    """
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    url = models.URLField(max_length=255, verbose_name=_('URL'), unique=True)
    summary = models.TextField(blank=True, verbose_name=_('Summary'))
    image_url = models.URLField(max_length=255, blank=True, verbose_name=_('Image URL'))
    published_date = models.DateTimeField(verbose_name=_('Published Date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    content = models.TextField(blank=True, verbose_name=_('Content'))

    class Meta:
        """Meta options for HutechNewsArticle."""
        verbose_name = _('HUTECH News Article')
        verbose_name_plural = _('HUTECH News Articles')
        ordering = ['-published_date']

    def __str__(self):
        """String representation of HutechNewsArticle."""
        return self.title