from django.shortcuts import redirect
from django.views.generic import DetailView
from .models import Organization
from .forms import UserProfileForm

from django.http import JsonResponse

from organizations.services import get_all_organizations
from django.db.models import Q

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

def get_organizations(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        organizations = Organization.objects.filter(Q(name__icontains=search_query))
    else:
        organizations = Organization.objects.all()
    
    data = [{"name": org.name} for org in organizations]
    return JsonResponse({"organizations": data})