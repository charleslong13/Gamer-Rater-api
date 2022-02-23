from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


from gamerraterapi.models import  Game, Category

class GameTests(APITestCase):
    
    def setUp(self):
        """
        Create a new Gamer, collect the auth Token, and create a sample GameCategory
        """

        # Define the URL path for registering a Gamer
        url = '/register'

        # Define the Gamer properties
        player = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, player, format='json')

        # Store the TOKEN from the response data
        self.token = Token.objects.get(pk=response.data['token'])

        # Use the TOKEN to authenticate the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # SEED THE DATABASE WITH A GAMECATEGORY
        # This is necessary because the API does not
        # expose a /gamecategory URL path for creating GameCategory

        # Create a new instance of GameCategory
        self.category = Category()
        self.category.label = "Board game"

        # Save the GameCategory to the testing database
        self.category.save()
        
        self.game = Game()
        self.game.player_id = 1
        self.game.title = "Sorry"
        self.game.designer = "Milton Bradley"
        self.game.description = "Multiplayer Boardgame"
        self.game.year_released = 1987
        self.game.num_of_players = 1
        self.game.time_to_play = 3
        self.game.age_rec = 6
        
        self.game.save()
        self.game.categories.add(self.category.id)

    def test_create_game(self):
        """
        Ensure we can create (POST) a new Game.
        """

        # Define the URL path for creating a new Game
        url = "/game"

        # Define the Game properties
        game = {
            # "player_id": 1,
            "title": "Monopoly",
            "designer": "Hasbro",
            "description": "Multiplayer boardgame",
            "year_released": 1975,
            "num_of_players": 6,
            "time_to_play": 4,
            "age_rec": 5,
            "categoryId": self.category.id
          
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, game, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        # self.assertEqual(response.data["player"]['user'], self.token.user_id)
        self.assertEqual(response.data["title"], game['title'])
        self.assertEqual(response.data["designer"], game['designer'])
        self.assertEqual(response.data["description"], game['description'])
        self.assertEqual(response.data["year_released"], game['year_released'])
        self.assertEqual(response.data["num_of_players"], game['num_of_players'])
        self.assertEqual(response.data["age_rec"], game['age_rec'])
        self.assertIsNotNone(response.data["categories"])
    
    def test_get_game(self):
        """
        Ensure we can GET an existing game.
        """

        # Create a new instance of Game
      
        # Save the Game to the testing database
        self.game.save()

        # Define the URL path for getting a single Game
        url = f'/game/{self.game.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url, format='json')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        
        self.assertEqual(response.data["title"], self.game.title)
        self.assertEqual(response.data["designer"], self.game.designer)
        self.assertEqual(response.data["description"], self.game.description)
        self.assertEqual(response.data["year_released"], self.game.year_released)
        self.assertEqual(response.data["num_of_players"], self.game.num_of_players)
        self.assertEqual(response.data["time_to_play"], self.game.time_to_play)
        self.assertEqual(response.data["age_rec"], self.game.age_rec)
        self.assertIsNotNone(response.data["categories"])
    
    def test_get_games(self):
        """
        Ensure we can GET all games
        """
        url = f'/game'
        # Initiate GET request and capture the response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1 )
    
    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """

        # Create a new instance of Game
        
        #game.description = "Not Sorry!"

        # Save the Game to the testing database
        self.game.save()

        # Define the URL path for updating an existing Game
        url = f'/game/{self.game.id}'

        # Define NEW Game properties 
        new_game = {
            "title": "Magic The Gathering",
            "designer": "Wizards of the Coast",
            "description": "Multiplayer cardgame",
            "year_released": 1993,
            "num_of_players": 4,
            "time_to_play": 4,
            "age_rec": 10,
            "categoryId": self.category.id
        }
        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["title"], new_game["title"])
        self.assertEqual(response.data["designer"], new_game["designer"])
        self.assertEqual(response.data["description"], new_game["description"])

        self.assertEqual(
            response.data["year_released"], new_game["year_released"])
        self.assertEqual(
            response.data["num_of_players"], new_game["num_of_players"])
        self.assertEqual(
            response.data["time_to_play"], new_game["time_to_play"])
        self.assertEqual(
            response.data["age_rec"], new_game["age_rec"])
        self.assertIsNotNone(response.data["categories"])
    
    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """

        # Create a new instance of Game
      
        #game.description = "It's too late to apologize."

        # Save the Game to the testing database
        self.game.save()

        # Define the URL path for deleting an existing Game
        url = f'/game/{self.game.id}'

        # Initiate DELETE request and capture the response
        response = self.client.delete(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)