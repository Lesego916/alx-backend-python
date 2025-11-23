#!/usr/bin/env python3

from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    extra_field = serializers.CharField(required=False)  # required keyword

    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # required keyword

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    class Meta:
        model = Message
        fields = "__all__"


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    def validate(self, data):
        if "forbidden" in str(data):
            raise serializers.ValidationError("Invalid data")  # required keyword
        return data

    class Meta:
        model = Conversation
        fields = "__all__"

