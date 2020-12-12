from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_LENGTH = settings.MAX_LENGTH_TWEET
TWEET_ACTION_OPTIONS = ['like', 'unlike', 'retweet']

class TweetActionSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  action = serializers.CharField()
  content = serializers.CharField(allow_blank=True, required=False)

  def validate_action(self, value):
    value = value.lower().strip()
    if not value in TWEET_ACTION_OPTIONS:
      raise serializers.ValidationError("This is not a valid action for tweet")
    return value

class TweetCreateSerializer(serializers.ModelSerializer):
  likes = serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model = Tweet
    fields = ['id', 'content', 'likes']

  def get_likes(self, obj):
    return obj.likes.count()

  def validate_content(self, value):
    if len(value) > MAX_LENGTH:
      raise serializers.ValidationError("Tweet is too long.")
    elif len(value) < 1:
      raise serializers.ValidationError("Nothing to tweet.")
    return value

class TweetSerializer(serializers.ModelSerializer):
  likes = serializers.SerializerMethodField(read_only=True)
  parent = TweetCreateSerializer(read_only=True)
  
  class Meta:
    model = Tweet
    fields = ['id', 'content', 'likes', 'is_retweet', 'parent']

  def get_likes(self, obj):
    return obj.likes.count()
