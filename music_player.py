import re
import requests as r
import streamlit as st
from urllib.parse import quote_plus as encode
from yt_dlp import YoutubeDL

# Base URL for YouTube search
base = "https://www.youtube.com/results?search_query="

# Function to search YouTube for videos
def search_yt(query: str):
    query = encode(query)
    url = base + query
    resp = r.get(url)
    pattern = r'videoId":"([^"]+)","thumbnail":{"thumbnails":\[{"url":"[^"]+","width":\d+,"height":\d+},{"url":"[^"]+","width":\d+,"height":\d+\}\]\},"title":\{"runs":\[{\"text":"([^"]+)'
    result = re.findall(pattern, resp.text)
    data = {f"https://www.youtube.com/watch?v={v[0]}": v[1] for v in result}
    return data

# Function to get downloadable audio URL
def get_audio_url(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        audio_url = info['url']
    return audio_url

# Function to get downloadable video URL
def get_video_url(link):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        video_url = info['url']
    return video_url

# Function to embed audio player
def play_audio(link):
    audio_url = get_audio_url(link)
    st.audio(audio_url)

# App Design with Custom Styling
st.markdown(
    """
    <style>
        .app-container {
            font-family: 'Arial', sans-serif;
            color: white;
            background-color: #121212;  /* Dark Background */
            padding: 20px;
            border-radius: 10px;
        }
        .title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .search-box {
            text-align: center;
            margin-bottom: 20px;
        }
        .player-container {
            background-color: #1f1f1f;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .song-title {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        .song-subtitle {
            font-size: 14px;
            color: #888;
        }
        .highlight-text {
            font-size: 20px;
            color: #FFD700;
            margin-bottom: 10px;
        }
        .loading-text {
            font-size: 18px;
            color: #32CD32;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main App Container
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# Title
st.markdown('<div class="title">Music Player 🎵</div>', unsafe_allow_html=True)

# Initialize session state
if "search_results" not in st.session_state:
    st.session_state["search_results"] = []
if "selected_song_index" not in st.session_state:
    st.session_state["selected_song_index"] = 0

# Search Box
st.markdown('<div class="search-box">', unsafe_allow_html=True)
st.markdown(
    '<div class="highlight-text">video ka name bta :</div>', unsafe_allow_html=True
)
search_query = st.text_input("", key="song_search")
st.markdown('</div>', unsafe_allow_html=True)

# Search and Display Results
if search_query:
    st.markdown(
        '<div class="loading-text">wait kar yrr search ho rha hai.....</div>',
        unsafe_allow_html=True,
    )
    search_results = list(search_yt(search_query).items())[:10]  # Get top 3 results
    st.session_state["search_results"] = search_results

# Display Top 3 Suggestions
if st.session_state["search_results"]:
    search_results = st.session_state["search_results"]
    total_results = len(search_results)

    # Next and Previous Buttons
    col1, col2 = st.columns(2)
    if col1.button("⏮️ Previous"):
        st.session_state["selected_song_index"] = (st.session_state["selected_song_index"] - 1) % total_results
    if col2.button("⏭️ Next"):
        st.session_state["selected_song_index"] = (st.session_state["selected_song_index"] + 1) % total_results

    # Get the currently selected song
    selected_index = st.session_state["selected_song_index"]
    selected_song = search_results[selected_index]
    selected_link, selected_title = selected_song

    # User Choice: Audio or Video
    play_video = st.radio(
        "video play karna hai ya nhi?",
        options=["Yes", "No"],
        index=0,
        horizontal=True,
    ) == "Yes"

    # Display Player UI
    st.markdown('<div class="player-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="song-title">{selected_title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="song-subtitle">Now Playing</div>', unsafe_allow_html=True)

    # Play Selected Song
    if play_video:
        st.video(selected_link)
        video_download_url = get_video_url(selected_link)
        st.markdown(
            f'<a href="{video_download_url}" download="{selected_title}.mp4" style="color:white; text-decoration:none; padding:10px; background-color:#1DB954; border-radius:5px;">Download Video</a>',
            unsafe_allow_html=True,
        )
    else:
        play_audio(selected_link)

    st.markdown('</div>', unsafe_allow_html=True)
else:
    if search_query:
        st.error("No results found. Please try a different search.")

# End of App Container
st.markdown('</div>', unsafe_allow_html=True)
