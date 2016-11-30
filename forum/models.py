from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from authentication.models import MyUser


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False)
    author = models.ForeignKey(User)
    publish_time = models.DateTimeField(auto_now_add=True)
    show_times = models.IntegerField(default=0)
    content = UEditorField(imagePath="forum/question/image/", filePath="forum/question/files/")
    category = models.ForeignKey(Category)
    inviting_person = models.ForeignKey(MyUser, null=True, default=None, blank=True)

    class Meta:
        ordering = ['-publish_time']

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(User)
    reply_author = models.ForeignKey(MyUser, null=True, default=None, blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = UEditorField(imagePath="forum/question/image/", filePath="forum/question/files/")
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return self.author + '\'s answer'
