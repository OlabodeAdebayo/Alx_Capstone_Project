from django.db import models
from users.models import User
from equipment.models import Equipment

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="reservations")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} ({self.start_date} to {self.end_date})"
