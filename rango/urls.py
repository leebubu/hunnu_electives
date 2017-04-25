from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^about/$', views.about, name='about'),

		url(r'^category/(?P<cat_name_slug>[\w\-]+)/$', views.get_category, name='category'),
		url(r'^subject/(?P<subject_name_slug>[\w\-]+)/$', views.subject, name='subject'),
		url(r'^campus/(?P<campus_name_slug>[\w\-]+)/$', views.campus, name='campus'),
		#url(r'^add_category/$', views.add_category, name='add_category'),
		url(r'^subject/(?P<subject_name_slug>[\w\-]+)/add_category/$', views.add_category, name='add_category'),
		
		#url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
		url(r'^like_category/$', views.like_category, name='like_category'),
		
		url(r'^delete_answer/$', views.delete_answer, name='delete_answer'),
		url(r'^category/(?P<cat_name_slug>[\w\-]+)/add_answer/$', views.get_category, name='add_answer'),
		url(r'^category/(?P<cat_name_slug>[\w\-]+)/edit_answer/(?P<answer_id>[\d]+)$', views.edit_answer, name='edit_answer'),
		
		url(r'^answer_up/$', views.answer_up, name='answer_up'),
		url(r'^answer_up_off/$', views.answer_up_off, name='answer_up_off'),
		url(r'^answer_down/$', views.answer_down, name='answer_down'),
		url(r'^answer_down_off/$', views.answer_down_off, name='answer_down_off'),
)