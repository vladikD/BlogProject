from Blog.models import Post, Comment
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        # Кастомна валідація для формату електронної пошти
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Електронна пошта повинна закінчуватися на @gmail.com.')
        return value

    def validate_password(self, value):
        # Кастомна валідація для паролю (наприклад, довжина паролю)
        if len(value) < 8:
            raise serializers.ValidationError('Пароль повинен бути не менше 8 символів.')
        return value

    def validate(self, data):
        # Перевірка, чи користувач з таким ім'ям вже існує
        username = data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Користувач з таким іменем вже існує.')
        return data
    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, value):
        # Кастомна валідація для формату електронної пошти
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Електронна пошта повинна закінчуватися на @gmail.com.')
        return value

    def validate_username(self, value):
        # Кастомна валідація для унікальності імені користувача
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Користувач з таким іменем вже існує.')
        return value


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'publ_date', 'category']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'author_of_the_comment', 'content_of_the_comment', 'date_of_creation']

