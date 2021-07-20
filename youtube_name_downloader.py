################## @ Modules ##################
import asyncio
import re
import os
from pytube import YouTube, Playlist
from moviepy.editor import *
###############################################

def println(msg, prefix="[>]"):
	return print(f"{prefix} {msg}")

def inputln(msg, prefix="[>]"):
	return input(f"{prefix} {msg}")

class YoutubeDownloader:
	def __init__(self):
		self.file_path : str = ""
		self.manual : bool = True
		self.link : str = "" 
		self.musicName : str = ""
		self.youtubeLink : bool = True
		self.dType : bool = True

	async def getLink(self):
		isLink = inputln("Enter a Link: ")
		reg = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
		youtubeRegex = re.match(reg, isLink)
		if youtubeRegex:
			self.link = isLink
			println("Download started...")
			self.youtubeLink = True
		else:
			self.youtubeLink = False
		return self.link

	async def getListLink(self):
		isLink = inputln("Enter List Link: ")
		reg = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
		youtubeRegex = re.match(reg, isLink)
		if youtubeRegex:
			self.link = isLink
			self.youtubeLink = True
		else:
			self.youtubeLink = False
		return self.link
	
	async def getPathBool(self):
		isManual = inputln("Select Manual file path or Automatic File path. (M/A): ")
		while(1):
			if isManual is "M":
				self.manual = True
				break
			elif isManual is "A":
				self.manual = False
				break
			isManual = inputln("Is it not listed in the file, or is it where the tool is?? (Manual/Automatic): ")
		return self.manual


	async def getPathFile(self):
		choose = self.manual
		if choose:
			filepath = inputln("Type the Path of the File You Want to Put Ex(C:/Users/pc/): ")
			if filepath.startswith("C:") or filepath.startswith("D:"):
				self.file_path = filepath
			else:	
				while True:
					if filepath.startswith("C:") or filepath.startswith("D:"):
						self.file_path = filepath
						break
					filepath = inputln("Type the Path of the File You Want to Put Ex(C:/Users/pc/): ")
		else:
			self.file_path = os.getcwd()
		return self.file_path

	async def setChooseType(self):
		type = inputln("N = Normal, L = List\n[>] Choose a Type: (N/L): ")
		if type == "N":
			await self.getLink()
			await self.getVideoDownload()
		elif type == "L":
			await self.getListLink()
			await self.getListDownload()



	async def getConvertMp3(self, videoTitle):
		mp3_file = r'{}\{}.mp3'.format(self.file_path, videoTitle)

		mp4_file = r'{}\{}.mp4'.format(self.file_path, videoTitle)

		videoclip = VideoFileClip(mp4_file)
		audioclip = videoclip.audio
		audioclip.write_audiofile(mp3_file)
		println("Converting Mp3 succesful.")
		audioclip.close()
		videoclip.close()

	async def setList(self):
		PL = Playlist(self.link)
		for video in PL.videos:
			try:
				video.streams.first().download(self.file_path)
				println("Music name: " + video.title)
				println("Download is in progress, please wait.")
			except:
				println("Download is finished.")

	async def getListDownload(self):
		if self.youtubeLink:
			await self.setList()
		else:
			while(True):
				if self.youtubeLink:
					await self.setList()
					break
				await self.getListLink()

	async def setVideo(self):
		try:
			youtube = YouTube(self.link).streams.first()
			println("Music name: " + youtube.title)
			youtube.download(self.file_path)
			await self.getConvertMp3(youtube.title)
			println("Download is finished.")
		except:
			pass

	async def getVideoDownload(self):
		if self.youtubeLink:
			await self.setVideo()
		else:
			while(True):
				if self.youtubeLink:
					await self.setVideo()
					break
				await self.getLink()
		
	async def setAll(self, bot = True):
		if bot:
			await self.getPathBool()
			await self.getPathFile()
			await self.setChooseType()
	
		else:
			println("Offline")

if __name__ == "__main__":
	YD = YoutubeDownloader()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(YD.setAll())

	



