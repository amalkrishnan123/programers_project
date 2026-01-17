from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import ProductForm,CategoryForm,EnquiryForm
from .models import Category,Product,Enquiry
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Enquiry

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
            enquiry.product=product
            enquiry.save()
            return redirect('user_section')
    else:
        form=EnquiryForm()
    return render(request,'user_enquiry.html',{'form':form})

def admin_enquiry(request,id):
    product=get_object_or_404(Product,id=id)
    enq=Enquiry.objects.filter(product=product)
    sort = request.GET.get('sort')
    if sort == 'latest':
        enq = enq.order_by('-created_at')
    elif sort == 'oldest':
        enq = enq.order_by('created_at')
    return render(request,'admin_enquiry.html',{'enq':enq,'product_id':id})

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

def enquiry_pdf_report(request,id):
    product=get_object_or_404(Product,id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enquiry_report.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    title = Paragraph("<b>Enquiry Report</b>", styles['Title'])
    elements.append(title)
    data = [
        [
            "Name", "Mobile","Address","Product",
            "Quantity", "Date"
        ]
    ]
    enquiries = Enquiry.objects.filter(product=product)
    print(enquiries)
    for enq in enquiries:
        data.append([
            enq.name,
            enq.mobile,
            enq.address,
            enq.product.name,
            enq.quantity,
            enq.created_at.strftime("%d-%m-%Y"),
        ])
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ]))
    elements.append(table)
    pdf.build(elements)
    return response