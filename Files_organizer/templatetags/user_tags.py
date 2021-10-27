from django import template
from django.contrib.auth.models import Group, User

from Files_organizer.models import SubTopic

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()

    return False


@register.filter(name='has_access')
def has_access(user, subtopic):

    if user in subtopic.user.all():
        return True
    return False
