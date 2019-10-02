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
def archive_month_year():
    current_time = timezone.now()
    previous_month = current_time.month - 1
    current_year = current_time.year
    first_post = Post.objects.published().order_by("-published").first()
    first_post_published_time = first_post.published
    first_post_published_month = first_post_published_time.month
    first_post_published_year = first_post_published_time.year
    archive_month_year = {}

    year_list = [i for i in range(first_post_published_year, current_year+1)]
    return year_list


