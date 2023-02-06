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
    path('create_employee/', views.create_employee, name='create_employee'),
    path('list_employee/', views.list_employee, name='list_employee'),
    path('retrieve_employee/<int:pk>', views.retrieve_employee, name='retrieve_employee'),
    path('update_employee/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),

]
