import asyncio
import discord
discord.opus._load_default()


class RelayBot(discord.Client):
	def __init__(self, channel, audio):
		super().__init__()
		self.channel = channel
		self.vc = None
		self.audio_in = f'{audio}.wav'
		self.audio_out = f'{channel}.wav'
	async def on_ready(self):
		print(f'Online:  {self.user}')
		self.vc = await self.get_channel(self.channel).connect()
	async def on_message(self, ctx):
		if ctx.content.startswith('.'):
			if ctx.content.startswith('.play'):
				self.play(1.)
			if ctx.content.startswith('.rec'):
				self.rec(3)
			if ctx.content.startswith('.cut'):
				self.cut()
	def play(self, volume):
		self.vc.play(
			discord.PCMVolumeTransformer(
				discord.FFmpegPCMAudio(self.audio_in),
				volume = volume
			)
		)
	def rec(self, duration):
		self.vc.listen(
			discord.TimedFilter(
				discord.WaveSink(self.audio_out),
				duration
			)
		)
	def cut(self):
		self.vc.stop_listening()


# T0, T1 = os.getenv(TOKEN0), os.getenv(TOKEN1)
# C0, C1 = os.getenv(CHANNEL0), os.getenv(CHANNEL1)

B0, B1 = RelayBot(C0, C1), RelayBot(C1, C0)

loop = asyncio.get_event_loop()
loop.create_task(B0.start(T0))
loop.create_task(B1.start(T1))
loop.run_forever()
