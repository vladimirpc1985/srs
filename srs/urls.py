from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.welcome_text, name="welcome"),
	url(r'^create_account/', views.create_account, name="create_account"), 
	url(r'^login/', views.login),  
	url(r'^notefile_list', views.notefile_list, name='notefile_list'),
	url(r'^notefile/(?P<name>[-\w]+)/$', views.notefile_detail, name='notefile_detail'),
	url(r'^notecard_list/(?P<name>[-\w]+)/$', views.notecard_list, name='notecard_list'),  
	url(r'^notecard/(?P<pk>\d+)/$', views.notecard_detail, name='notecard_detail'),
	url(r'^create_notefile', views.notefile_new, name='create_notefile'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^about/$', views.about, name='about'), 
	url(r'^srs/$', views.home_directory, name='home_directory'),
	url(r'^srs/create_directory/$', views.create_directory, name='create_directory'),
	url(r'^srs/(?P<name>[-\w]+)/$', views.directory_content, name='directory_content'),
	url(r'^admin/', admin.site.urls, name='login_redirect'),
	url(r"^logout/$", views.logout_view,name="logout"),
	url(r'^srs/(?P<directory>[-\w]+)/(?P<notefile>[-\w]+)/$', views.notefile_details, name='notefile'),
	url(r'^srs/(?P<name>[-\w]+)/$', views.notefile_detail, name='notefile_detai'), 
]