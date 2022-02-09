"""View module for handling requests about game types"""
from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Game, Player


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)
    

    def create(self, request):
        # player = Player.objects.get(user=request.auth.user)
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.create(
            title = request.data['title'],
            description = request.data['description'],
            designer = request.data['designer'],
            year_released = request.data['yearReleased'],
            num_of_players = request.data['numOfPlayers'],
            time_to_play = request.data['timeToPlay'],
            age_rec = request.data['ageRec'],
            player = player
        )
        game.categories.set(request.data['categories'])
        
        serializer = GameSerializer(game)
        return Response (serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        try:
            game=Game.objects.get(pk=pk)
            game.title = request.data['title']
            game.description = request.data['description']
            game.designer = request.data['designer']
            game.year_released = request.data['yearReleased']
            game.num_of_players = request.data['numOfPlayers']
            game.time_to_play = request.data['timeToPlay']
            game.age_rec = request.data['ageRec']

            game.categories.set(request.data['categories'])

            game.save()
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = "__all__"
        depth = 2