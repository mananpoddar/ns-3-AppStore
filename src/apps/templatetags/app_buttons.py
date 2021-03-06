from django import template
from apps.models import App, Release

register = template.Library()

@register.inclusion_tag('app_button.html')
def app_button(app, order_index):
    app.star_percentage = 100 * app.stars / 5 / app.votes if app.votes else 0
    c = {}
    c['app'] = app
    c['order_index'] = order_index
    return c

@register.inclusion_tag('app_button.html')
def app_button_by_name(app_name):
    app = App.objects.get(name = app_name)
    c = {}
    c['app'] = app
    return c

@register.inclusion_tag('app_buttons.html')
def app_buttons(apps):
    return {'apps': apps}

@register.inclusion_tag('list_of_apps.html')
def list_of_apps(apps, include_relevancy = False):
    #FIXME
    apps_with_releases = filter(lambda a: a.has_releases, apps)
    apps_without_releases = filter(lambda a: not a.has_releases, apps)
    # a list of sort buttons to display
                    # button name       div attr name          attr type
    sort_criteria = (('name',           'fullname',            'str'),
                     ('votes',          'votes',               'int'),
                     ('newest release', 'latest_release_date', 'date'))
    if (include_relevancy):
        sort_criteria = (('relevancy',  'order_index',  'int'), ) + sort_criteria
    return {'apps_with_releases': apps,
            'apps_without_releases': apps_without_releases,
            'sort_criteria': sort_criteria}
