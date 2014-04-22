
from django.views.generic import ListView

from testlist.models import TestModel


class TestListView(ListView):
    template_name = 'test-list.html'
    model = TestModel
    paginate_by = 10
