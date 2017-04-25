from django import template
from rango.models import Campus

register = template.Library()

@register.inclusion_tag('rango/cams.html')
def get_campus_list(cam=None):
    return {'cams': Campus.objects.all(), 'act_cam': cam}