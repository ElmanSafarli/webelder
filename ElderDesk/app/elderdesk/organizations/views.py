from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Organization, UserProfile
from .forms import OrganizationForm, UserProfileForm

# View to display the list of organizations
class OrganizationListView(ListView):
    model = Organization
    template_name = 'organization/organization_list.html'
    context_object_name = 'organizations'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organization_list')  
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

# View to display the details of a single organization
class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'organization/organization_detail.html'
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        organization = self.get_object()
        form = UserProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            user_type = form.cleaned_data['user_type']
            user_profile, created = organization.add_user(name, email, user_type)
            if created:
                return redirect('organization_detail', pk=organization.pk)
        return self.render_to_response(self.get_context_data(form=form))