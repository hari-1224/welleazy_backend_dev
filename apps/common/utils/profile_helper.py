from apps.dependants.models import ProfileSwitch


def get_effective_user(request):
    #Get the effective user and active dependant for the current request.
    user = request.user
    
    if not user.is_authenticated:
        return user, None
    
    active_switch = ProfileSwitch.get_active_switch(user)
    
    if active_switch:
        return user, active_switch.dependant.id
    
    return user, None


def filter_by_effective_user(queryset, request, for_whom_field='for_whom', dependant_field='dependant'):
    #Filter a queryset based on the effective user (main user or switched dependant).
    user, dependant_id = get_effective_user(request)
    
    if dependant_id:
        # User is switched to a dependant's profile
        # Filter for records belonging to that specific dependant only
        filter_kwargs = {
            for_whom_field: 'dependant',
            dependant_field: dependant_id
        }
        return queryset.filter(**filter_kwargs)
    else:
        # User is on their own profile
        # Show ALL data (self + all dependants)
        return queryset


def get_active_profile_info(request):
    #Get information about the current active profile.
    user, dependant_id = get_effective_user(request)
    
    if dependant_id:
        from apps.dependants.models import Dependant
        dependant = Dependant.objects.get(id=dependant_id)
        return {
            'profile_type': 'dependant',
            'user': user,
            'dependant': dependant
        }
    else:
        return {
            'profile_type': 'self',
            'user': user,
            'dependant': None
        }
