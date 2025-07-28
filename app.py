import streamlit as st
import pandas as pd
import plotly.express as px
from spotify_utils import get_playlist_tracks, get_audio_features

st.set_page_config(layout="wide")
st.title("🎵 Spotify Playlist Analyzer")

playlist_url = st.text_input("Enter Spotify Playlist URL")

if playlist_url:
    try:
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        track_ids = get_playlist_tracks(playlist_id)

        if not track_ids:
            st.warning("No tracks found in this playlist.")
        else:
            features = get_audio_features(track_ids)
            features = [f for f in features if f]  # Remove None

            df = pd.DataFrame(features)
            numeric_cols = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

            st.subheader("📊 Feature Distribution")
            selected_feature = st.selectbox("Choose a feature to visualize", numeric_cols)

            fig = px.histogram(df, x=selected_feature, nbins=20, title=f"Distribution of {selected_feature.capitalize()}")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📋 Full Audio Features")
            st.dataframe(df[numeric_cols + ['id']])

    except Exception as e:
        st.error(f"Something went wrong: {e}")
