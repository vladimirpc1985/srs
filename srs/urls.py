from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome_text),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^create_account/', views.create_account), 
	url(r'^login/', views.login),  
	url(r'^notefile_list', views.notefile_list, name='notefile_list'),
	url(r'^notefile/(?P<pk>\d+)/$', views.notefile_detail, name='notefile_detail'),
	url(r'^create_notefile', views.notefile_create, name='create_notefile'),  
]