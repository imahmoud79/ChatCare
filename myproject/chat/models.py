from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    size = models.PositiveIntegerField()  # Size in bytes
    uploaded_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    file_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-uploaded_at']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

class UserPreference(models.Model):
    MODEL_CHOICES = [
        ('llama-3.1-8b-instant', 'Llama 3.1 8B Instant'),  # Much better rate limits
        ('llama3-8b-8192', 'Llama 3 8B'),  # This is the correct ID according to Groq docs
        ('llama-3.3-70b-versatile', 'Llama 3.3 70B'),  # Keep as an option but not default
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_model = models.CharField(max_length=50, choices=MODEL_CHOICES, default='llama-3.1-8b-instant')
    
    # Model parameters
    temperature = models.FloatField(default=0.6)
    max_tokens = models.IntegerField(default=4096)
    stream = models.BooleanField(default=True)
    
    # Custom system prompt for prompt engineering
    custom_system_prompt = models.TextField(
        blank=True, 
        null=True,
        help_text="Define how the AI assistant should behave. Leave empty to use the default prompt."
    )
    
    use_custom_prompt = models.BooleanField(default=False)
    
    # Resource usage settings
    use_resources = models.BooleanField(default=True)
    
    # Cached values to avoid regenerating on every page load
    cached_site_name = models.CharField(max_length=100, blank=True, null=True)
    site_name_updated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s preferences" 