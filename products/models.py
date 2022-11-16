from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid


AppUser = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=120)
    short_description = models.CharField(max_length=240, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to="files/products", null=True, blank=True)
    code = models.CharField(max_length=240, null=True, blank=True)
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

    def get_api_url(self):
        """Returns the url to access a particular instance."""
        return reverse('product-api-detail', args=[str(self.id)])

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "122"

class Provider(models.Model):
    cuit = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=240, null=True, blank=True)
    documentation = models.FileField(upload_to="files/providers", null=True, blank=True)
    avatar = models.ImageField(upload_to="files/providers", null=True, blank=True)
    products = models.ManyToManyField(Product)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('provider-detail', args=[str(self.id)])

    def get_api_url(self):
        """Returns the url to access a particular instance."""
        return reverse('provider-api-detail', args=[str(self.id)])


class WhLocation(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('whlocation-detail', args=[str(self.id)])

    def get_api_url(self):
        """Returns the url to access a particular instance."""
        return reverse('whlocation-api-detail', args=[str(self.id)])


class Client(models.Model):
    cuit = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=240, null=True, blank=True)
    documentation = models.FileField(upload_to="files/clients", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('client-detail', args=[str(self.id)])

    def get_api_url(self):
        """Returns the url to access a particular instance."""
        return reverse('client-api-detail', args=[str(self.id)])


class ProductMoveType(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return f"{self.name}"

class ProductPackaging(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return f"{self.name}"

class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=240, null=True, blank=True)
    quantity = models.IntegerField()
    wh_location = models.ForeignKey(WhLocation, on_delete=models.SET_NULL, null=True, blank=True)
    product_packaging = models.ForeignKey(ProductPackaging, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4)
    lot = models.CharField(max_length=120, null=True, blank=True)
    unit_valuation = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    related_moves = models.CharField(max_length=120, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('productunit-detail', args=[str(self.id)])

    def get_api_url(self):
        return reverse('productunit-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.product.name} on {self.date_created}"


class ProductMove(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.DO_NOTHING, null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, blank=True)
    move_type = models.ForeignKey(ProductMoveType, on_delete=models.DO_NOTHING, null=True, blank=True)
    wh_location_to = models.ForeignKey(WhLocation, on_delete=models.SET_NULL, null=True, blank=True)
    product_packaging = models.ForeignKey(ProductPackaging, on_delete=models.SET_NULL, null=True, blank=True)
    move_date = models.DateTimeField(null=True, blank=True)
    lot = models.CharField(max_length=120, null=True, blank=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    unit_taxes = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    new_unit_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    new_unit_taxes = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    new_total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    unit_valuation = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4)
    expiration_date = models.DateTimeField(null=True, blank=True)
    related_units = models.CharField(max_length=120, null=True, blank=True)
    add_qr = models.BooleanField(default=False)
    rfid_code = models.CharField(max_length=240, null=True, blank=True)
    description = models.CharField(max_length=240, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('productmove-detail', args=[str(self.id)])

    def get_api_url(self):
        """Returns the url to access a particular instance."""
        return reverse('productmove-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.product.name} on {self.date_created}"


class LogisticUnitCode(models.Model):
    entity = models.CharField(max_length=20)
    entity_id = models.CharField(max_length=20)
    description = models.CharField(max_length=240, null=True, blank=True)
    rfid_code = models.CharField(max_length=240, null=True, blank=True)
    qr_code = models.ImageField(upload_to="files/codes", null=True, blank=True)
    entity_url = models.CharField(max_length=240, null=True, blank=True)
    entity_api_url = models.CharField(max_length=240, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.entity} {self.entity_id}"
