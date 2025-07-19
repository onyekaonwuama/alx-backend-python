from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 
            'phone_number', 'role', 'created_at', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True},
        }
    
    def create(self, validated_data):
        """
        Create and return a new user instance with encrypted password
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model with sender details
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation', 
            'message_body', 'sent_at'
        ]
        extra_kwargs = {
            'message_id': {'read_only': True},
            'sent_at': {'read_only': True},
        }

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested relationships
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids', 
            'messages', 'created_at'
        ]
        extra_kwargs = {
            'conversation_id': {'read_only': True},
            'created_at': {'read_only': True},
        }
    
    def create(self, validated_data):
        """
        Create a conversation with participants
        """
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        
        return conversation

class ConversationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing conversations
    """
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'created_at', 
            'last_message', 'message_count'
        ]
    
    def get_last_message(self, obj):
        """
        Get the most recent message in the conversation
        """
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return {
                'message_body': last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': f"{last_message.sender.first_name} {last_message.sender.last_name}"
            }
        return None
    
    def get_message_count(self, obj):
        """
        Get the total number of messages in the conversation
        """
        return obj.messages.count()