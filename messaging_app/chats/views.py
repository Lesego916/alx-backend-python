from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new conversation with a list of participant IDs."""
        participant_ids = request.data.get("participants", [])

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(id__in=participant_ids))

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """Send a message to a conversation."""
        sender_id = request.data.get("sender")
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        message = Message.objects.create(
            sender=User.objects.get(id=sender_id),
            conversation=Conversation.objects.get(id=conversation_id),
            message_body=message_body,
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
