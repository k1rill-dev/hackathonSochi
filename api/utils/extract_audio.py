from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import json
import moviepy.editor as mp


def extract(filename: str):
    clip = mp.VideoFileClip(filename)
    clip.audio.write_audiofile(f"{filename[:-4]}.wav", codec='pcm_s16le')


SetLogLevel(0)

# Устанавливаем Frame Rate
FRAME_RATE = 16000
CHANNELS = 1

model = Model("./vosk-model-ru-0.10")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)

# Используя библиотеку pydub делаем предобработку аудио
mp3 = AudioSegment.from_wav('test.wav')
mp3 = mp3.set_channels(CHANNELS)
mp3 = mp3.set_frame_rate(FRAME_RATE)

# Преобразуем вывод в json
rec.AcceptWaveform(mp3.raw_data)
result = rec.Result()
text = json.loads(result)["text"]

# Записываем результат в файл "data.txt"
# with open('data.txt', 'w') as f:
#     json.dump(cased, f, ensure_ascii=False, indent=4)
print(text)
