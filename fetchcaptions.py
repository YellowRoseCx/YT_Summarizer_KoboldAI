import requests, json, os, re
from youtube_transcript_api import YouTubeTranscriptApi

ENDPOINT = ("http://127.0.0.1:5000")
def split_text(text):
    parts = re.split(r'\n\s+', text)
    return parts

def get_prompt(transcript_text):
    return {
        "prompt": f"{transcript_text}\n\nHere's a Summary of the above text: ",
        "max_context_length": 2048,
        "max_length": 512,
        "rep_pen": 1.0,
        "rep_pen_range": 2048,
        "rep_pen_slope": 0.7,
        "temperature": 0.8,
        "tfs": 0.97,
        "top_a": 0.8,
        "top_k": 0,
        "top_p": 0.5,
        "typical": 0.19,
        "sampler_order": [5, 4, 3, 1, 2, 0, 6],
        "singleline": False, 
        "frmttriminc": False,
        "frmtrmblln": False
    }

os.system(f"clear")

def get_video_id(url):
    return url.split('=')[1]
while True:
    video_url = input("Enter the YouTube video URL: ")
    video_id = get_video_id(video_url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript_text = ''
    for transcript in transcript_list:
        translated_transcript = transcript.translate('en').fetch()
    for line in translated_transcript:
        transcript_text += line['text'] + ' '
    prompt = get_prompt(transcript_text)
    response = requests.post(f"{ENDPOINT}/api/v1/generate", json=prompt)
    if response.status_code == 200:
        results = response.json()['results']
        text = results[0]['text']
        response_text = split_text(text)
    clean_text = " ".join([part.strip() for part in response_text])
    print("Summary: \n" + clean_text + "\n")
