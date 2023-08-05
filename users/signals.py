from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .helpers import sendOtpEmail
from .models import User, UserProfile

@receiver(post_save, sender=User)
def user_verification_send_otp(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    sendOtpEmail(instance)
    
    

@receiver(post_delete, sender=UserProfile)
def user_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()
