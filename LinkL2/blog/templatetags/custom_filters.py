from django import template

register = template.Library()

@register.filter(name="lookup")
def lookup_dict_filter(dictionary, key):
    return dictionary.get(key)

@register.filter(name="get_user")
def get_user_from_rec(user_comment_rec):
    return user_comment_rec[0]

@register.filter(name="get_comment")
def get_comment_from_rec(user_comment_rec):
        return user_comment_rec[1]