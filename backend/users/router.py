from rest_framework import routers
from .views import userViewSet, profileViewSet

# app name I created!
app_name="users"
# by default, trailing slash = True
router = routers.DefaultRouter()

# /user/...
router.register('users', userViewSet)
router.register('profiles', profileViewSet)