from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
  # return HttpResponse("<h1>Hello Django!</h1>")
  return render(request, 'pages/home.html', context={}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
  serializer = TweetSerializer(data=request.POST)
  if serializer.is_valid(raise_exception=True):
    serializer.save(user=request.user)
    return Response(serializer.data, status=201)
  return Response({}, status=400)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
  tweets = Tweet.objects.all()
  serializer = TweetSerializer(tweets, many=True)
  return Response(serializer.data, status=200)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):  
  tweet = Tweet.objects.filter(id=tweet_id)
  if not tweet.exists():
    return Response({}, status=404)
  obj = tweet.first()
  serializer = TweetSerializer(obj)
  return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
  tweet = Tweet.objects.filter(id=tweet_id)
  if not tweet.exists():
    return Response({}, status=404)
  tweet = tweet.filter(user=request.user)
  if not tweet.exists():
    return Response({'message': 'Unauthorized'}, status=401)
  obj = tweet.first()
  obj.delete()
  return Response({'message': 'Tweet deleted successfully'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
  # like, unline, retweet actions
  serializer = TweetActionSerializer(data=request.POST)
  if serializer.is_valid(raise_exception=True):
    data = serializer.validated_data
    tweet_id = data.get('id')
    action = data.get('action')

    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
      return Response({}, status=404)
    obj = qs.first()
    if action == 'like':
      obj.likes.add(request.user)
    elif action == 'unlike':
      obj.likes.remove(request.user)
    elif action == 'retweet':
      pass

  return Response({}, status=201)


# Implementation using Pure Django - Not usable

def tweet_create_view_django(request, *args, **kwargs):
  user = request.user
  if not request.user.is_authenticated:
    user = None
    if request.is_ajax():
      return JsonResponse({}, status=401)
    return redirect(settings.LOGIN_URL)

  form = TweetForm(request.POST or None)
  next_url = request.POST.get('next') or None

  if form.is_valid():
    obj = form.save(commit=False)
    obj.user = user
    obj.save()
    if request.is_ajax():
      return JsonResponse(obj.serialize(), status=201)
    if(next_url != None and is_safe_url(next_url, ALLOWED_HOSTS)):
      return redirect(next_url)
    form = TweetForm()

  if form.errors:
    if request.is_ajax():
      return JsonResponse(form.errors, status=400)

  return render(request, 'components/form.html', context={"form": form})


def tweet_list_view_django(request, *args, **kwargs):
  tweets = Tweet.objects.all()
  tweets_list = [x.serialize() for x in tweets]
  data = {
    "response": tweets_list
  }
  return JsonResponse(data)

def tweet_detail_view_django(request, tweet_id, *args, **kwargs):  
  data = {
    "id": tweet_id
  }
  status = 200
  try:
    obj = Tweet.objects.get(id=tweet_id)
    data['content'] = obj.content
  except:
    data['message'] = "Tweet not found."
    status = 404
  return JsonResponse(data, status=status)
