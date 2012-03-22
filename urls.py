from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api
from apps.expenses.api import GroupResource, UserResource, ExpenseResource, PaymentResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(GroupResource())
v1_api.register(ExpenseResource())
v1_api.register(PaymentResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'base.html'}, name="index"),
    (r'^',   include('apps.expenses.urls')),
    (r'^currencies/', include('apps.currencies.urls')),
    (r'^api/', include(v1_api.urls)),
    (r'^accounts/',  include('apps.registration.backends.simple.urls')),
    (r'^accounts/profile/',  include('apps.profiles.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^admin/',     include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT,
            'show_indexes': True}),
    )
