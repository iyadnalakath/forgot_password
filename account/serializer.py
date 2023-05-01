from rest_framework import serializers
from .models import Account,PasswordRest
from .function import send_password_reset_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.hashers import make_password







class RegistrationSerializer(serializers.ModelSerializer):

    comfirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email','username','password', 'comfirm_password']
        extra_kwargs = {
                'password': {'write_only': True},
        }    


    def save(self):

        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            
        )
        password = self.validated_data['password']
        comfirm_password = self.validated_data['comfirm_password']
        if password != comfirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account

class RegisterDetails(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=[
            "id",
            "username",
            "email"

        ]



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = Account.objects.get(email=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")
        return value


    def save(self):
        user = Account.objects.get(email=self.validated_data['email'])
        token = PasswordRest.objects.create(account=user).id
        # token = PasswordResetTokenGenerator().make_token(user)
        send_password_reset_email(user.email, token)
        print(token)
        return {'token': token, 'parent_serializer_context': self.context}
        

# class PasswordResetConfirmSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=128)
#     token = serializers.CharField()


#     def save(self):
#         try:
#             user = PasswordRest.objects.get(pk=self.validated_data['token'],is_active=True).account
#             user.password = make_password(self.validated_data['password'])
#             user.save()
#         except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
#             raise serializers.ValidationError("Invalid token.")
        
#         user.save()

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)
    token = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        try:
            user = PasswordRest.objects.get(pk=self.validated_data['token'],is_active=True).account
            user.password = make_password(self.validated_data['password'])
            user.save()
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            raise serializers.ValidationError("Invalid token.")
        
        user.save()











































