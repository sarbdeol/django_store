from django.contrib import admin

# Register your models here.
from .models import HeroSection, AwardInfo, AboutSection, Service, Project
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(HeroSection)
admin.site.register(AwardInfo)
admin.site.register(AboutSection)
admin.site.register(Service)
admin.site.register(Project)