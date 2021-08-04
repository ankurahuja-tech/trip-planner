from django import template
import datetime


register = template.Library()


@register.filter()
def addDay(value: datetime.date) -> datetime.date:
    """
    Given a date value, adds 1 day to a given date.
    Intended use: template with Fullcalendar's calendar view, to make trip's "end" date inclusive while rendering.
    """
    newDate = value + datetime.timedelta(days=1)
    return newDate
