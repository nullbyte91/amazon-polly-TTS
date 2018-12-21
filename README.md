# A Simple Text To Speech application using Amazon Polly - Excel to MP3:
## What is Amazon Polly:
Amazon Polly is a cloud service that converts text into lifelike speech. You can use Amazon Polly to develop applications that increase engagement and accessibility.

## How it works:
Amazon Polly converts input text into life-like speech. You call one of the speech synthesis methods,
provide the text you wish to synthesize, select one of the available Text-to-Speech (TTS) voices, and
specify an audio output format. Amazon Polly then synthesizes the provided text into a high-quality
speech audio stream.

• <b>Input text</b> – Provide the text you want to synthesize, and Amazon Polly returns an audio stream. You
can provide the input as plain text or in Speech Synthesis Markup Language (SSML) format. With SSML
you can control various aspects of speech such as pronunciation, volume, pitch, and speech rate. For
more information, see Generating Speech from SSML Documents (p. 30).
 
• <b>ilable voices</b> – Amazon Polly provides a portfolio of multiple languages and a variety of voices,
including a bilingual voice (for both English and Hindi). For most languages you can select from several
different voices, both male and female. You specify the voice ID name when launching the speech
synthesis task, and then the service uses this voice to convert the text to speech. Amazon Polly is
not a translation service—the synthesized speech is in the language of the text. However, numbers
using digits (for example, 53, not fifty-three) are synthesized in the language of the voice. For more
information, see Voices in Amazon Polly.
 
• <b>Output format</b> – Amazon Polly can deliver the synthesized speech in multiple formats. You can select
the audio format that suits your needs. For example, you might request the speech in the MP3 or Ogg
Vorbis format to consume in web and mobile application

## Installing prerequisites for Application:
```bash
cd amazon-polly-TTS
basic_setup.sh
```