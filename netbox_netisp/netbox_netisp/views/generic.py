from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.contrib.contenttypes.models import ContentType
from django_tables2 import RequestConfig

class ObjectListView(View):
    queryset = None
    filterset = None
    filterset_form = None
    table = None
    template_name = 'netbox_netisp/generic/object_list.html'
    action_buttons = ('add', 'import', 'export')

    def get(self, request):

        model = self.queryset.model
        content_type = ContentType.objects.get_for_model(model)

        table = self.table(self.queryset, user=request.user)
        paginate = {
            'per_page': 5
        }
        RequestConfig(request, paginate).configure(table)

        context = {
            'content_type': content_type,
            'action_buttons': self.action_buttons,
            'table': table,
            'filter_form': self.filterset_form(request.GET, label_suffix='') if self.filterset_form else None,
        }

        return render(request, self.template_name, context)
