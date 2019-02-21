from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    email2 = serializers.EmailField(label="Confirm you're email")
    email = serializers.EmailField(label="Email address")
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
        }

    def validate_email2(self, value):# value being actual value passed to email
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError("Emails must match")
        return value

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError("This email has already been used to create a user")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    token = serializers.CharField(allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
        }

    def validate(self, data):
        user_obj = None
        username = data.get("username")
        password = data.get("password")
        if not username:
            raise serializers.ValidationError("A username is required")
        user = User.objects.filter(
            Q(username=username) #using Q lookups
        ).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("incorrect credentials please try again")
        # data["token"] = "some random token"
            payload = jwt_payload_handler(user_obj)
            print(user_obj)
            token = jwt_encode_handler(payload)
            response = jwt_response_payload_handler(token)
            data["token"] = token
        return data