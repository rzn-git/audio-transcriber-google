import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os

# Function to save the transcribed text to a file in the transcripts folder
def save_transcription_to_file(text, folder="transcripts", filename="transcription.txt"):
    # Create the transcripts folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Define the full file path
    file_path = os.path.join(folder, filename)

    # Save the transcription to the specified text file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

# Function to transcribe audio using Google Speech Recognition API
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)
    
    # Save as a temporary WAV file for processing
    temp_wav = "temp.wav"
    audio.export(temp_wav, format="wav")
    
    transcription = ""
    
    try:
        with sr.AudioFile(temp_wav) as source:
            # Split the audio into smaller segments (e.g., 30 seconds) with overlap
            duration = len(audio)  # Total duration in milliseconds
            segment_length = 30 * 1000  # 30 seconds in milliseconds
            overlap_length = 5 * 1000   # 5 seconds of overlap

            for start_time in range(0, duration, segment_length - overlap_length):
                end_time = min(start_time + segment_length, duration)
                audio_segment = audio[start_time:end_time]
                
                # Export the segment to a temporary WAV file
                segment_temp_wav = "segment_temp.wav"
                audio_segment.export(segment_temp_wav, format="wav")
                
                with sr.AudioFile(segment_temp_wav) as segment_source:
                    audio_data = recognizer.record(segment_source)
                    # Transcribing the audio to text
                    try:
                        text = recognizer.recognize_google(audio_data)
                        transcription += text + " "  # Append the transcription
                    except sr.UnknownValueError:
                        transcription += "[Audio not understood] "
                    except sr.RequestError as e:
                        return f"Could not request results; {e}"

    finally:
        # Clean up temporary files
        if os.path.exists(temp_wav):
            os.remove(temp_wav)  # Delete the original temp file
        if os.path.exists(segment_temp_wav):
            os.remove(segment_temp_wav)  # Delete the segment temp file

    return transcription.strip()  # Return the complete transcription

# Streamlit UI
st.title("Audio Transcription App")
st.write("Upload an audio file to transcribe it into English text.")

# File uploader
audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg"])

if audio_file is not None:
    # Show the audio file name
    st.write(f"Transcribing: {audio_file.name}")
    
    # Button to transcribe
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(audio_file)
            st.success("Transcription Complete!")
            st.write(transcription)
            
            # Save the transcription to a text file in the transcripts folder
            save_transcription_to_file(transcription)
            st.success("Transcription saved to 'transcripts/transcription.txt'.")
