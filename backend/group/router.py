from rest_framework import routers
from .views import GroupViewSet

app_name = "group"
router = routers.DefaultRouter()

router.register('groups', GroupViewSet)