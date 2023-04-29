from django.urls import path
from .views import RegisterView,LoginView,PasswordResetView,PasswordResetConfirmView,forgot_password,login_views
from rest_framework_nested import routers
from .import views





urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("loginfunction/", login_views, name="loginfunction"),
    path("register/", RegisterView.as_view(), name="register"),
    path("resetpassword/", PasswordResetView.as_view(), name="resetpassword"),
    path("confirmpassword/", PasswordResetConfirmView.as_view(), name="resetpassword"),
    path('forgot_password/', forgot_password, name="forgot_password"),
    
]



router = routers.DefaultRouter()
router.register("details", views.RegisterDetailView)
# router.register("loginfunction/", views.login_views)



urlpatterns = urlpatterns + router.urls