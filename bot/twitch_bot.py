from twitchio.ext import commands

class TwitchBot(commands.Bot):
    def __init__(self, irc_token: str, client_id: str, nick: str, prefix: str, initial_channels: List[str]):
        super().__init__(irc_token=irc_token, client_id=client_id, nick=nick, prefix=prefix, initial_channels=initial_channels)

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if message.author.name.lower() == self.nick.lower():
            return
        await self.handle_commands(message)

    @commands.command(name='vote')
    async def vote(self, ctx, *args):
        # Handle voting logic
        pass

    @commands.command(name='redeem')
    async def redeem(self, ctx, *args):
        # Handle redeem logic
        pass
