# blogs/serializers.py
'''
Serializers in DRF work similarly to Django forms. They allow complex data types 
such as querysets and model instances to be converted to native Python datatypes 
that can then be easily rendered into JSON, XML, or other content types.
'''

from rest_framework import serializers
from .models import BlogPost, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='name',
        many=True
    )

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'tags', 'created_at', 'updated_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        blog_post = BlogPost.objects.create(**validated_data)
        for tag in tags_data:
            blog_post.tags.add(tag)
        return blog_post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        # Update tags
        instance.tags.clear()
        for tag in tags_data:
            instance.tags.add(tag)
        return instance
