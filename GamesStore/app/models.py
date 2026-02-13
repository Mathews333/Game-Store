   
from django.db import models
from django.contrib.auth.models import User

class gamedetails(models.Model):
    CATEGORY_CHOICE = [
        ('Multipl', 'Multiplayer'),
        ('RPG', 'Action RPG'),
        ('Racing', 'Racing'),
        ('Rogue', 'Rogue'),
        ('Sim', 'Simulator'),
        ('online', 'Online Co-op'),
        ('Horror', 'Horror'),
        ('Indie', 'Indie'),
        ('AAA', 'AAA Titles'),
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE)
    name = models.TextField()
    description = models.TextField()
    game_price = models.IntegerField()

    game_image = models.ImageField(upload_to='game_image/')
    game_logo = models.ImageField(upload_to='games/logos/', null=True, blank=True)

    # 🔹 NEW (optional)
    screenshot1 = models.ImageField(upload_to='games/screenshots/', null=True, blank=True)
    screenshot2 = models.ImageField(upload_to='games/screenshots/', null=True, blank=True)
    screenshot3 = models.ImageField(upload_to='games/screenshots/', null=True, blank=True)
    screenshot4 = models.ImageField(
    upload_to='games/screenshots/',
    null=True,
    blank=True
    )
    
    embedding = models.JSONField(null=True, blank=True)


    trailer = models.FileField(upload_to='games/videos/', null=True, blank=True)
    
    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(gamedetails, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"


    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(gamedetails, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
# ✅ PASTE SIGNAL CODE HERE (BOTTOM)
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(gamedetails, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} owns {self.game.name}"


class Game(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    game_price = models.DecimalField(max_digits=10, decimal_places=2)

    # NEW FIELDS
    rating = models.FloatField(default=0)
    genre = models.CharField(max_length=100, blank=True)
    developer = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(null=True, blank=True)
    players = models.CharField(max_length=100, blank=True)
    storage_required = models.CharField(max_length=100, blank=True)

    # your existing image fields below...
