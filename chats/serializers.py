from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message
User = get_user_model


