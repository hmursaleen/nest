from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    is_reply = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'parent', 'is_reply', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author', 'post']

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value
