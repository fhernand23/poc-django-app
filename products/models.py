from django.db import models
from django.conf import settings


AppUser = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """
    Notification or log
    """
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    app_name = models.CharField(max_length=120, null=True, blank=True)
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
    dest_user_id = models.CharField(max_length=120, null=True, blank=True)
    tags = models.CharField(max_length=120, null=True, blank=True)
    id_file = models.CharField(max_length=120, null=True, blank=True)
    file_resource = models.JSONField(help_text='File resource related', blank=True, null=True)


class Provider(models.Model):
    cuit = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=240, null=True, blank=True)
    documentation = models.FileField(upload_to="files/providers", null=True, blank=True)
    avatar = models.ImageField(upload_to="files/providers", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=120)
    short_description = models.CharField(max_length=240, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to="files/products", null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


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
    location = models.CharField(max_length=120, null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']
