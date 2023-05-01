from django.shortcuts import render
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .serializer import RegistrationSerializer,RegisterDetails,PasswordResetSerializer,PasswordResetConfirmSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from .models import Account
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from .models import password_generater

# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            profile = serializer.save()

            data["email"] = profile.email
            data["username"] = profile.username
            data["pk"] = profile.pk
            data["response"] = "successfully registered new user."
            data["role"] = profile.role

            token = Token.objects.get(user=profile).key
            data["token"] = token

            status_code = status.HTTP_200_OK
            return Response(data, status=status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        


class LoginView(APIView):

    def post(self, request):
        context = {}
        username = request.data.get("username")
        password = request.data.get("password")
        account = authenticate(username=username, password=password)

        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context["response"] = "Successfully authenticated."
            context["pk"] = account.pk
            context["username"] = username.lower()
            context["token"] = token.key
            context["role"] = account.role
            return Response(context, status=status.HTTP_200_OK)
        else:
            context["response"] = "Error"
            context["error_message"] = "The username or password is incorrect"
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login_views(request):
    context = {}
    username = request.data.get("username")
    password = request.data.get("password")
    account = authenticate(username=username, password=password)

    if account:
        try:
            token = Token.objects.get(user=account)
        except Token.DoesNotExist:
            token = Token.objects.create(user=account)
        context["response"] = "Successfully authenticated."
        context["pk"] = account.pk
        context["username"] = username.lower()
        context["token"] = token.key
        # context["role"] = account.role
        return Response(context, status=status.HTTP_200_OK)
    else:
        context["response"] = "Error"
        context["error_message"] = "The username or password is incorrect"
        return Response(context, status=status.HTTP_401_UNAUTHORIZED)

class RegisterDetailView(ModelViewSet):

    queryset=Account.objects.all()
    serializer_class=RegisterDetails
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.role == "admin":
            instance = self.get_object()
            serializer = RegisterDetails(instance)
            return Response(serializer.data)
        elif self.request.user.is_authenticated:
            instance = self.get_object()
            if instance.id == self.request.user.id:
                serializer = RegisterDetails(instance)
                return Response(serializer.data)
            else:
                raise PermissionDenied("You are not allowed to retrieve this object.")
        else:
            raise PermissionDenied("You are not allowed to retrieve objects.")
        

    def list(self, request, *args, **kwargs):
        if self.request.user.role == "admin":
            queryset = self.get_queryset()
            serializer = RegisterDetails(queryset, many=True)
            return Response(serializer.data)
        elif self.request.user.is_authenticated:
            queryset = self.get_queryset().filter(id=self.request.user.id)
            serializer = RegisterDetails(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to list objects.")

 
 
    def update(self, request, *args, **kwargs):
        if self.request.user.role == "admin":
            instance = self.get_object()
            serializer = RegisterDetails(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif self.request.user.is_authenticated:
            instance = self.get_object()
            if instance.id == self.request.user.id:
                serializer = RegisterDetails(instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        else:
            raise PermissionDenied("You are not allowed to update objects.")
        
    def destroy(self, request, *args, **kwargs):
        if self.request.user.role == "admin":
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "successfully deleted."},status=status.HTTP_204_NO_CONTENT)
        elif self.request.user.is_authenticated:
            instance = self.get_object()
            if instance.id == self.request.user.id:
                self.perform_destroy(instance)
                return Response({"message": "successfully deleted."},status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        else:
            raise PermissionDenied("You are not allowed to delete objects.")
        



class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password reset link has been sent to your email.'})

class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password reset successfully.'})
    







# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def register_list(request):
#     if request.user.role == "admin":
#         queryset = Account.objects.all()
#         serializer = RegisterDetails(queryset, many=True)
#         return Response(serializer.data)
#     else:
#         queryset = Account.objects.filter(id=request.user.id)
#         serializer = RegisterDetails(queryset, many=True)
#         return Response(serializer.data)


# @api_view(['POST','GET'])
# @permission_classes((AllowAny, ))
# def forgot_password(request):
#     # Check old password
#     data = {}
#     if Account.objects.filter(email=request.data.get('email')).exists():
#         password = password_generater(8)

#         user = Account.objects.get(email=request.data.get('email'))
#         user.set_password(password)
#         user.save()
#         # from_email = "mail.osperb@gmail.com"
#         to_email = user.email
#         subject = "Password changed Successfully"
#         html_context = {
#             "title":"Password changed Successfully",
#             "data":[
#                 {
#                     "label":"email",
#                     "value":user.email
#                 },
#                 {
#                     "label":"Your New Password",
#                     "value":password
#                 }
#             ]
#         }
#         text_content = str(html_context)
#         send_common_mail(html_context,to_email,subject)
#         data['response'] = "Your new password has been sent to your email"
        
#     else:
#         data['response'] = "Email does not exist"

#     return Response(data, status=status.HTTP_200_OK)
