from django import forms

from apis.models import School


class SchoolForm(forms.ModelForm):
    '''forms to add schools'''
    
    class Meta:
        model = School
        exclude = ['created_at', 'updated_at']