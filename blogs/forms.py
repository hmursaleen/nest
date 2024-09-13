# blogs/forms.py
from django import forms
from .models import BlogPost, Tag
from django_select2.forms import Select2MultipleWidget



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control w-full border border-gray-300 rounded-md shadow-sm',
                'placeholder': 'Enter post title here',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control w-full border border-gray-300 rounded-md shadow-sm',
                'rows': 6,
                'placeholder': 'Write your content here...',
            }),
            'tags': Select2MultipleWidget(attrs={
                'class': 'form-control border border-gray-300 rounded-md shadow-sm',
            }),
        }


    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not tags:
            raise forms.ValidationError("Please select at least one tag.")
        return tags