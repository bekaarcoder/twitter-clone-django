from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_LENGTH = settings.MAX_LENGTH_TWEET

class TweetSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Tweet
    fields = ['content']

  def validate_content(self, value):
    if len(value) > MAX_LENGTH:
      raise serializers.ValidationError("Tweet is too long.")
    elif len(value) < 1:
      raise serializers.ValidationError("Nothing to tweet.")
    return value