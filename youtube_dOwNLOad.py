from pytube import YouTube
yt = YouTube('http://youtube.com/watch?v=q4BP3UG2Bus')
stream = yt.streams.first()
name=stream.title
stream.download()
video = open(name+'.mp4', 'rb')
tb.send_video(chat_id, video)
