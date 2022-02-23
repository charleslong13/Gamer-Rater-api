from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from gamerraterapi.models import GameReviews, Game, Player

class GameReviewView(ViewSet):

    def list(self, request):
        player = Player.objects.get(pk=request.auth.user.id)
        reviews=GameReviews.objects.all()
        for review in reviews:
            review.author = review.player == player


        serializer=ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            player = Player.objects.get(pk=request.auth.user.id)
            review=GameReviews.objects.get(pk=pk)
            review.author = review.player == player
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except GameReviews.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        game = Game.objects.get(pk=request.data["gameId"])
        player = Player.objects.get(user=request.auth.user)
        review=GameReviews.objects.create(
            game = game,
            player = player,
            review = request.data['review'],
           
        )
        
        try:
            review.save()
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        review = GameReviews.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ReviewSerializer(serializers.ModelSerializer):
    
    author = serializers.IntegerField(default=None)

    class Meta:
        model = GameReviews
        fields = ('id', 'game', 'player', 'review', 'author')
        depth = 2