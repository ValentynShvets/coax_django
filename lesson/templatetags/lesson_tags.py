from django import template

register = template.Library()


@register.filter(name='check_if_user_liked')
def check_if_user_liked(likes, user_id):
    return likes.filter(user=user_id).exists()  # check if relationship
