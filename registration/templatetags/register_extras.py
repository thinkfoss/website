from django.template import Library
register = Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})
