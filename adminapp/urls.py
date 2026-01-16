from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_view,name='user_section'),
    path('user_enq/<int:id>',views.user_enquiry,name='user_enq'),
    path('admin_enquiry/',views.admin_enquiry,name='admin_enq'),
    path('admin_page/',views.admin_login,name='admin_login_page'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dash'),
    path('add_products/',views.add_product_category,name='add_prodct'),
    path('edit_product/<int:id>',views.edit_product,name='edit_pro'),
    path('product_del/<int:id>',views.delete_product,name='delete'),
    path('category_edit/<int:id>',views.edit_category,name='edit_cat'),
    path('category_delete/<int:id>',views.delete_category,name='delete_cat'),
    path('password_change/',views.admin_password_change,name='password_change'),
    path('logout_ad/',views.logout_admin,name='logout_admin')

]
