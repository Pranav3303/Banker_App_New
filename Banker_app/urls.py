from django.urls import path
from .import views

urlpatterns = [
    path('',views.Home,name="Home"),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),
    path('signout',views.signout,name="signout"),
    path('contact1',views.contact1,name="contact1"),
    path('getTouch',views.getInTouch,name="getTouch"),
    path('profile_detail',views.profile_detail,name="profile_detail"),
    path('contactForm',views.contactform,name="contactForm"),
    path('payment',views.payment,name="payment"),
    path('payment/create/<str:plan>/', views.create_payment, name='create_payment'),  # Payment creation
    path('payment/execute/', views.execute_payment, name='execute_payment'),  # Execute payment after approval
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]