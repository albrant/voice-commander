import speech_recognition
import os
import random
import pyaudio
import wave


sr = speech_recognition.Recognizer()

commands_dict = {
    'commands': {
        'greetings': ['привет', 'приветствую', 'привет друг'],
        'play_music': ['включить музыку', 'музыка', 'потанцуем', 'хочу веселья']
    }
}

def play_music():
    files = os.listdir('music')
    filename = f'music/{random.choice(files)}'
    # os.system(f'xdg-open {random_file}')
    print(f'Танцуем под {filename}')
    # Set chunk size of 1024 samples per data frame
    chunksize = 1024
    # Now open the sound file, name as wavefile
    wavefile = wave.open(filename, 'rb')
    # Create an interface to PortAudio
    portaudio = pyaudio.PyAudio()
    # Open a .Stream object to write the WAV file to play the audio using pyaudio
    # in this code, 'output = True' means that
    # the audio will be played rather than recorded
    streamobject = portaudio.open(
        format=portaudio.get_format_from_width(wavefile.getsampwidth()),
        channels=wavefile.getnchannels(),
        rate=wavefile.getframerate(),
        output=True)
    # Read data in chunksize
    data_audio = wavefile.readframes(chunksize)
    # Play the audio by writing the audio data to the streamobject
    while data_audio != '':
        streamobject.write(data_audio)
        data_audio = wavefile.readframes(chunksize)
    # Close and terminate the streamobject
    streamobject.close()
    portaudio.terminate()

    return f'Танцуем под {filename}'


def listen_command():
    # mic = speech_recognition.Microphone()
    # print(mic.list_microphone_names())

    with speech_recognition.Microphone(device_index=3) as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=0.5)
        print('Слушаю, повелитель!')
        audio = sr.listen(source=mic)
        query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
    return query


def greetings():
    print('И тебе привет, хозяин')


def main():
    sr.pause_threshold = 0.5
    query = listen_command()
    for function, voice in commands_dict['commands'].items():
        if query in voice:
            print(globals()[function]())
    else:
        print('Не знаю такую команду:', query)


if __name__ == '__main__':
    main()
