from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

        fields = ["id", "product", "title", "comment", "rating", "user"]
        read_only_fields = ["product", "user"]
