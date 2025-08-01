from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import Profile

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_profile(sender: UserModel, instance: UserModel, created: bool, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
        )


@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_profile = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    if old_profile.image and old_profile.image != instance.image:
        old_profile.image.delete(save=False)
