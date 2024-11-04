from django.db import models
from django.conf import settings
from organizations.models import Organization, UserProfile
import uuid

# Create your models here.
class DynamicField(models.Model):
    name = models.CharField(max_length=100)
    values = models.TextField(help_text="Comma-separated values")

    def get_values_list(self):
        return self.values.split(",") if self.values else []

    def __str__(self):
        return f"{self.name}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    initiator = models.EmailField()
    assignee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assigned_tickets')
    subscribers = models.ManyToManyField(UserProfile, related_name='subscribed_tickets', blank=True)
    body = models.TextField()
    ticket_id = models.CharField(max_length=10, unique=True)
    files = models.FileField(upload_to='uploads/tickets/', blank=True, null=True) # add company and username like uploads/tickets/company_name/Agent_name 
    # links?
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        super().save(*args, **kwargs)

    def generate_ticket_id(self):
        company_code = self.initiator[:4].upper()
        existing_count = Ticket.objects.filter(ticket_id__startswith=company_code).count() + 1
        return f"{company_code}{existing_count:04d}"

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'