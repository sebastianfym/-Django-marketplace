from django.contrib.auth.mixins import UserPassesTestMixin


class SellerPermissoinMixin(UserPassesTestMixin):
    def test_func(self):
        if hasattr(self.request.user, 'seller'):
            return True
        return False
