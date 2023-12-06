from django import template

def email_cut(value: str, *_):
    """Cuts an email"""
    return value.split("@")[0]

register = template.Library()
register.filter("email_cut", email_cut)