import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='guest',
        null=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    # Remove username field and use email as the unique identifier
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Conversation(models.Model):
    """
    Model representing a conversation between multiple users
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        blank=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'conversations'
        indexes = [
            models.Index(fields=['conversation_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        participant_names = ", ".join([
            f"{user.first_name} {user.last_name}" 
            for user in self.participants.all()[:2]
        ])
        if self.participants.count() > 2:
            participant_names += f" and {self.participants.count() - 2} others"
        return f"Conversation: {participant_names}"

class Message(models.Model):
    """
    Model representing a message in a conversation
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        null=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        null=False
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'messages'
        indexes = [
            models.Index(fields=['message_id']),
            models.Index(fields=['sender']),
            models.Index(fields=['conversation']),
            models.Index(fields=['sent_at']),
        ]
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message from {self.sender.first_name}: {self.message_body[:50]}..."