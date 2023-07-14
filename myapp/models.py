from django.db import models


class Issue(models.Model):
    STATUS_CHOICES = [
        ('INQUEUE', 'In Queue'),
        ('ASSIGNED', 'Assigned'),
        ('DISPATCHED', 'Dispatched'),
        ('RESOLVED', 'Resolved'),
    ]

    issueID = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    location = models.CharField(max_length=100)
    problem = models.TextField()
    time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    agentId = models.IntegerField(blank=True, null=True)
    mechanicId = models.IntegerField(blank=True, null=True)


class Agents(models.Model):
    agentID = models.AutoField(primary_key=True)
    queue = models.IntegerField(default=0)
    assigned_issues = models.CharField(max_length=1000, default='', blank=True)



class Mechanic(models.Model):
    mechanicID = models.AutoField(primary_key=True)
    availability = models.BooleanField(default=True)
