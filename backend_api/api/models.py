from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    isDoctor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'isDoctor']


    def profile(self):
        profile = Profile.objects.get(user=self)

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    verified = models.BooleanField(default=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


# for pdf upload
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='report_gallery/')
    created_at = models.DateTimeField(default=timezone.now)
    isModified = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, related_name='shared_reports')

    def share_with_doctor(self, doctor): # Method to share the report with a doctor.
        
        self.shared_with.add(doctor)