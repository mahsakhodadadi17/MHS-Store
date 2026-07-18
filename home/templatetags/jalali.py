from django import template
import jdatetime

register = template.Library()

@register.filter
def jalali(value):
    if not value:
        return ""

    try:
        return jdatetime.datetime.fromgregorian(
            datetime=value
        ).strftime("%Y/%m/%d")
    except Exception:
        try:
            return jdatetime.date.fromgregorian(
                date=value
            ).strftime("%Y/%m/%d")
        except Exception:
            return value