from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Employee import views

# Creating Router Object
router = DefaultRouter()

""""
 Register EmployeeViewSet with Router
"""
router.register('employee', views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('Home/', views.Details, name='Home')
]
