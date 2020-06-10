from django import forms
from .models import Feedback


class CreateNewList(forms.Form):
	name = forms.CharField(label='name',max_length=200)
	check = forms.BooleanField(required=False)

 
 
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['name','email','text']
        #exclude = []

class contactform(forms.Form):
	name = forms.CharField(label='name',max_length=200)
	email = forms.EmailField()
	text = forms.CharField(required=True,widget=forms.Textarea)