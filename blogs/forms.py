# blogs/forms.py
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content', 'tags', 'status', 'published_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def clean_slug(self):
        #Adding a clean_slug method to check for unique slugs is a good practice to avoid duplicates
        slug = self.cleaned_data.get('slug')
        if BlogPost.objects.filter(slug=slug).exists():
            raise forms.ValidationError("A post with this slug already exists.")
        return slug










class BlogPostUpdateForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content', 'tags', 'status', 'published_at']
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_slug(self):
        """
        Ensure the slug is unique and valid.
        """
        slug = self.cleaned_data['slug']
        if BlogPost.objects.exclude(pk=self.instance.pk).filter(slug=slug).exists():
            raise forms.ValidationError("A post with this slug already exists.")
        return slug
