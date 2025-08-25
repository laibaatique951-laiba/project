
from django.db import models
from django.contrib.auth.models import User

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.user.username

class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10, null=True)
    company = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=100)
    salary = models.FloatField()
    image = models.FileField(null=True)
    description = models.CharField(max_length=300)
    experience = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    skills = models.CharField(max_length=100)
    creationdate = models.DateField()

    def __str__(self):
        return self.title


class Apply(models.Model):
   job = models.ForeignKey(Job, on_delete=models.CASCADE)
   student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
   resume = models.FileField(null=True)
   applydate = models.DateField()

   def __str__(self):
        return self.id

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_reply = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=(('Pending', 'Pending'), ('Resolved', 'Resolved')), default='Pending')

    def __str__(self):
        return f"{self.user.username} ({self.rating}★)"

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username