from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Marker
from .forms import MarkerCreateForm

from trip_planner.trips.models import Trip


# Create your views here.


class MarkerListView(LoginRequiredMixin, TemplateView):

    template_name = 'markers/marker_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        return context


class MarkerCreateView(LoginRequiredMixin, CreateView):
    
    model = Marker
    template_name = 'markers/marker_form.html'
    form_class = MarkerCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.trip = Trip.objects.get(pk=self.kwargs['trip_pk'])
        return super().form_valid(form)
