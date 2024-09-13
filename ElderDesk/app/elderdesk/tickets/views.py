from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from organizations.forms import OrganizationForm
from django.contrib.auth.decorators import login_required
from organizations.services import get_all_organizations


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'ticket/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['organizations'] = get_all_organizations() # убери это потом, сделай апи запрос через джгуери
        context['organization_form'] = OrganizationForm()

        user = self.request.user
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['email'] = user.email

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
    
