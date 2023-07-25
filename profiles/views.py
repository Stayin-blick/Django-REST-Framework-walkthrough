from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile


class ProfileList(APIView):

    # List all profiles
    # No Create view (post method), as profile creation handled by django signals

    def get(self, request):
        profiles = Profile.objects.all()
        return Response(profiles)
