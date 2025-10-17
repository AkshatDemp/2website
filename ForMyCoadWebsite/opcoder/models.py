from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from .utils import generate_fixed_length_slug, generate_category_id, img_preprocessing
 
class Blog(models.Model):
    sno = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = CKEditor5Field(config_name='extends')
    slug = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField()
    likes = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, related_name="blogComment", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.blog.title, self.name)


class Playlist(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    desc = models.TextField()
    thumbnail = models.ImageField(upload_to ='playlistThumbnail/')
    date = models.DateTimeField(auto_now_add=True)
    visi = models.BooleanField(default=True)  # True-visible
    slug = models.CharField(max_length=23, blank=True)

    def __str__(self):
        return "%s - %s" % (self.slug, self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_fixed_length_slug(self.title)

        if self.pk and Playlist.objects.filter(pk=self.pk).exists():  # Check if updating an existing instance
            old = Playlist.objects.get(pk=self.pk)  # old = old_instance
            if old.thumbnail and old.thumbnail != self.thumbnail:
                old.thumbnail.delete(save=False)  # Delete old photo from S3
            else:
                super().save(*args, **kwargs)

        output = img_preprocessing(self.thumbnail)
        self.thumbnail = InMemoryUploadedFile(
            output, 'ImageField', f"{self.thumbnail.name.split('.')[0]}.png",
            'image/png', sys.getsizeof(output), None)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.thumbnail:  # Check if there is an image
            self.thumbnail.delete(save=False)

        super().delete(*args, **kwargs)  # Delete the model instance


class Video(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    playlist = models.ForeignKey(Playlist, related_name="playlist", on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.TextField()
    thumbnail = models.ImageField(upload_to ='videoThumbnail/')
    date = models.DateTimeField(auto_now_add=True)
    visi = models.BooleanField(default=True)  # True-visible
    tviews = models.PositiveIntegerField(default=0)
    tlikes = models.PositiveIntegerField(default=0)
    slug = models.CharField(max_length=23, blank=True)
    source = models.CharField(max_length=200, blank=True)
    categories = models.CharField(max_length=350)
    categoryId = models.PositiveBigIntegerField(blank=True)

    def __str__(self):
        return "%s - %s" % (self.slug, self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_fixed_length_slug(self.title)

        self.categoryId = generate_category_id(self.categories)

        if self.pk and Video.objects.filter(pk=self.pk).exists():  # Check if updating an existing instance
            old = Video.objects.get(pk=self.pk)  # old = old_instance
            if old.thumbnail and old.thumbnail != self.thumbnail:
                old.thumbnail.delete(save=False)  # Delete old photo from S3
            else:
                super().save(*args, **kwargs)

        output = img_preprocessing(self.thumbnail)
        self.thumbnail = InMemoryUploadedFile(
            output, 'ImageField', f"{self.thumbnail.name.split('.')[0]}.png",
            'image/png', sys.getsizeof(output), None)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.thumbnail:  # Check if there is an image
            self.thumbnail.delete(save=False)

        super().delete(*args, **kwargs)  # Delete the model instance


class VideoComment(models.Model):
    video = models.ForeignKey(Video, related_name="videoComment", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.video.title, self.name)


FEEDBACK_CATEGORIES = [
    ('BUG', 'Technical Bug Report'),
    ('FEATURE', 'Feature Request / Suggestion'),
    ('UI', 'UI/UX Improvement'),
    ('CONTENT', 'Content Quality/Correction'),
    ('GENERAL', 'General Inquiry/Praise'),
]

RATING_CHOICES = [
    (1, '1 - Very Dissatisfied'),
    (2, '2 - Dissatisfied'),
    (3, '3 - Neutral'),
    (4, '4 - Satisfied'),
    (5, '5 - Very Satisfied'),
]

class UserFeedback(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=10, choices=FEEDBACK_CATEGORIES,default='GENERAL')
    rating = models.IntegerField(choices=RATING_CHOICES, default=5,
                                 help_text="User's satisfaction rating (1 to 5 stars).")
    date = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes on resolution or triage.")

    class Meta:
        verbose_name_plural = "User Feedback"
        ordering = ['-date']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.subject} by {self.name or self.email or 'Anonymous'}"
