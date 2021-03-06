from django.db import models
from django.conf import settings
from .storages import ProtectedStorage

# Create your models here.
User = settings.AUTH_USER_MODEL

# def get_storage_location():
#     if settings.DEBUG:
#         return ProtectedStorage()
#     return LiveProtectedStorage

class ProductLike(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    #id = models.AutoField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    video_link = models.TextField(blank=True, null=True)
    media = models.FileField(storage=ProtectedStorage, upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    inventory = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    can_backorder = models.BooleanField(default=False)
    requires_shipping = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='product_user', blank=True, through=ProductLike)
    timestamp = models.DateTimeField(auto_now_add=True)

    # @property
    # def requires_shipping(self):
    #     return not self.is_digital

    @property
    def can_order(self):
        if self.has_inventory():
            return True
        elif self.can_backorder:
            return True
        return False

    @property
    def order_btn_title(self):
        if self.can_order and not self.has_inventory():
            return "Backorder"
        if not self.can_order:
            return "Cannot purchase"
        return "Purchase"

    def has_inventory(self):
        return self.inventory > 0  # True or False
    
    def remove_items_from_inventory(self, count=1, save=True):
        current_inv = self.inventory
        current_inv -= count
        self.inventory = current_inv
        if save == True:
            self.save()
        return self.inventory

    '''
    Feel free to delete this class
    '''
    class Meta:
        ordering = ['-id']


    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "image": self.image,
            "media": self.media,
            "price": self.price,
        }