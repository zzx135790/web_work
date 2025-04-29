from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ModuleInstanceViewSet, ProfessorRatingViewSet,
    AverageRatingView, RatingViewSet, RegisterView,
    LoginView, LogoutView
)

router = DefaultRouter()
router.register(r'module-instances', ModuleInstanceViewSet, basename='module-instances')
router.register(r'professors', ProfessorRatingViewSet, basename='professors')
router.register(r'ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('average/', AverageRatingView.as_view(), name='average-rating'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]