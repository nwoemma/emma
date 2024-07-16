from django.urls import path
from users import views 
# from .views import CustomLoginView

app_name = "users"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='loginUser'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',views.logoutUser, name= 'logoutUser'),

   
]