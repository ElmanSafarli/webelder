from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from organizations.forms import OrganizationForm
from organizations.services import get_all_organizations

from .services import get_microsoft_graph_access_token, read_email

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'ticket/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['organization_form'] = OrganizationForm()

        user = self.request.user
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['email'] = user.email
        
        context['access_token'] = read_email(self.request)

        return context
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['name'] = data.get('add_organization_name')
        data['domains'] = data.get('add_organization_domains')

        form = OrganizationForm(data)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by = request.user
            organization.save()
            return redirect('dashboard')  
        return self.get(request, *args, **kwargs)
    
