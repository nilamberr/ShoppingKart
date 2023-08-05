from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.home),
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/,<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/,<slug:data>', views.laptop, name='laptopdata'),
    path('top_wear/', views.topWear, name='topWear'),
    path('top_wear/,<slug:data>', views.topWear, name='topWeardata'),
    path('bottom_wear/', views.bottomWear, name='bottomWear'),
    path('bottom_wear/,<slug:data>', views.bottomWear, name='bottomWeardata'),
    path('buy/<int:pk>', views.buy_now, name='buy-now'),
    path('paymentdones/<int:pk>', views.paymentdones, name='paymentdones'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('showCart/', views.showCart, name='showcart'),
    path('pluscart/', views.plusCart, name='pluscart'),
    path('minuscart/', views.minusCart, name='minuscart'),
    path('removecart/<int:id>/', views.removeCart, name='removecart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('ordercancel/<int:id>', views.ordercancel, name='ordercancel'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('deleteaddress/<int:id>', views.delete_address, name='deleteaddress'),
    path('changepassword/', views.user_changepass, name='changepassword'),
    path('passwordchangedone/', views.passwordchangedone, name='passwordchangedone'),
    path('accounts/login/', views.log_in, name='login'),
    path('accounts/logout/', views.log_out, name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('resetpasswordconfirm/', views.resetPasswordConfirm, name='resetpasswordconfirm'),
    path('resetpassworddone/<uidb64>/<token>/', views.resetPasswordDone, name='resetpassworddone'),
    path('resetpasswordcomplete/', views.resetPasswordComplete, name='resetpasswordcomplete'),



    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
