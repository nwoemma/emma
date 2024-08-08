from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """
    Middleware to redirect unauthenticated users to the login page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure the request object has a user attribute
        if not hasattr(request, "user"):
            return self.get_response(request)

        # List of public paths that don't require authentication
        public_paths = [
            reverse("accounts:loginAccount"),
            reverse("accounts:register"),
            reverse("pages:about"),
            reverse("pages:contact"),
            reverse("pages:services"),
        ]

        # Redirect unauthenticated users away from protected paths
        if not request.user.is_authenticated and not any(
            request.path.startswith(path) for path in public_paths
        ):
            return redirect(reverse("accounts:loginAccount"))

        response = self.get_response(request)
        return response
