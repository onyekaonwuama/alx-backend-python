from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import User, Conversation, Message
from .serializers import (
    UserSerializer, 
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'conversation_id'
    
    def get_queryset(self):
        """
        Filter conversations to only show those the user participates in
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    def create(self, request):
        """
        Create a new conversation
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Add the current user to participants if not already included
            participant_ids = serializer.validated_data.get('participant_ids', [])
            if request.user.user_id not in participant_ids:
                participant_ids.append(request.user.user_id)
                serializer.validated_data['participant_ids'] = participant_ids
            
            conversation = serializer.save()
            response_serializer = ConversationSerializer(conversation)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, conversation_id=None):
        """
        Add a participant to an existing conversation
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response(
                {'message': f'User {user.first_name} {user.last_name} added to conversation'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages with nested routing support
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'message_id'
    
    def get_queryset(self):
        """
        Filter messages based on conversations the user participates in
        Handle nested routing for /conversations/{id}/messages/
        """
        # Check if this is a nested route (conversation messages)
        conversation_pk = self.kwargs.get('conversation_conversation_id')
        
        if conversation_pk:
            # Nested route: /conversations/{id}/messages/
            try:
                conversation = Conversation.objects.get(
                    conversation_id=conversation_pk,
                    participants=self.request.user
                )
                return Message.objects.filter(
                    conversation=conversation
                ).select_related('sender', 'conversation').order_by('sent_at')
            except Conversation.DoesNotExist:
                return Message.objects.none()
        else:
            # Top-level route: /messages/
            user_conversations = Conversation.objects.filter(
                participants=self.request.user
            ).values_list('conversation_id', flat=True)
            
            return Message.objects.filter(
                conversation_id__in=user_conversations
            ).select_related('sender', 'conversation')
    
    def create(self, request, *args, **kwargs):
        """
        Create a new message with proper nested routing support
        """
        # Check if this is a nested route
        conversation_pk = self.kwargs.get('conversation_conversation_id')
        
        if conversation_pk:
            # For nested routes, automatically set the conversation
            try:
                conversation = Conversation.objects.get(
                    conversation_id=conversation_pk,
                    participants=request.user
                )
                # Add conversation to request data
                data = request.data.copy()
                data['conversation'] = conversation.conversation_id
                serializer = self.get_serializer(data=data)
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation not found or you are not a participant'},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if conversation_pk:
                # For nested routes, we already verified the conversation
                message = serializer.save(sender=request.user, conversation=conversation)
            else:
                # For top-level routes, verify conversation access
                conversation_id = serializer.validated_data['conversation'].conversation_id
                try:
                    conversation = Conversation.objects.get(
                        conversation_id=conversation_id,
                        participants=request.user
                    )
                    message = serializer.save(sender=request.user)
                except Conversation.DoesNotExist:
                    return Response(
                        {'error': 'Conversation not found or you are not a participant'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_conversation(self, request):
        """
        Get messages for a specific conversation (for backward compatibility)
        """
        conversation_id = request.query_params.get('conversation_id')
        
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the user is a participant in the conversation
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or you are not a participant'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        messages = Message.objects.filter(
            conversation=conversation
        ).order_by('sent_at')
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)