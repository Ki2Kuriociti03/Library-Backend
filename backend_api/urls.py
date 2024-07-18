from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from backend_api import views

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", views.RegisterView.as_view(), name='auth_register'),
    path("test/", views.testEndPoint, name='test'),
    path("favourites/", views.FavouriteListCreateAPIView.as_view(), name='favorites-list-create'),
    path('ratings/', views.RatingListCreateView.as_view(), name='rating-create'),
    path('ratings/<int:pk>/', views.RatingDetailView.as_view(), name='rating-detail'),
    path('ratings/list/', views.RatingListView.as_view(), name='rating-list'),
    path('', views.getRoutes),
]