from django import forms
from django.forms import models
from .models import Post, Tag, UserPrefernces

class AddPostTag(models.ModelForm):

    class Meta:
        model = Tag
        fields = ['tag']

class AddTag(forms.Form):
    tag = forms.CharField()

class AddTagNo(forms.Form):
    no_of_tags = forms.IntegerField(min_value=1)

class Edit(forms.Form):
    tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,required=False,)

    def __init__(self, user):
        super(Edit, self).__init__()
        q=[]
        for x in UserPrefernces.objects.get(user=user).tags.all():
            p = (x.tag , x.tag)
            q.append(p)
        self.fields['tags'].choices = q
        ##self.fields['tags'].label = str(UserPrefernces.objects.get(user=user))
