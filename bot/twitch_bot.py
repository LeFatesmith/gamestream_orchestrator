from twitchio.ext import commands
import os
import time
import subprocess
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional

class TwitchBot(commands.Bot):
    def __init__(self, irc_token, client_id, nick, prefix, initial_channels):
        super().__init__(irc_token=irc_token, client_id=client_id, nick=nick, prefix=prefix, initial_channels=initial_channels)

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if message.author.name.lower() == self.nick.lower():
            return
        await self.handle_commands(message)

    @commands.command(name='vote')
    async def vote(self, ctx):
        await ctx.send(f"Thanks for your vote!")

class TwitchVotingBot:
    def __init__(self, channel_name: str, oauth_token: str, game_options: List[str], macros: Dict[str, List[str]], voting_time: int = 10, result_display_time: int = 5):
        self.channel_name = channel_name
        self.oauth_token = oauth_token
        self.game_options = game_options
        self.macros = macros
        self.votes = {game: 0 for game in game_options}
        self.voting_time = voting_time
        self.result_display_time = result_display_time
        self.previous_game = None

    def start_voting(self):
        print("Voting started! Type !vote <game> to vote.")
        fig, ax = plt.subplots()
        plt.ion()

        end_time = time.time() + self.voting_time
        while time.time() < end_time:
            vote = input("Enter your vote (calc/notepad/celeste/brawlhalla): ").strip().lower()
            if vote in self.votes:
                self.register_vote(vote)
                print(f"Vote registered for {vote}!")
            self.update_chart(ax)

        plt.ioff()
        selected_game = self.spin_wheel(ax)
        self.cleanup()  # Clean up the previous game, if any
        self.launch_game(selected_game)
        self.execute_macros(selected_game)
        self.previous_game = selected_game  # Store the current game as the previous one for the next round

    def register_vote(self, game: str):
        if game in self.votes:
            self.votes[game] += 1
            return True
        return False

    def update_chart(self, ax):
        ax.clear()
        labels = list(self.votes.keys())
        sizes = list(self.votes.values())

        if sum(sizes) == 0:
            sizes = [1 for _ in sizes]

        colors = plt.cm.Paired(np.arange(len(labels)))
        ax.pie(sizes, labels=labels, colors=colors, startangle=140, autopct='%1.1f%%')
        self.add_indicator(ax)
        plt.draw()
        plt.pause(0.1)

    def add_indicator(self, ax):
        ax.annotate('', xy=(0, 1.1), xytext=(0, 0),
                    arrowprops=dict(facecolor='red', shrink=0.05, width=2))

    def spin_wheel(self, ax):
        total_votes = sum(self.votes.values())
        if total_votes == 0:
            selected_game = random.choice(self.game_options)
            print("No votes cast, selecting randomly.")
        else:
            weighted_choices = [(game, votes) for game, votes in self.votes.items()]
            games, weights = zip(*weighted_choices)

            angles = [0] + list(np.cumsum(weights) / total_votes * 360)
            selected_game = None

            print(f"Spinning to select the game...")
            spin_steps = 20
            current_angle = 0
            for _ in range(spin_steps):
                current_angle += random.uniform(20, 60)
                ax.clear()
                ax.pie(list(self.votes.values()), labels=list(self.votes.keys()), colors=plt.cm.Paired(np.arange(len(self.votes))), startangle=current_angle, autopct='%1.1%%')
                self.add_indicator(ax)
                plt.draw()
                plt.pause(0.1)
            
            final_angle = (current_angle + 140) % 360
            for i, angle in enumerate(angles[:-1]):
                if angle <= final_angle < angles[i + 1]:
                    selected_game = games[i]
                    break

        ax.clear()
        ax.pie(list(self.votes.values()), labels=list(self.votes.keys()), colors=plt.cm.Paired(np.arange(len(self.votes))), startangle=current_angle, autopct='%1.1%%')
        self.add_indicator(ax)
        plt.draw()
        plt.pause(self.result_display_time)

        print(f"Selected game: {selected_game}")
        plt.close()

        return selected_game

    def cleanup(self):
        if self.previous_game:
            print(f"Closing previous game: {self.previous_game}")
            if self.previous_game == "calc":
                subprocess.run("taskkill /f /im Calculator.exe", shell=True)
            elif self.previous_game == "notepad":
                subprocess.run("taskkill /f /im notepad.exe", shell=True)
            elif self.previous_game == "celeste":
                subprocess.run("taskkill /f /im Celeste.exe", shell=True)
            elif self.previous_game == "brawlhalla":
                subprocess.run("taskkill /f /im Brawlhalla.exe", shell=True)

    def launch_game(self, game: str, options: Optional[List[str]] = None):
        if game == "calc":
            command = "calc"
        elif game == "notepad":
            command = "notepad"
        elif game == "celeste":
            command = r'"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Celeste.exe"'
        elif game == "brawlhalla":
            command = r'"C:\Program Files (x86)\Steam\steamapps\common\Brawlhalla\Brawlhalla.exe"'

        if options:
            command += " " + " ".join(options)
        
        os.system(command)
        print(f"Launched game: {game}")
        time.sleep(1)

    def execute_macros(self, game: str):
        if game in self.macros:
            for macro in self.macros[game]:
                os.system(macro)
                time.sleep(0.5)
                print(f"Executed macro: {macro}")

    def main(self):
        self.start_voting()
