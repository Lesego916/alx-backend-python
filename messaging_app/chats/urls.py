#!/usr/bin/env python3

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # required keyword
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()  # required keyword
router.register("conversations", ConversationViewSet, basename="conversations")
router.register("messages", MessageViewSet, basename="messages")

urlpatterns = router.urls

