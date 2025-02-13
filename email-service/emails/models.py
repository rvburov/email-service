from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)

class Mailing(models.Model):
    subject = models.CharField(max_length=200)
    template = models.TextField()
    scheduled_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.mailing.subject, self.subscriber.email)
