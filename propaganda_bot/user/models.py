from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0)

    def add_points(self, points):
        self.points += points
        self.save()


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    points_required = models.IntegerField()
    description = models.TextField()


class UserAchievement(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserProfile)
def check_for_achievements(sender, instance, **kwargs):
    achievements = Achievement.objects.filter(points_required__lte=instance.points)
    for achievement in achievements:
        UserAchievement.objects.get_or_create(user=instance, achievement=achievement)
