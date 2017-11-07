__author__ = 'sainatha798'
from django import forms
from django.forms import models
from .models import PollQuestion, PollChoice
class Vote(forms.Form):
    choices = forms.ModelChoiceField(queryset=None,widget=forms.RadioSelect,  empty_label=None)

    def __init__(self, vote_id):
        super(Vote, self).__init__()
        self.fields['choices'].queryset = PollQuestion.objects.get(pk=vote_id).pollchoice_set.all()
        self.fields['choices'].label = str(PollQuestion.objects.get(pk=vote_id))

class AddChoice(models.ModelForm):

    class Meta:
        model = PollChoice
        fields = ['poll_choice']