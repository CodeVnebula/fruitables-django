from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def language_url(context, language_code="en"):
    value = context['request'].path.lstrip('/')
    
    for lang in settings.LANGUAGES:
        if value.startswith(lang[0] + "/"):
            value = value[len(lang[0]) + 1:]
            break  

    return f"/{language_code}/{value}" if language_code != "en" else f"/{value}"
