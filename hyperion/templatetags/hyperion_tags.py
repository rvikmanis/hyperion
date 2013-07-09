__author__ = 'Dzedajs'

from django import template
from django.contrib.admin import site
from django.utils.text import capfirst
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpRequest

register = template.Library()
try:
    hyperion_menu_overrides = settings.__getattr__('HYPERION_MENU_OVERRIDES')
except AttributeError:
    hyperion_menu_overrides = {}

try:
    hyperion_admin_site_title = settings.__getattr__('HYPERION_ADMIN_SITE_TITLE')
except AttributeError:
    hyperion_admin_site_title = 'Hyperion'




def admin_menu(user, template='hyperion/_admin_menu.html', for_menu=False, limit_to_app=None):
    DEFAULT_ORDER = 10000

    apps = []
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        model_module_name = model._meta.module_name
        model_name = capfirst(model._meta.verbose_name)
        model_name_plural = capfirst(model._meta.verbose_name_plural)

        if limit_to_app and limit_to_app != app_label:
            continue

        request = HttpRequest()
        request.user = user
        if user.has_module_perms(app_label):
            perms = model_admin.get_model_perms(request)


            if True in perms.values():

                if not app_label in dict(apps).keys():
                    if app_label in hyperion_menu_overrides.keys():
                        app_name = hyperion_menu_overrides[app_label].get('name', app_label.title())
                        order = hyperion_menu_overrides[app_label].get('order', DEFAULT_ORDER)
                    else:
                        app_name = app_label.title()
                        order = DEFAULT_ORDER

                    app_dict = {
                        'models': [],
                        'url': reverse('admin:app_list', kwargs={'app_label': app_label}),
                        'name': app_name,
                        'order': order
                    }
                    if for_menu and app_label in hyperion_menu_overrides.keys() and hyperion_menu_overrides[app_label].get('exclude', False):
                        continue
                    else:
                        apps.append( (app_label, app_dict) )



                model_full_dotted_name = (app_label, model_module_name)
                app_index = [ apps.index(a) for a in apps if a[0]==app_label ][0]

                if model_full_dotted_name in hyperion_menu_overrides.keys():
                    model_display_name = hyperion_menu_overrides[model_full_dotted_name].get('name', model_name_plural)
                    order = hyperion_menu_overrides[model_full_dotted_name].get('order', DEFAULT_ORDER)
                else:
                    model_display_name = model_name_plural
                    order = DEFAULT_ORDER

                if perms.get('add', False):
                    add_url = reverse('admin:%s_%s_add' % (app_label, model_module_name))
                else:
                    add_url = None

                if perms.get('change', False):
                    edit_url = reverse('admin:%s_%s_changelist' % (app_label, model_module_name))
                else:
                    edit_url = None

                model_dict = {
                    'name': model_display_name,
                    'name_singular': model_name,
                    'url': edit_url,
                    'add_url': add_url,
                    'order': order
                }
                if for_menu and model_full_dotted_name in hyperion_menu_overrides.keys() and hyperion_menu_overrides[model_full_dotted_name].get('exclude', False):
                    continue
                else:
                    apps[app_index][1]['models'].append( (model_module_name, model_dict) )


    apps.sort(key=lambda x: x[1]['name'])
    apps = sorted(apps, lambda x,y: cmp(x[1]['order'], y[1]['order']))
    for app_label, app in apps:
        app['models'].sort(key=lambda x: x[1]['name'])
        app['models'] = sorted(app['models'], lambda x,y: cmp(x[1]['order'], y[1]['order']))
    return render_to_string(template, {'apps': apps})

register.simple_tag(admin_menu)





def app_title(app_label, default=None):
    if app_label in hyperion_menu_overrides.keys():
        return hyperion_menu_overrides[app_label].get('name', default)

register.simple_tag(app_title)




def admin_site_title():
    return hyperion_admin_site_title

register.simple_tag(admin_site_title)