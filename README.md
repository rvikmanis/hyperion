Hyperion - django administration theme
======================================

A nice simple theme for django admin.


Features
--------------

* Looks good
* Styles for FeinCMS item editor
* Configurable admin-wide navigation
* Pretty app labels


Screenshots
----------------

Change list:
![Screenshot #1](http://oi44.tinypic.com/v6rupd.jpg)

Change form:
![Screenshot #2](http://s2.postimg.org/432zgo2op/hyperion.png)


Requirements
------------------

* Django >= 1.4


Compatibility
------------------

* FeinCMS >= 1.6.2



Installation
------------------------------------

1. Clone our repo somewhere in your project's include path

        git clone https://github.com/rvikmanis/hyperion.git

2. Add `hyperion` to `INSTALLED_APPS` before `django.contrib.admin`.


Configuration
--------------------

### HYPERION_MENU_OVERRIDES

By default hyperion shows all apps and models from `admin.site._registry`.

To exclude `yourapp` from the menu add this to project settings:

    HYPERION_MENU_OVERRIDES = {

        'yourapp': {
            'exclude': True
        }

    }

Pretty app names:

    HYPERION_MENU_OVERRIDES = {

        'yourapp': {
            'name': 'Your Great Application'
        }

    }

And custom ordering:

    HYPERION_MENU_OVERRIDES = {

        'yourapp': {
            'name': 'Your Great Application',
            'order': 1
        },
        'auth': {
            'name': 'Users & Groups',
            'order': 2
        }

    }

Do the same with models:

    HYPERION_MENU_OVERRIDES = {

        'yourapp': {
            'name': 'Your Great Application',
            'order': 1
        },
        'yourapp.entry': {
            'name': 'Catalog entries',
            'order': 1
        },
        'yourapp.catalog': {
            'name': 'Catalog (the one containing entries)',
            'order': 2
        }

    }

### HYPERION_ADMIN_SITE_TITLE

Change the admin site title. Default is "Hyperion":

    HYPERION_ADMIN_SITE_TITLE = 'My Administration System'
