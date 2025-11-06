from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
User = get_user_model()
# Create your views here.


class GetorCreateConversationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        current_user = request.user
        other_user = get_object_or_404(User, id=user_id)
        conversation = Conversation.objects.filter(
            is_group=False).filter(participants=current_user).filter(participants=other_user).first()

        if not conversation:
            conversation = Conversation.objects.create(is_group=False)
            conversation.participants.add(current_user, other_user)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        current_user = request.user
        recipient = get_object_or_404(User, id=user_id)

        conversation = Conversation.objects.filter(is_group=False).filter(
            participants=current_user).filter(participants=recipient).first()
        if not conversation:
            conversation = Conversation.objects.create(is_group=False)
            conversation.participants.add(current_user, recipient)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(
                sender=current_user, conversation=conversation)

            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if request.user not in conversation.participants.all():
            return Response({
                "success": False,
                "message": "conversation not found",
                "error": "conversation not found"
            }, status=status.HTTP_403_FORBIDDEN)

        message = conversation.messages.select_related(
            "sender").order_by("timestamp")

        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
