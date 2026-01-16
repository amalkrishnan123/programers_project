from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import ProductForm,CategoryForm,EnquiryForm
from .models import Category,Product,Enquiry

# Create your views here.
def admin_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('admin_dash')
        else:
            messages.error(request,'Invalid Credentials')
    return render(request,'admin_login.html')

def admin_dashboard(request):
    pro=Product.objects.all()
    cat=Category.objects.all()
    return render(request,'admin_dashboard.html',{'product':pro,'category':cat})

def add_product_category(request):
    product_form=ProductForm()
    category_form=CategoryForm()
    if request.method=='POST':
        if 'product_submit' in request.POST:
            product_form=ProductForm(request.POST,request.FILES)
            if product_form.is_valid():
                product_form.save()
                return redirect('admin_dash')
        elif 'category_submit' in request.POST:
            category_form=CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('admin_dash')
    return render(request,'add_product_category.html',{'product_form':product_form,'category_form':category_form})

def edit_product(request,id):
    item=Product.objects.get(id=id)
    if request.method=='POST':
        product=ProductForm(request.POST,request.FILES,instance=item)
        if product.is_valid():
            product.save()
            return redirect('admin_dash')
    else:
        product= ProductForm(instance=item)
    return render(request,'add_product_category.html',{'product_form':product})

def delete_product(request,id):
    pro=Product.objects.get(id=id)
    pro.delete()
    return redirect('admin_dash')

def edit_category(request,id):
    item=Category.objects.get(id=id)
    if request.method=='POST':
        cat=CategoryForm(request.POST,instance=item)
        if cat.is_valid():
            cat.save()
            return redirect('admin_dash')
    else:
        cat=CategoryForm(instance=item)
    return render(request,'add_product_category.html',{'category_form':cat})

def delete_category(request,id):
    cat=Category.objects.get(id=id)
    cat.delete()
    return redirect('admin_dash')
    
def user_view(request):
    pro=Product.objects.all()
    return render(request,'user_section.html',{'pro':pro})

def user_enquiry(request,id):
    product=Product.objects.get(id=id)
    if request.method=='POST':
        form=EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.enqproduct=product
            enquiry.save()
            return redirect('user_section')
    else:
        form=EnquiryForm()
    return render(request,'user_enquiry.html',{'form':form})

def admin_enquiry(request):
    enq=Enquiry.objects.all()
    sort = request.GET.get('sort')
    if sort == 'latest':
        enq = enq.order_by('-created_at')
    elif sort == 'oldest':
        enq = enq.order_by('created_at')
    return render(request,'admin_enquiry.html',{'enq':enq})

def admin_password_change(request):
     if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password=request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user=request.user
        if not user.check_password(current_password):
            return redirect('password_change')
        if new_password != confirm_password:
            return redirect('password_change')
        user.set_password(new_password)
        user.save()
        return redirect('admin_login_page')
     return render(request,'change_password.html')

def logout_admin(request):
    logout(request)
    return redirect('admin_login_page')