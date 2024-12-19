from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'destinations', views.DestinationViewSet, basename='destination')

urlpatterns = [
    path('', include(router.urls)),
    path('server/incoming_data/', views.receive_data, name='receive_data'),
]