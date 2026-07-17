from django import template
from home.models import SiteSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def site_logo(context):

    request = context["request"]
    settings = SiteSettings.objects.first()

    if not settings:
        return ""

    if request.path.startswith("/perfume"):
        if settings.perfume_logo:
            return settings.perfume_logo.url

    if settings.shoe_logo:
        return settings.shoe_logo.url

    return ""