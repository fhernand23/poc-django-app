from django.db import models
from django.conf import settings
from django.urls import reverse


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

class Provider(models.Model):
    cuit = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=240, null=True, blank=True)
    documentation = models.FileField(upload_to="files/providers", null=True, blank=True)
    avatar = models.ImageField(upload_to="files/providers", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"
    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('provider-detail', args=[str(self.id)])

class Product(models.Model):
    name = models.CharField(max_length=120)
    short_description = models.CharField(max_length=240, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to="files/products", null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('product-detail', args=[str(self.id)])

class WhLocation(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('whlocation-detail', args=[str(self.id)])


class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=120)
    ACTION_TYPES = (
        ('buy', 'Increase by buy'),
        ('sell', 'Decrease by sell'),
        ('move', 'Move'),
        ('fix', 'Fix'),
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
        blank=True,
        default='fix',
        help_text='Action type')
    quantity = models.IntegerField()
    wh_location = models.ForeignKey(WhLocation, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']
