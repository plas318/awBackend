from rest_framework import serializers
from .models import CustomUser, Category, Tag, Post, Comment
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_staff')
        def update(self, instance, validated_data):
            password = validated_data.pop('password', None)
            if password is not None:
                instance.set_password(password)
            else:
                raise serializers.ValidationError('Password is Empty', code='InvalidPassword')
            return super().update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        verbose_name_plural = 'Categories'
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'pub_date', 'author', 'category', 'tags')


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'content', 'pub_date', 'author', 'post')
        
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('password', 'password2', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('error')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if user is None:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User is not active.')
        else:
            raise serializers.ValidationError('Must include email and password.')

        data['user'] = user
        return data