from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender",
                  "text", "timestamp", "is_read"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "name", "is_group",
                  "participants", "created_at", "last_message"]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-timestamp").first()
        return MessageSerializer(last_msg).data if last_msg else None
