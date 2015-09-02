from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'carshare.views.index', name='home'),

		url(r'^test/$', 'carshare.views.home', name='home'),
		
    url(r'^user/','carshare.views.list_users', name='user'),
		url(r'^test_view/','carshare.views.test_view', name='test'),
		url(r'^log_in/','carshare.views.log_in', name='login'),
		url(r'^get_msg/','carshare.views.get_msg', name='msg'),
		url(r'^put_msg/','carshare.views.put_msg', name='msg'),
		url(r'^log_off/','carshare.views.log_off', name='login'),
		url(r'^detail/id=(?P<id>\d+)/$','carshare.views.detail', name='detail'),
		url(r'^deleterec/id=(?P<id>\d+)/$','carshare.views.deleterec', name='del'),
		url(r'^updaterec/id=(?P<id>\d+)/$','carshare.views.updaterec', name='update'),
		url(r'^sign_up/', 'carshare.views.sign_up', name='test'),
		url(r'^start_now/', 'carshare.views.start_now', name='start_now'),
		url(r'^showmessageinput/id=(?P<id>\d+)/$', 'carshare.views.showmessageinput', name='show_msg_input'),
		url(r'^start_input', 'carshare.views.start_input', name='start_now'),
		url(r'^searchregion', 'carshare.views.searchregion', name='searchregion'),
		url(r'^query_fromto', 'carshare.views.query_fromto', name='query_fromto'),
    url(r'^admin/', include(admin.site.urls)),
)
