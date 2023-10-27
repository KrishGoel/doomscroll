from django.shortcuts import render
from .forms import UserInputForm
import requests
import os
import random
import time

def load_openai_api_key():
	# api_key = os.getenv("OPENAI_API_KEY")
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
		response.raise_for_status()  # Raise an exception for non-2xx response codes

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

def core_render(request):
	if request.method == 'POST':
		form = UserInputForm(request.POST)
		if form.is_valid():
			topic = form.cleaned_data['topic']
			prompt = get_random_user_message(topic)
			openai_api_key = load_openai_api_key()
			response = call_openai_api(openai_api_key, prompt)
			content = handle_openai_response(response)
			return render(request, 'feed/feed.html', {'topic': topic, 'prompt': prompt, 'response': content})
	else:
		form = UserInputForm()
	return render(request, 'feed/index.html', {'form': form})

def feed_render(request):
	return render(request, 'feed/feed.html', {'topic': 'undefined', 'prompt': 'undefined', 'response': 'undefined'})
