from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    amount=models.PositiveIntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='catex')
    image=models.ImageField(upload_to='product_images')

    def __str__(self):
        return f"{self.name}"
    
class Enquiry(models.Model):
    name=models.CharField(max_length=100)
    address=models.TextField()
    mobile=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    is_contact=models.BooleanField(default=False)
    remarks=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='enqproduct')

