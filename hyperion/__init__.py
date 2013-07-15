from django.contrib.admin import options
from django.contrib.admin.widgets import AdminSplitDateTime
import django.db.models
from django.utils.translation import ugettext as _


# django 1.4 compat
try:
    from django.utils.html import format_html
except ImportError:
    pass
else:
    class FixedAdminSDT(AdminSplitDateTime):
        def format_output(self, rendered_widgets):
            return format_html('<p class="datetime"><span class="sublabel">{0}</span> {1}<br /><span class="sublabel">{2}</span> {3}</p>',
                               _('Date:'), rendered_widgets[0],
                               _('Time:'), rendered_widgets[1])

    options.FORMFIELD_FOR_DBFIELD_DEFAULTS[django.db.models.DateTimeField]['widget'] = FixedAdminSDT

