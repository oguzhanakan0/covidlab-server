from rest_framework import serializers
from .models import Notif


class NotifSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notif
        fields = ['date_created', 'title',
                  'content', 'notif_type', 'date_read']
