from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.generic import ListView

from item.models import Item

@method_decorator(login_required, name='dispatch')
class indexView(ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        return Item.objects.filter(created_by=self.request.user)