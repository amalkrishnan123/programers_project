from .models import Product,Category,Enquiry
from django.forms import ModelForm

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'

class CategoryForm(ModelForm):
    class Meta:
        model=Category
        fields='__all__'

class EnquiryForm(ModelForm):
    class Meta:
        model=Enquiry
        fields=['name','address','mobile','quantity',]