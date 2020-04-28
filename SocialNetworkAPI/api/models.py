import datetime

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    pub_date = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together = (('user', 'post'),)
        index_together = (('user', 'post'),)

    def __str__(self):
        return str(self.pub_date) + str(self.post) + str(self.user.username)
