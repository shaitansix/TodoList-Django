from django import forms

class TaskForm(forms.Form):
    title = forms.CharField(
        label = 'Title', 
        widget = forms.TextInput(attrs = { 'class': 'input-custom' }), 
        max_length = 250
    )
    description = forms.CharField(
        label = 'Description', 
        widget = forms.Textarea(attrs = { 'class': 'input-custom textarea-custom' })
    )
    important = forms.BooleanField(
        label = 'Important', 
        widget = forms.CheckboxInput(attrs = { 'class': 'input-chkbox' }), 
        required = False
    )