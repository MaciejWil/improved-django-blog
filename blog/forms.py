from django import forms
from blog.models import Post,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','text', 'image', 'categories')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('text',)

        widgets = {
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }

    # def clean_text(self):
    #     # author = self.cleaned_data.get("author")
    #     # print (forms.ValidationError("Wrong author"))
    #     raise forms.ValidationError("Wrong author")


class ContactForm(forms.Form):
	full_name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email address'
