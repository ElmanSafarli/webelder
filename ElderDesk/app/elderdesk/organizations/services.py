from organizations.models import Organization

def get_all_organizations():
    return Organization.objects.all()