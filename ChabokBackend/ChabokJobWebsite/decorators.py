from rest_framework.exceptions import PermissionDenied
from .exeptions import AuthenticationFailed

def check_default_role_permission(role, authentication_class=None, message="access denied!"):

    def decorator(func):
        def wrapper_func(*args, **kwargs):
            request = args[1]
            if authentication_class:
                # authenticate user 
                try:
                    user, token = authentication_class().authenticate(request)
                    request.user = user
                except:
                    raise AuthenticationFailed("please login ot your acount!")

            if type(role) == list: 
                role_list = role
                if request.user.get_role() not in [role.name for role in role_list]:
                    raise PermissionDenied(message)
            elif request.user.get_role() != role.name:
                raise PermissionDenied(message)
            return func(*args, **kwargs)
        return wrapper_func

    return decorator