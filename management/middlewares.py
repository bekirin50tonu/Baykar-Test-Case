from functools import wraps

from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware


def isMontageTeam(view_func):
    @wraps(view_func)
    def _wrapped_view(obj, request, *args, **kwargs):
        # Eğer kullanıcı doğrulanmamışsa 401 Unauthorized
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        # eğer kullanıcı superuser ise giriş yapamaması gerekmektedir.
        if request.user.is_superuser:
            return JsonResponse({"error": "Forbidden"}, status=403)

        # Eğer team id'si < 5 ise 403 Forbidden
        if hasattr(request.user, 'team') and request.user.team and request.user.team.has_produce and not request.user.team.has_montage:
            return JsonResponse({"error": "Forbidden"}, status=403)

        # Her şey uygunsa view fonksiyonu çağrılır
        return view_func(obj,request, *args, **kwargs)

    return _wrapped_view


def isProductTeam(view_func):
    @wraps(view_func)
    def _wrapped_view(obj, request, *args, **kwargs):
        # Eğer kullanıcı doğrulanmamışsa 401 Unauthorized
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        # eğer kullanıcı superuser ise giriş yapamaması gerekmektedir.
        if request.user.is_superuser:
            return JsonResponse({"error": "Forbidden"}, status=403)

        # Eğer team id'si = 5 ise 403 Forbidden
        if hasattr(request.user, 'team') and request.user.team and request.user.team.has_montage and not request.user.team.has_produce:
            return JsonResponse({"error": "Forbidden"}, status=403)

        # Her şey uygunsa view fonksiyonu çağrılır
        return view_func(obj,request, *args, **kwargs)

    return _wrapped_view
