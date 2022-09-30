"""pinchi_online_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from online_shop import views as online_shop_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^signup/', online_shop_view.customer_signup_form, name="customer_signup_form"),
    url(r'^$', online_shop_view.index, name="index"),
    url(r'^login/', online_shop_view.login_view, name="login_view"),
    url('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^activate/', online_shop_view.activate_account, name='activate_account'),
    url(r'^order_submit/', online_shop_view.order_submit, name='order_submit'),
    url(r'^order_detail/', online_shop_view.order_detail, name='order_detail'),
    url(r'^user_detail/', online_shop_view.user_detail, name='user_detail')
]
