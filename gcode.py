import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

MAX_AUDIO_LENGTH_SECS = 8 * 60 * 60


def run_batch_recognize():
  # Instantiates a client.
  client = SpeechClient()

  # The output path of the transcription result.
  gcs_output_folder = "gs://audio-transcriber-bucket/transcripts"

  # The name of the audio file to transcribe:
  audio_gcs_uri = "gs://audio-transcriber-bucket/audio-files/Africa Wont Rise By Prayer And Fasting  Prof Lumumba.mp3"

  config = cloud_speech.RecognitionConfig(
      auto_decoding_config={},
      features=cloud_speech.RecognitionFeatures(
          enable_word_time_offsets=true,
          enable_spoken_punctuation=true,
        ),
      model="chirp",
      language_codes=["en-NG"],
  )

  output_config = cloud_speech.RecognitionOutputConfig(
      gcs_output_config=cloud_speech.GcsOutputConfig(uri=gcs_output_folder),
  )

  files = [cloud_speech.BatchRecognizeFileMetadata(uri=audio_gcs_uri)]

  request = cloud_speech.BatchRecognizeRequest(
      recognizer="projects/audio-transcriber-439012/locations/global/recognizers/_",
      config=config,
      files=files,
      recognition_output_config=output_config,
  )
  operation = client.batch_recognize(request=request)

  print("Waiting for operation to complete...")
  response = operation.result(timeout=3 * MAX_AUDIO_LENGTH_SECS)
  print(response)