from django.urls import path
from .views import RegisterView,LoginView,PasswordResetView,PasswordResetConfirmView,forgot_password
from rest_framework_nested import routers
from .import views





urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("resetpassword/", PasswordResetView.as_view(), name="resetpassword"),
    path("confirmpassword/", PasswordResetConfirmView.as_view(), name="resetpassword"),
    path('forgot_password/', forgot_password, name="forgot_password"),
    
]



router = routers.DefaultRouter()
router.register("details", views.RegisterDetailView)



urlpatterns = urlpatterns + router.urls