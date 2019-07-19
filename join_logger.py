from twitchbot import Mod, Channel


class JoinLogger(Mod):
    name = 'JoinLogger'

    async def on_user_join(self, user: str, channel: Channel):
        print(f'[JOIN][{channel.name}] {user}')

    async def on_user_part(self, user: str, channel: Channel):
        print(f'[PART][{channel.name}] {user}')
