from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from .users import User

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=150, verbose_name='نام')
    last_name = models.CharField(max_length=150, verbose_name='نام خانوادگی')
    image = models.ImageField(blank=True, null=True, verbose_name='عکس شخصی')
    discription = models.TextField(max_length=300, blank=True, null=True, verbose_name='توضیحات کاربر')
    email = models.EmailField(blank=True, null=True, max_length=100, unique=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.first_name} - {self.last_name} - {self.email}")
    
    
    
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        