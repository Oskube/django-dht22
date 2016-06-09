from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^latest$', views.dataview),
    url(r'^from/(\d{1,2})/(\d{1,2})/(\d{4})/to/(\d{1,2})/(\d{1,2})/(\d{4})$', views.selectionview, name='dateselect'),
	url(r'^current', views.currentview),
]
