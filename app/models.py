from django.db import models


class Profile(models.Model):
    """Single profile/site config: hero image and about text only (managed in admin)."""
    hero_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    about_text = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Profile (single row)'

    def __str__(self):
        return 'Profile'


class Research(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    link_url = models.URLField(blank=True)  # e.g. Google Scholar or external link
    link_text = models.CharField(max_length=200, default='Read more')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Research'

    def __str__(self):
        return self.title[:80]


class Publication(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    link_url = models.URLField(blank=True)
    link_text = models.CharField(max_length=200, default='Read more')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Publications'

    def __str__(self):
        return self.title[:80]


class Project(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    link_url = models.URLField(blank=True)
    link_text = models.CharField(max_length=200, default='Read more')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title[:80]


class Award(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='awards/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Awards & Achievements'

    def __str__(self):
        return self.title


class CVFile(models.Model):
    """Single active CV file for download."""
    file = models.FileField(upload_to='cv/')
    label = models.CharField(max_length=100, default='Download CV')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'CV File'
        verbose_name_plural = 'CV (use one active)'

    def __str__(self):
        return self.label


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Gallery images'

    def __str__(self):
        return self.title or f'Image {self.id}'
