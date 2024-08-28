from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']  # Include 'parent' for replies
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
            'parent': forms.HiddenInput(),  # Hide the parent field in the form
        }

    def __init__(self, *args, **kwargs):
        # Allow passing the parent comment in the form instance
        self.parent_instance = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)
        if self.parent_instance:
            self.fields['parent'].initial = self.parent_instance

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("The comment cannot be empty.")
        return content