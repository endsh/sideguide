from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^activate/(?P<activation_key>\w+)/$', 'registration.views.activate'),
	url(r'^login/$', auth_views.login,
		{'template_name': 'registration/login.html'}),
	url(r'^logout/$', auth_views.logout,
		{'template_name': 'registration/logged_out.html'}),
	url(r'^password/change/$', auth_views.password_change,
		{'template_name': 'registration/password_change_form.html',
		'post_change_redirect': 'done'}),
	url(r'^password/change/done/$', auth_views.password_change_done,
	 	{'template_name': 'registration/password_change_done.html'}),
	url(r'^password/reset/$', auth_views.password_reset,
		{'template_name': 'registration/password_reset.html',
		'from_email': 'staff@openart.com'}),
	url(r'^password/reset/done/$', auth_views.password_reset_done,
		{'template_name': 'registration/password_reset_done.html'}),
	url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
		auth_views.password_reset_confirm,
		{'post_reset_redirect': '/accounts/password/reset/complete/'}),
	url(r'^password/reset/complete/$',TemplateView.as_view(template_name='registration/password_reset_complete.html')),
    url(r'^register/$', 'registration.views.register'),
    url(r'^register/complete/$',TemplateView.as_view(template_name='registration/registration_complete.html')),


    url(r'^profile/$', 'registration.views.profile'),
)
