from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from .models import Profile
from .serializer import ProfileSerializer, UserSerializer
from .permissions import IsUserOwnerOrGetPostOnly, IsProfileOwnerOrReadOnly

# customise Oauth2 response
from django.http import HttpResponse
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
import json


# Custom Login Response
class CustomTokenView(TokenView):
    '''
    Customise the return fields after a successful token-authentication.
    Use email from the response object for admin and user login feature
    '''
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token)
                app_authorized.send(
                    sender=self, request=request,
                    token=token)
                body['member'] = {
                    'id': str(token.user.id), 
                    'username': token.user.username, 
                    'profile_id': token.user.profile.id,
                }
                body = json.dumps(body) 
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response

class profileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsProfileOwnerOrReadOnly,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user').all()
    filterset_fields = ['user_status']

class userViewSet(viewsets.ModelViewSet):
    
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsUserOwnerOrGetPostOnly,]
    serializer_class = UserSerializer
    queryset = User.objects.select_related('profile').all()
    filterset_fields = ['first_name', 'last_name']
