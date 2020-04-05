from django import template
from django.utils.html import format_html

register = template.Library()


def user_context(context):
    """
    Return the user object from the context dictionary.
    :param context: The context dictionary.
    :return: Return None if the user is anonymous
    Return the user otherwise.
    """
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user
    user_is_anonymous = user.is_anonymous

    if user_is_anonymous:
        return None
    return user


@register.simple_tag(takes_context=True)
def live_notify_badge(context, badge_class='live_notify_badge'):
    """
    The takes_context argument means that this function need to refer to the current context of the page.
    """
    user = user_context(context)
    if not user:
        return ''

    html = "<span class='{badge_class}'>{unread}</span>".format(
        badge_class=badge_class, unread=user.notifications.unread().count()
    )
    return format_html(html)

