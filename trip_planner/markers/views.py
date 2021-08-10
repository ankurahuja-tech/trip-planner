from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from trip_planner.core.mixins import UserPassesOwnerTestMixin
from trip_planner.trips.models import Trip

from .forms import MarkerCreateForm, MarkerUpdateForm
from .models import Marker

# Create your views here.


class MarkerListView(LoginRequiredMixin, UserPassesOwnerTestMixin, TemplateView):

    template_name = "markers/marker_list.html"
    owner_mixin_model = Trip  # custom field for UserPassesOwnerTestMixin

    def test_func(self) -> bool:
        """Pass custom pk param to UserPassesOwnerTestMixin."""
        return super().test_func(pk_param="trip_pk")


class MarkerCreateView(LoginRequiredMixin, UserPassesOwnerTestMixin, CreateView):

    model = Marker
    template_name = "markers/marker_form.html"
    form_class = MarkerCreateForm
    owner_mixin_model = Trip  # custom field for UserPassesOwnerTestMixin

    def test_func(self) -> bool:
        """Pass custom pk param to UserPassesOwnerTestMixin."""
        return super().test_func(pk_param="trip_pk")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.trip = Trip.objects.get(pk=self.kwargs["trip_pk"])
        return super().form_valid(form)


class MarkerUpdateView(LoginRequiredMixin, UserPassesOwnerTestMixin, UpdateView):

    model = Marker
    template_name = "markers/marker_update_form.html"
    form_class = MarkerUpdateForm
    owner_mixin_model = Trip  # custom field for UserPassesOwnerTestMixin

    def test_func(self) -> bool:
        """Pass custom pk param to UserPassesOwnerTestMixin."""
        return super().test_func(pk_param="trip_pk")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.trip = Trip.objects.get(pk=self.kwargs["trip_pk"])
        return super().form_valid(form)


class MarkerDeleteView(LoginRequiredMixin, UserPassesOwnerTestMixin, DeleteView):

    model = Marker
    template_name = "markers/marker_delete.html"
    owner_mixin_model = Trip  # custom field for UserPassesOwnerTestMixin

    def test_func(self) -> bool:
        """Pass custom pk param to UserPassesOwnerTestMixin."""
        return super().test_func(pk_param="trip_pk")

    def get_success_url(self) -> str:
        trip_pk = self.kwargs["trip_pk"]
        return reverse_lazy("markers:marker_list", kwargs={"trip_pk": trip_pk})
