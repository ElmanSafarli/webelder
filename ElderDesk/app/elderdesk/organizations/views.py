from django.shortcuts import redirect
from django.views.generic import DetailView
from .models import Organization
from .forms import UserProfileForm
from django.core.paginator import Paginator
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
    page_number = request.GET.get('page', 1) 
    
    if search_query:
        organizations = Organization.objects.filter(Q(name__icontains=search_query))
    else:
        organizations = Organization.objects.all()

    paginator = Paginator(organizations, 16)  
    page_obj = paginator.get_page(page_number)

    data = [
        {
            "name": org.name,
            "domains": org.domains.split(),
            "optional_info": org.optional_info,
            "created_date": org.created_date.strftime('%b. %d, %Y') 
        } for org in page_obj
    ]

    # Return the paginated data
    return JsonResponse({
        "organizations": data,
        "has_previous": page_obj.has_previous(),
        "has_next": page_obj.has_next(),
        "current_page": page_obj.number,
        "num_pages": paginator.num_pages,
        "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None
    })