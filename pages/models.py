from django.db import models
from django.conf import settings

AppUser = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """
    Notification or log
    """
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120, default="Notification title")
    content = models.TextField(default="Notification content")
    object_type = models.CharField(max_length=120, null=True, blank=True)
    object_id = models.CharField(max_length=120, null=True, blank=True)
    object_name = models.CharField(max_length=120, null=True, blank=True)
    NOTE_TYPES = (
        ('log', 'Log'),
        ('error', 'Error'),
        ('direct', 'Direct'),
        ('upload', 'Upload'),
        ('mail', 'Mail'),
        ('call', 'Call'),
        ('event', 'Event'),
        ('state-change', 'State change'),
    )
    status = models.CharField(
        max_length=15,
        choices=NOTE_TYPES,
        blank=True,
        default='log',
        help_text='Notification type')
    from_user_id = models.CharField(max_length=120, null=True, blank=True)
    attach = models.FileField(upload_to="files/notifications", null=True, blank=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creation_date']

    @property
    def table_class(self):
        if self.status == 'error':
            return 'table-danger'
        elif self.status == 'event':
            return 'table-warning'
        return 'table-info'

    @property
    def ui_icon(self):
        if self.status == 'error':
            return 'alert-triangle'
        elif self.status == 'direct':
            return 'message-square'
        elif self.status == 'upload':
            return 'paperclip'
        elif self.status == 'mail':
            return 'mail'
        elif self.status == 'call':
            return 'phone'
        elif self.status == 'event':
            return 'bell'
        elif self.status == 'state-change':
            return 'repeat'
        return 'info'

    @property
    def ui_color(self):
        if self.status == 'error':
            return 'text-danger'
        elif self.status == 'event':
            return 'text-warning'
        return 'text-info'
