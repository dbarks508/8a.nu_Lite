from django import forms
from .models import Ascent

# form to fill in the fields related to loggin an ascent
class AscentForm(forms.ModelForm):
    # date picker plug in
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"} 
        )
    )
    
    class Meta:
        model = Ascent
        fields = ["proposedGrade", "type", "date", "comment"]
