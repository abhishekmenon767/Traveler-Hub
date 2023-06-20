from django import template

from datetime import date, timedelta, datetime

register = template.Library()

@register.simple_tag(name="todays_date")
def get_current_date():
    now = date.today().isoformat() 
    return now

@register.simple_tag
def checkin_dates():
    """
    Returns the current date as a string in the ISO format (YYYY-MM-DD).
    """
    return date.today().isoformat()

def checkout_date(checkin_date):
    """
    Calculates and returns a valid checkout date based on a given check-in date.
    The checkout date must not be earlier than the check-in date.
    """
    checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d').date()
    checkout_date = checkin_date + timedelta(days=1)
    return checkout_date.isoformat()

@register.simple_tag(name="max_date")
def get_current_date():
    max = (date.today()+timedelta(days=30)).isoformat()  
    return max

@register.simple_tag(name="tommorow")
def get_current_date():
    max = (date.today()+timedelta(days=1)).isoformat()
    return max





































































@register.filter
def percentage(value1,value2=100):
    
    return int(value1)/int(value2)*100
