from django.urls import path
from .tokens import MyTokenObtainPairView
from .views import loginUser, registerUser, updateUser, deleteUser, getUsers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', registerUser, name="regiter"),
    path('login', loginUser, name="login"),
    path('update', updateUser, name="update"),
    path('delete', deleteUser, name="delete"),
    path('all', getUsers, name="all"),
]