from django.db import models
from . import utils
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from .managers import ActiveLinkManager
# Create your models here.
class Link(models.Model):

    ACCESS_CHOICES = (
        ("True", "YES"),
        ("False", "NO")
    )

    target_url = models.URLField(max_length = 200)
    description = models.CharField(max_length = 200)
    identifier = models.SlugField(max_length = 20, unique=True, blank=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="post_links"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(choices=ACCESS_CHOICES,default="True")
    objects = models.Manager()
    public = ActiveLinkManager()

    def __str__(self):
        return f"{self.identifier}"

    def save(self, *args, **kwargs):
        if not self.identifier:
            # Generate a random ID
            random_id = utils.generate_random_id()
            
            # Make sure there is no other Link with that same ID
            while Link.objects.filter(identifier=random_id).exists():
                random_id = utils.generate_random_id()

            self.identifier = random_id
        
        # Complete the save operation   
        super().save(*args, **kwargs)        