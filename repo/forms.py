from django import forms


class RepoForm(forms.Form):
    repo_url = forms.CharField(
        label="Enter the URL of a git repo:",
        initial="https://github.com/douglasryanadams/gitgrade",
    )
