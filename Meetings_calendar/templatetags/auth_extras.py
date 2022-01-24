from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def mentor_filter(meetings, mentor):
    return meetings.filter(mentor=mentor)


@register.filter
def student_filter(meetings, student):
    return meetings.filter(student=student)


