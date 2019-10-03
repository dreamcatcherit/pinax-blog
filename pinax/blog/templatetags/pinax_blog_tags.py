from django import template
from django.utils import timezone

from ..models import Post, Section


register = template.Library()


@register.simple_tag
def latest_blog_posts(scoper=None):
    qs = Post.objects.current()
    if scoper:
        qs = qs.filter(blog__scoper=scoper)
    return qs[:5]


@register.simple_tag
def latest_blog_post(scoper=None):
    qs = Post.objects.current()
    if scoper:
        qs = qs.filter(blog__scoper=scoper)
    return qs[0]


@register.simple_tag
def latest_section_post(section, scoper=None):
    qs = Post.objects.published().filter(section__name=section).order_by("-published")
    if scoper:
        qs = qs.filter(blog__scoper=scoper)
    return qs[0] if qs.count() > 0 else None


@register.simple_tag
def blog_sections():
    return Section.objects.filter(enabled=True)


@register.simple_tag
def archive_blog_posts():
    current_time = timezone.now()
    current_month = current_time.month
    current_year = current_time.year
    archive_posts = Post.objects.published().exclude(published__month=current_month, published__year=current_year)
    return archive_posts
