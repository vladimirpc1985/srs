from django.conf.urls import url
from django.contrib import admin
from srs import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.welcome_text, name='welcome'),
	url(r'^create_account/', views.create_account, name='create_account'),
	url(r'^login/', views.login),
	url(r'^srs/$', views.selection_view, name='selection_view'),
	url(r'^srs/notefile_list', views.notefile_list, name='notefile_list'),
	url(r'^srs/notefile/(?P<pk>\d+)/$', views.notefile_detail, name='notefile_detail'),
	url(r'^srs/notecard_list/(?P<pk>\d+)/$', views.notecard_list, name='notecard_list'),
	url(r'^srs/import_notecard/(?P<pk>\d+)/$', views.import_notecard, name='import_notecard'),
	url(r'^srs/export_notecard/(?P<pk>\d+)/$', views.export_notecard, name='export_notecard'),
	url(r'^srs/notecard/(?P<pk>\d+)/$', views.notecard_detail, name='notecard_detail'),
	url(r'^srs/create_notefile/(?P<pk>\d+)/$', views.notefile_new, name='create_notefile'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^about/$', views.about, name='about'),
	url(r'^srs/directory_list/$', views.home_directory, name='home_directory'),
	url(r'^srs/create_directory/(?P<pk>\d+)/$', views.create_directory, name='create_directory'),
	url(r'^srs/directory_list/(?P<pk>\d+)/$', views.directory_content, name='directory_content'),
	url(r'^srs/create_notecard/(?P<pk>\d+)/$', views.create_notecard, name='create_notecard'),
	url(r'^srs/create_video/(?P<pk>\d+)/$', views.create_video, name='create_video'),
	url(r'^srs/create_audio/(?P<pk>\d+)/$', views.create_audio, name='create_audio'),
	url(r'^srs/create_document/(?P<pk>\d+)/$', views.create_document, name='create_document'),
	url(r'^srs/create_equation/(?P<pk>\d+)/$', views.create_equation, name='create_equation'),
	url(r'^admin/', admin.site.urls, name='login_redirect'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^srs/video_archive/$', views.video_list, name='video_list'),
	url(r'^srs/audio_archive/$', views.audio_list, name='audio_list'),
    url(r'^srs/document_archive/$', views.document_list, name='document_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
