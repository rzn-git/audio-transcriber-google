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
    
    try:
        # Recognize speech using Google Speech Recognition
        with sr.AudioFile(temp_wav) as source:
            audio_data = recognizer.record(source)
            # Transcribing the audio to text
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Audio not understood"
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_wav):
            os.remove(temp_wav)  # Delete the temporary file

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
