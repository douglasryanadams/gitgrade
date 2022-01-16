from django import forms


class RepoForm(forms.Form):
    repo_url = forms.CharField(label="Git repo")
