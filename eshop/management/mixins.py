from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

class AdminRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    login_url = reverse_lazy('login')  # Use reverse_lazy to refer to the named URL pattern
    
    def test_func(self):
        # Check if the user is authenticated and has either staff status or specific permissions
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.has_perm('app_label.permission_codename'))

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You do not have permission to view this page.')
            return redirect('home')  # Redirect to home or another appropriate page
        else:
            return super().handle_no_permission()
