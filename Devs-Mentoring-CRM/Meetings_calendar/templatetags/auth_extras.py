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


@register.filter
def user_filter(sub_topic, user):
    return sub_topic.filter(user__student__user__id=user)


@register.filter
def subject_filter(subject, subtopic):
    return subject.filter(id=subtopic)


@register.filter
def students_filter(students, mentor):
    return students.filter(mentor__user__id=mentor)
