from django.shortcuts import render
from .forms import UserInputForm
import requests
import os
import random
import time

def load_openai_api_key():
	api_key = "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"
	if api_key is None:
		raise EnvironmentError("OpenAI API key not found in .env file")
	return api_key

def get_random_user_message(user_prompt):
	user_messages = [
		f"Write a high-engagement Reddit TIFU (Today I Fucked Up) Post explaining {user_prompt} as the story of a dysfunctional {random.choice(['family', 'office', 'startup'])} dealing with {random.choice(['rogue AI', 'quantum computing', 'autonomous robots'])}. Focus on explaining {user_prompt} in this post through the story. Start your answer with a TL;DR.",
		f"Write a high-engagement Reddit AITA (Am I The Asshole) Post explaining {user_prompt} as the dilemma of 2 friends, one of whom met a bizarre fate involving {random.choice(['time travel', 'nanobots', 'extraterrestrial encounters'])}. Focus on explaining {user_prompt} through the story. Start your answer with a TL;DR.",
		f"Make a high-engagement Meme Tweet explaining {user_prompt} in the context of {random.choice(['AI uprising', 'cybersecurity breach', 'space exploration'])}.",
		f"Write a high-engagement 4Chan Flash Post explaining {user_prompt} disguised as a story of a top-secret government {random.choice(['experiment', 'conspiracy', 'cover-up'])}.",
	]
	random_message = random.choice(user_messages)
	print("Selected User Message:", random_message)
	return random_message

def call_openai_api(api_key, user_message):
	api_url = "https://api.openai.com/v1/chat/completions"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {api_key}"
	}
	request_data = {
		"model": "gpt-3.5-turbo",
		"messages": [{"role": "user", "content": user_message}],
		"temperature": 0.7
	}

	try:
		start_time = time.time()
		response = requests.post(api_url, headers=headers, json=request_data, timeout=1000)
		response.raise_for_status()

		if time.time() - start_time > 10:
			print("It is taking too much time")
	except requests.exceptions.RequestException as e:
		print(f"Request failed with error: {e}")
		return None

	return response

def handle_openai_response(response):
	if response is None:
		return "Error in the API request"

	if response.status_code == 200:
		result = response.json()
		if "choices" in result and result["choices"]:
			user_message = result["choices"][0]["message"]["content"]
			print(user_message)
			return user_message
		else:
			print("Empty response or unexpected response structure.")
			return "Empty response or unexpected response structure."
	else:
		print(f"Request failed with status code: {response.status_code}")
		print(response.text)
		return f"Request failed with status code: {response.status_code}"

from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_config.json'

def generate_audio(transcript):
	print(f"Generating audio for {transcript}")
	try:
		client = texttospeech.TextToSpeechClient()

		voice = texttospeech.VoiceSelectionParams(
			language_code="en-US",
			name="en-US-Studio-M"
		)

		audio_config = texttospeech.AudioConfig(
			audio_encoding=texttospeech.AudioEncoding.LINEAR16,
			pitch=-4,
			speaking_rate=1.15
		)

		synthesis_input = texttospeech.SynthesisInput(text=transcript)

		output_directory = "static/content"
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)

		output_path = os.path.join(output_directory, "speech.mp3")

		if os.path.exists(output_path):
			os.remove(output_path)

		response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

		with open(output_path, "wb") as out_file:
			out_file.write(response.audio_content)
			print(f"Audio content written to '{output_path}' file.")
		
		return output_path.replace("static/", "")
	
	except Exception as e:
		print(f"Audio generation failed: {e}")
		return None

from moviepy.editor import VideoFileClip, AudioFileClip

def generate_video(audio_path):
	try:
		random_number = random.randint(1, 7)
		video_path = VideoFileClip(f"static/videos/{random_number}.mp4")
		audio_clip = AudioFileClip(f"static/{audio_path}")

		final_video = video_path.set_audio(audio_clip)
		final_video.write_videofile("static/output_video.mp4", codec="libx264", audio_codec="aac")

		print("Video generated successfully, saved at static/output_video.mp4")
		return "output_video.mp4"
	except Exception as e:
		print(f"Video generation failed: {e}")
		return None

def core_render(request):
	if request.method == 'POST':
		form = UserInputForm(request.POST)
		if form.is_valid():
			topic = form.cleaned_data['topic']
			prompt_generated = get_random_user_message(topic)
			openai_api_key = load_openai_api_key()
			response = call_openai_api(openai_api_key, prompt_generated)
			transcript = handle_openai_response(response)
			audio = generate_audio(transcript)
			video = generate_video(audio)
			return render(request, 'feed/feed.html', {'topic': topic, 'prompt': prompt_generated, 'response': transcript, 'audio': audio, 'video': video})
	else:
		form = UserInputForm()
	return render(request, 'feed/index.html', {'form': form})

def feed_render(request):
	return render(request, 'feed/feed.html', {'topic': 'undefined', 'prompt': 'undefined', 'response': 'undefined', 'audio': None, 'video': None})
