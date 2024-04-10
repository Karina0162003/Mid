from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from django.contrib.admin.models import LogEntry

admin.site.site_header = "RA"
admin.site.index_title = "Welcome to Agriculture Website"
admin.site.site_title = "Revolutionizing Agriculture"


class a1(admin.ModelAdmin):
    list_display = ['id', 'name']


class a2(admin.ModelAdmin):
    list_display = ['name', 'pincode', 'city_name']
    list_filter = ['city_name']
    list_per_page = 5


class a3(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact', 'email', 'area_name']


class a4(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'contact', 'email', 'address']
    list_filter = ['first_name']
    list_per_page = 5


class a5(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'f1', 'price', 'manufacturedate', 'expirydate', 'ava_quantity',
                    'Category',
                    'filter']
    list_filter = ['Category', 'name', 'filter']
    list_per_page = 10


class a6(admin.ModelAdmin):
    list_display = ['id', 'name', 'f1', 'Subcategory']
    list_per_page = 5


class a8(admin.ModelAdmin):
    list_display = ['date', 'delivery_address', 'iscancel', 'payment_status', 'totalamount', 'customer_name',
                     'paymentmode']


class a9(admin.ModelAdmin):
    list_display = ['id', 'salesorder_name', 'product_name', 'quantity']


class a10(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact', 'email', 'company_name', 'prodct_name', 'area_name']


class a11(admin.ModelAdmin):
    list_display = ['product_name', 'customer_name', 'quantity', 'totalprice', 'product_status', 'orderid']


class a12(admin.ModelAdmin):
    list_display = ['date', 'customer_name', 'saleorder_name', 'payment_type', 'total_amount', 'saleorder_name']
    list_per_page = 5
    list_filter = ['customer_name', 'date']


class a13(admin.ModelAdmin):
    list_display = ['rating', 'customer_name', 'product_name', 'description', 'date']
    list_per_page = 5
    list_filter = ['product_name', 'rating', 'customer_name']


class a14(admin.ModelAdmin):
    list_display = ['id', 'name', 'company_name']


class a15(admin.ModelAdmin):
    list_display = ['id', 'name']


class a7(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message']
    list_filter = ['user', 'object_id', 'action_time']
class a16(admin.ModelAdmin):
    list_display = ['product_id', 'customer_id', 'time_duration', 'rent_amount', 'payment_type','booked_date']


class a17(admin.ModelAdmin):
    list_display = ['date_time', 'status', 'salesorder_id']


admin.site.register(city, a1)
admin.site.register(area, a2)
admin.site.register(company, a3)
admin.site.register(customer, a4)
admin.site.register(product, a5)
admin.site.register(productcategory, a6)
admin.site.register(salesorder, a8)
admin.site.register(salesorder_detail, a9)
admin.site.register(supplier, a10)
admin.site.register(cart, a11)
admin.site.register(payment, a12)
admin.site.register(feedback1, a13)
admin.site.register(report1, a14)
admin.site.register(filter, a15)
admin.site.register(rentmachinery, a16)
admin.site.register(LogEntry, a7)
admin.site.register(Order_Status, a17)
