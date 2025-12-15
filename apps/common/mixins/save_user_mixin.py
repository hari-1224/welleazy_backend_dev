from apps.common.middleware.current_user import _user

class SaveUserMixin:

    def initial(self, request, *args, **kwargs):
        # Store the DRF-authenticated user in thread-local storage
        _user.value = request.user
        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        # Clear the user reference after the response
        _user.value = None
        return super().finalize_response(request, response, *args, **kwargs)
