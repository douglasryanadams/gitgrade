# from django.contrib import admin

# Register your models here.
from django.contrib import admin

from repo.models import GitRepoData

admin.site.register(GitRepoData)
