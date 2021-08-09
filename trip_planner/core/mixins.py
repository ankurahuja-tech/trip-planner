from django.contrib.auth.mixins import UserPassesTestMixin


class UserPassesOwnerTestMixin(UserPassesTestMixin):
    def test_func(self, pk_param: str='pk') -> bool:
        """
        Checks if user is the owner of the requested data by verifying with given model's "user" field.
        """
        try:
            return self.request.user == self.owner_mixin_model.objects.get(pk=self.kwargs[pk_param]).user
        except AttributeError:
            return self.request.user == self.model.objects.get(pk=self.kwargs[pk_param]).user
