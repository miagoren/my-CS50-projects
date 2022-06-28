from django import forms

class NewOpportunityForm(forms.Form):
    """create a new opportunity"""
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control form-control-lg'}), max_length=64)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'rows': '5', 'class': 'form-control'}), max_length=1000)
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Location', 'class': 'form-control'}), max_length=64)
    categories = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Categories, separated by commas', 'rows': '2', 'class': 'form-control'}), max_length=1000)

class NewConversationForm(forms.Form):
    """start a new conversation"""
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}), max_length=64)
    users = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Users, separated by commas', 'class': 'form-control'}), max_length=64)

class ResolveOpportunityForm(forms.Form):
    """resolve an opportunity"""
    resolvers = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'The users that helped you, separated by commas', 'rows': '2', 'class': 'form-control'}), max_length=1000, required=False)
    summary = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Summary of this opportunity', 'rows': '5', 'class': 'form-control'}), max_length=1000)
