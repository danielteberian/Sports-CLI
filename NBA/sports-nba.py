# Sports-CLI - NBA Tracker
# 11/11/2024

# Imports:
from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import boxscore, scoreboard
import time


# Main stuff

def live_game_tracking():
	games_status = None # This initializes the games_status variable

	while True:
		score_data = scoreboard.ScoreBoard() # Retrieve current score
		score_data_dict = score_data.get_dict() # Load score data

		t = 10 # Timer is set to 10 seconds
		games = score_data_dict.get('games', []) # Retrieve list of ongoing games

		if not games: # If no games are being played
			if games_status != 'No games are being played.': # If the games_status has not been set
				print("No games are being played. Try again later.") # Tell the user to chill
				games_status = 'No games are being played.' # Set to no games
		else: # If games are being played
			games_status = 'Games are being played.' # Set status accordingly

		for game in games:
			gameid = game['gameId'] # Game ID
			hteam = game['homeTeam']['teamTricode'] # Home team
			ateam = game['awayTeam']['teamTricode'] # Away team. Pity the fool
			hscore = game['homeTeam']['score'] # Score for the home team
			ascore = game['awayTeam']['score'] # Score for the away team
			status = game['status'] # Game status


			# Print the live data
			print(f"{hteam} {hscore} - {ateam} {ascore} ({status})")


			# Play-by-play data
			g_boxscore = boxscore.BoxScore(gameid) # Rerieve the game boxscore
			g_boxscore.load() # Load the game's boxscore
			pbp = g_boxscore.play_by_play # Play-by-play variable


			# Display recent plays
			print("RECENT PLAYS: ")
			for play in pbp[:10]:
				print(play['text'])

			print('\n') # Print a newline, just to make things pretty
			refresh_timer(int(t))

		# Timer to prevent API overload
		def refresh_timer(t):

			while t:
				sec = divmod(t, 60)
				timer = '{:02d}', format(sec)

				print(f"Updating game data in {t} seconds.") # Display countdown until next refresh
				time.sleep(1) # Wait for a second
				t -= 1 # Subtract 1 from the timer


if __name__ == "__main__":
	live_game_tracking()
