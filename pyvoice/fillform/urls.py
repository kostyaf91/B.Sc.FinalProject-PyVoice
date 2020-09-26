
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    # path('gen/', views.generate_invoice),

    path('getvalues/', views.getValues, name='getvalues'),
    path('gen/1', views.generate_invoice_dummy,),

    path('gen/', views.generate_invoice, name="geninv" )

]
