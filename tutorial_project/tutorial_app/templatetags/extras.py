from django import template
from tutorial_app.models import Category

register = template.Library()

@register.inclusion_tag('cat.html')
def get_category_list(cat=None):
		return {'cats': Category.objects.all(), 'act_cat': cat}
		
@register.filter(name='addcls')
def addcls(value, cls):
		return value.as_widget(attrs={'class':cls})