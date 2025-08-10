from .models import Instructor, Learner

def user_roles(request):
    user = getattr(request, 'user', None)
    roles = {
        'is_guest': True,
        'is_admin': False,
        'is_instructor': False,
        'is_learner': False,
        'role': 'guest',
    }
    if user and user.is_authenticated:
        roles['is_guest'] = False
        roles['is_admin'] = bool(getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False))
        roles['is_instructor'] = Instructor.objects.filter(user=user).exists()
        db_learner = Learner.objects.filter(user=user).exists()
        roles['is_learner'] = db_learner or (not roles['is_admin'] and not roles['is_instructor'])
        if roles['is_admin']:
            roles['role'] = 'admin'
        elif roles['is_instructor']:
            roles['role'] = 'instructor'
        elif roles['is_learner']:
            roles['role'] = 'learner'
        else:
            roles['role'] = 'user'
    return roles
