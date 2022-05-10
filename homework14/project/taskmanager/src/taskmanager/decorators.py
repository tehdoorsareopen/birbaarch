from django.conf import settings
from django.core.exceptions import PermissionDenied


# def test(function):
#     def wrap(request, *args, **kwargs):
#         print(request.user.is_authenticated)
#         if 1:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     return wrap