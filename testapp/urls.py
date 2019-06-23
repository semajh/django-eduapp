import django
from django.conf.urls import url
from django.urls import include, path

from testapp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_to_system, name='login'),
    url(r'^logout/$', views.LogoutView, name='logout'),
    url(r'^home/$', views.home, name='home'),
    path('home/<int:group_id>/', views.GroupView, name='group'),
    path('home/<int:group_id>/<int:class_id>/', views.ClassView, name='class'),
]
