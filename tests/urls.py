
from django.conf.urls import patterns, url

from testlist.views import TestListView


urlpatterns = patterns(
    '',
    url(r'^$', TestListView.as_view()),
)
