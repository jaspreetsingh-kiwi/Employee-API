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
    path('add_employee/', views.add_employee, name='add_employee'),
    path('show_employee/', views.show_employee, name='show_employee'),

]
