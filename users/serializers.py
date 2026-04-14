from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for displaying user info (e.g. nested in posts)."""

    class Meta:
        model = User
        fields = ("id", "name", "email", "date_joined")
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles user registration.
    - Password is write-only and hashed via create_user().
    - Email uniqueness is enforced at the model level.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")

    def create(self, validated_data):
        # Delegates to UserManager.create_user which hashes the password
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Validates login credentials. Token generation happens in the view."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
