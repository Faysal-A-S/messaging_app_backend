from django.urls import path
from .views import GetorCreateConversationView, MessageView, MessageListView


urlpatterns = [
    path("conversations/<int:user_id>/",
         GetorCreateConversationView.as_view(), name="get-or-create-conversation"),
    path("messages/send/<int:user_id>/",
         MessageView.as_view(), name="send-message"),
    path("conversations/<int:conversation_id>/messages/",
         MessageListView.as_view(), name="message-list")
]
