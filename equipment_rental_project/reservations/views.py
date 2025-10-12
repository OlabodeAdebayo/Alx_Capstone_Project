from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Reservation
from .serializers import ReservationSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a reservation to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

