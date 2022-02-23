"""View module for handling requests about game types"""
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Game, Player, Category
from django.http import HttpResponseServerError
# data flow: starts as row in the database then it gets converted to a python object 
# then to a dictionary then to json to be passed to the front end 


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
        

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
            year_released = request.data['year_released'],
            num_of_players = request.data['num_of_players'],
            time_to_play = request.data['time_to_play'],
            age_rec = request.data['age_rec'],
            player = player
        )
        game.categories.add(request.data['categoryId'])
        
        try:
            game.save()
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        try:
            game=Game.objects.get(pk=pk)
            game.title = request.data['title']
            game.description = request.data['description']
            game.designer = request.data['designer']
            game.year_released = request.data['year_released']
            game.num_of_players = request.data['num_of_players']
            game.time_to_play = request.data['time_to_play']
            game.age_rec = request.data['age_rec']
            category = Category.objects.get(pk=request.data["categoryId"])
            game.categories.add(category)

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
        depth = 1