import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

options = {
    "alias": ('pixel', 'пикся', 'пиксель', 'пиксел', 'пикс', 'мистер пи', 'пи',
              'пексель', 'пексиль', 'пиксиль', 'пексел', 'пексил', 'пиксил'),

    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),

    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "meme": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты', 'анекдот')
    }
}


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(options["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in options['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in options['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in options['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        # os.system("D:\\Jarvis\\res\\radio_record.m3u")
        pass

    elif cmd == 'meme':
        # рассказать анекдот
        with open('meme.txt', encoding='utf-8') as file:
            if file.readable():
                meme = str(file.read())
                speak("А я уже рассказывал анекдот про парты? " + meme)
            else:
                speak("факин фак эту табуретку")
            file.close()


    else:
        print('Команда не распознана, повторите!')


recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=1)

with microphone as source:
    recognizer.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

speak("Пиксель на связи!")
stop_listening = recognizer.listen_in_background(microphone, callback)
while True: time.sleep(0.1)
