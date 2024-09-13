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
        #fields: Specifies the fields to be included in the serialized output

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'tags', 'created_at', 'updated_at']
