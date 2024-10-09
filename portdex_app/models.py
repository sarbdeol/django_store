from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Allow null values
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.JSONField(default=list)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.title



# home page #################
class HeroSection(models.Model):
    background_image = models.ImageField(upload_to='img/bg/')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    button_text = models.CharField(max_length=100)
    button_link = models.URLField()
    demo_video_link = models.URLField()

    def __str__(self):
        return self.title


class AwardInfo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unique_selling_points = models.TextField()

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_image = models.ImageField(upload_to='img/icons/')

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img/work/')
    link = models.URLField()

    def __str__(self):
        return self.title