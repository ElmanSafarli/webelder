from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from organizations.models import Organization
from organizations.forms import OrganizationForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'ticket/dashboard.html'
    login_url = '/accounts/login/'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = Organization.objects.all()
        context['organization_form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Assuming 'dashboard' is the name of your dashboard URL pattern
        return self.get(request, *args, **kwargs)
