from django.contrib.admin import views
from django.urls import path
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('about_us', views.about_us, name="about_us"),
    path('blogs', views.blogs, name="blogs"),
    path('blogs_details', views.blogs_details, name="blogs_details"),
    path('checkout', views.checkout, name="checkout"),
    path('contact', views.contact, name="contact"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('dashoboard_info_edit',views.dashboard_info_edit,name="dashboard_info_edit"),
    path('dashboard_order', views.dashboard_order, name="dashboard_order"),
    path('dashboard_order_invoice', views.dashboard_order_invoice, name="dashboard_order_invoice"),
    path('otp', views.otp, name="otp"),
    path('order_tracking', views.order_tracking, name="order_tracking"),
    path('payment', views.payment, name="payment"),
    path('sign_in', views.sign_in, name="sign_in"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('validate_user', views.validate_user, name="validate_user"),
    path('validate_otp', views.validate_otp, name="validate_otp"),
    path('ifo', views.ifo, name="ifo"),
    path('info', views.info, name="info"),
    path('send_otp', views.send_otp, name="send_otp"),
    path('register', views.register, name="register"),
    path('update/<int:id>', views.update, name="update"),
    path('profile/<int:id>', views.profile, name="profile"),
    path('logout', views.logout, name="logout"),
    path('filterp/<int:id>', views.filterp, name="filterp"),
    path('destroycart/<int:id>', views.destroycart, name="destroycart"),
    path('category=<str:name>/', views.subcategory, name="subcategory"),
    path('category=<str:cat>/product=<str:name>/', views.product_details, name="product_details"),
    path('cart_view', views.cart_page, name="cart_view"),
    path('add_cart/<int:id>/<int:qty>/', views.add_cart, name='add_cart'),
    path('destroycart/<int:id>',views.destroy_cart,name="destroycart"),
    path('removeItem/<int:id>',views.removeItem_cart,name="destroycart"),
    path('destroy_cart',views.destroy_cart,name="destroy_cart"),
    path('search', views.search, name="search"),
    path('placeorder',views.placeorder,name="placeorder"),
    path('thanku',views.thanku,name="thanku"),
    path('orderhistory',views.orderhistory,name="orderhistory"),
    path('orderdetails/<int:id>',views.orderdetails,name="orderdetails"),
    path('order_details',views.order_details,name="order_details"),
    path('feedback/<int:id>/<int:id2>',views.feedback,name="feedback"),
    path("feedback",views.feedback,name="feedback"),
    path('send_feed/<int:id>/<int:id2>',views.send_feed,name="send_feed"),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('booking_page',views.booking_page,name="booking_page"),
    path('book_machinery',views.book_machinery,name="book_machinery"),
    path('bookmachinery',views.bookmachinery,name="bookmachinery"),
    path('delete_order/<int:id>',views.delete_order,name="deleteorder"),



]
