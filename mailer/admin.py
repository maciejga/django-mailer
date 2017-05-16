from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mailer.models import Message, DontSendEntry, MessageLog


def show_to(message):
    return ", ".join(message.to_addresses)
show_to.short_description = _("To")  # noqa: E305


class MessageAdminMixin(object):

    def get_actions(self, request):
        actions = super(MessageAdminMixin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def plain_text_body(self, instance):
        email = instance.email
        if hasattr(email, 'body'):
            return email.body
        else:
            return _("<Can't decode>")
    plain_text_body.short_description = _("Plain text body")


class MessageAdmin(MessageAdminMixin, admin.ModelAdmin):

    list_display = ["id", show_to, "subject", "when_added", "priority"]
    readonly_fields = ['plain_text_body']
    #date_hierarchy = "when_added"


class DontSendEntryAdmin(admin.ModelAdmin):

    list_display = ["to_address", "when_added"]


class MessageLogAdmin(MessageAdminMixin, admin.ModelAdmin):

    list_display = ["id", show_to, "subject", "message_id", "when_attempted", "result"]
    list_filter = ["result"]
    #date_hierarchy = "when_attempted"
    readonly_fields = ['message_id', "when_added", "priority", "result", "log_message", "when_attempted", 'plain_text_body',]
    search_fields = ['message_id']
    exclude = ('message_data',)


admin.site.register(Message, MessageAdmin)
#admin.site.register(DontSendEntry, DontSendEntryAdmin)
admin.site.register(MessageLog, MessageLogAdmin)
