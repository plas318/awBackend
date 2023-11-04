# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Custom user manager
class CustomUserManager(BaseUserManager):
    # Custom user manager to handle email as primary key

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Custom user model with email as primary key
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# Category model
class Category(models.Model):
    # Category model for organizing blog posts
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Tag model
class Tag(models.Model):
    # Tag model for adding searchable keywords to blog posts
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Post model
class Post(models.Model):
    # Post model for storing blog posts
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


# Comment model
class Comment(models.Model):
    # Comment model for storing comments on blog posts
    content = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.email}: {self.content[:20]}...'
