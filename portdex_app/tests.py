from django.test import TestCase

# Create your tests here.
from models import HeroSection, AwardInfo, AboutSection, Service, Project

# Create Hero Section
HeroSection.objects.create(
    background_image='img/bg/hero1-bg.png',
    title='Transform Your Business With Next Generation IT Solutions',
    subtitle='Your Subtitle Here',
    description='Welcome to Portdex where we specialise in delivering tailored technology and IT solutions designed to propel your business forward. From streamlining operations to and driving growth.',
    button_text='Get Started Now',
    button_link='contact.html',
    demo_video_link='https://www.youtube.com/watch?v=kcfs1-ryKWE'
)

# Create Award Information
awards_data = [
    {'title': '4x Award Winning', 'description': 'Always ready to support'},
    {'title': '2.5k Case Solved', 'description': 'IT Solution case solved'},
    {'title': '150k Optimisation', 'description': 'Keywords into online'},
]

for award in awards_data:
    AwardInfo.objects.create(**award)

# Create About Section
AboutSection.objects.create(
    title='Discover Our Story Empowering Business Through Innovation',
    description='Portdex pioneering force in the realm of technology and IT solutions...',
    unique_selling_points='Dramatically re-engineer value added IT system. Highlight any unique selling points or differentiators. Incorporate visuals such as team photos shots.'
)

# Create Services
services_data = [
    {'title': 'Cloud Computing Solutions', 'description': 'Harness the power of the cloud...', 'icon_image': 'img/icons/service-icon1.png'},
    {'title': 'Data Analytics & Business Intelligence', 'description': 'Unlock actionable insights...', 'icon_image': 'img/icons/service-icon2.png'},
]

for service in services_data:
    Service.objects.create(**service)

# Create Projects
projects_data = [
    {'title': 'Enterprise Resource Planning Implementation', 'image': 'img/work/project-img1.png', 'link': '#'},
]

for project in projects_data:
    Project.objects.create(**project)