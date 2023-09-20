from django.db.models.signals import post_save, post_delete
from .models import profile
from django.contrib.auth.models import User



# connect User and Profile Model
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile = profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )
        


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteProfile(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=profile)
post_delete.connect(deleteProfile, sender=profile)
