from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
from django.db import models

from django.db import models
from django.utils.safestring import mark_safe


payment_list = (
    ('1', 'Cash On Delivery'),
    ('2', 'UPI'),
    ('3', 'Card')
)
slot = (

    ('1', '8:00 AM to 10:00 AM'),
    ('2', '10:00 AM to 12:00 PM'),
    ('3', '12:00 PM to 2:00 PM'),
    ('4', '2:00 PM to 4:00 PM'),
    ('5', '4:00 PM to 6:00 PM'),
    ('6', '6:00 PM TO 8:00 PM')
)

order_status=(
    ('1','Waiting for Accept'),
    ('2','Accepted'),   
    ('3','Delivered'),
    ('4','Canceled'),
)

# Create your models here.
class city(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Check that the Name does not contain only digits
        if self.name.isdigit():
            raise ValidationError('Name should not contain only digits.')
        super().clean()


class area(models.Model):
    pincode = models.DecimalField(max_digits=6, decimal_places=0)
    name = models.CharField(max_length=40, unique=True)
    city_name = models.ForeignKey(city, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Check that the Name does not contain only digits
        if self.name.isdigit():
            raise ValidationError('Name should not contain only digits.')
        super().clean()


class company(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField(null=False)
    contact = models.DecimalField(max_digits=10, decimal_places=0)
    email = models.EmailField(unique=True)
    area_name = models.ForeignKey(area, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # Check that the Name does not contain only numerics
        if self.name.isdigit():
            raise ValidationError('Name should not contain only numerics.')

        # Check that the Address does not contain only numerics
        if self.address.isdigit():
            raise ValidationError('Address should not contain only numerics.')

        super().clean()


class customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    contact = models.CharField(max_length=10, null=False, unique=True)
    address = models.TextField(null=False)

    def __str__(self):
        return self.first_name

    def clean(self):
        if self.first_name.isdigit() or self.last_name.isdigit():
            raise ValidationError("Name should not contain only digits.")


class filter(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


def validate_image_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png']
    extension = value.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError('Only JPG and PNG files are allowed.')


class productcategory(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    image = models.ImageField(upload_to='photos', validators=[validate_image_extension])
    Subcategory = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def f1(self):
        return mark_safe('<img src="{}" width="10%">'.format(self.image.url))


class product(models.Model):
    name = models.CharField(max_length=70, unique=True)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='photos', null=False, validators=[validate_image_extension])
    price = models.IntegerField(null=False)
    manufacturedate = models.DateField(blank=True, null=True)
    expirydate = models.DateField(blank=True, null=True)
    ava_quantity = models.IntegerField(default=0)
    Category = models.ForeignKey('productcategory', on_delete=models.SET_NULL, null=True, to_field='id')

    filter = models.ForeignKey(filter, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def f1(self):
        return mark_safe('<img src="{}" width="10%">'.format(self.image.url))

    f1.allow_tags = True


class salesorder(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(null=True)
    iscancel = models.BooleanField()
    totalamount = models.IntegerField()
    customer_name = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    payment_status = models.BooleanField(default=False)
    paymentmode = models.CharField(max_length=40, null=False, choices=payment_list)


class salesorder_detail(models.Model):
    salesorder_name = models.ForeignKey(salesorder, on_delete=models.SET_NULL, null=True)
    product_name = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(validators=[MaxValueValidator(10)])


class supplier(models.Model):
    name = models.CharField(max_length=40)
    address = models.TextField(null=False)
    contact = models.DecimalField(max_digits=10, unique=True, decimal_places=0)
    email = models.EmailField(unique=True)
    company_name = models.ForeignKey(company, on_delete=models.SET_NULL, null=True)
    prodct_name = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    area_name = models.ForeignKey(area, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name


class rentmachinery(models.Model):
    product_id = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    supplier_id = models.ForeignKey(supplier, on_delete=models.SET_NULL, null=True)
    customer_id = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    time_duration = models.CharField( max_length=30, null=False)
    rent_amount = models.IntegerField(null=False, validators=[MaxValueValidator(limit_value=10000)])
    deposit = models.IntegerField(null=True, blank=True)
    booked_date=models.DateField(null=True)
    payment_type=models.CharField(default="Cash On Delivery",max_length=20)

    # def save(self, *args, **kwargs):
    #     # Calculate deposit as 20% of rent amount
    #     self.deposit = int(0.2 * self.rent_amount)
    #
    #     super().save(*args, **kwargs)


class cart(models.Model):
    product_name = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    customer_name = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True)
    totalprice = models.IntegerField(null=True)
    product_status = models.IntegerField(null=True)
    orderid = models.IntegerField(null=True)


class payment(models.Model):
    date = models.DateField(auto_now_add=True)
    customer_name = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    saleorder_name = models.ForeignKey(salesorder_detail, on_delete=models.SET_NULL, null=True)
    payment_type = models.BooleanField(choices=payment_list)
    total_amount = models.IntegerField()


class feedback1(models.Model):
    rating = models.IntegerField()
    customer_name = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    product_name = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    saleorder_name = models.ForeignKey(salesorder_detail, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class report1(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    company_name = models.ForeignKey(company, on_delete=models.SET_NULL, null=True)


class Order_Status(models.Model):
    date_time=models.DateTimeField(auto_now=True)
    status=models.CharField(choices=order_status,max_length=30)
    salesorder_id = models.ForeignKey(salesorder, on_delete=models.SET_NULL,  null=True)