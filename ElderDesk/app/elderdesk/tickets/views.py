from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from organizations.models import Organization
from organizations.forms import OrganizationForm

from organizations.services import get_all_organizations

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'ticket/dashboard.html'
    login_url = '/accounts/login/'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = get_all_organizations()
        context['organization_form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['name'] = data.get('add_organization_name')
        data['domains'] = data.get('add_organization_domains')

        form = OrganizationForm(data)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
        return self.get(request, *args, **kwargs)
    
