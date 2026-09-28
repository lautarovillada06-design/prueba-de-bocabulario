import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
import time



#configuraciones 
sample_rate = 44100  # Frecuencia de muestreo
duration = 5  # Duración de la grabación en segundos
score=0
errors = 0
max_errors = 3

#palabras / niveles
words={
    "facil":{
        "gato":"cat",
        "perro":"dog"
    },
    "medio":{
        "colegio":"school",
        "amigo":"friend",
        "ventana":"window"
    }
}
#elige el nivel de dificultad
print("Seleccione el nivel de dificultad:")
print("1. Fácil")
print("2. Medio")

level=input(">>>>")

if level=="1":
    level="facil"
elif level=="2":
    level="medio"
else:
    print("Nivel no válido. Se seleccionará el nivel fácil por defecto.")
    exit()

#preparacion de las palabras
lista_palabras =list(words[level].keys())
random.shuffle(lista_palabras)

recognizer=sr.Recognizer()

#juego
for palabra in lista_palabras:
    print("palabras:",palabra)
    time.sleep(1)
    print("hable ahora")

    # Grabar voz
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()  # Esperar a que la grabación termine 
    # Guardar la grabación en un archivo WAV temporal
    wav.write("output.wav", sample_rate, recording)
    print("procesando...")

    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

            answer = recognizer.recognize_google(
            audio,
            language = "en"
        ).lower()

        print("Dijiste: ", answer)

        # == Evaluar Respuesta ==
        if answer == words[level][palabra]:
            print("¡Correcto!")
            score += 1
        else:
            print("Incorrecto. La respuesta era:", words[level][palabra])
            errors += 1

    except:
        print("Lo sentimos no entendimos lo que dijiste")
        errors += 1

    print("Puntos:", score)
    print("Errores:", errors)

    if errors >= max_errors:
        print("Llegaste a 3 errores. El juego terminó.")
        break

print("Puntuación final:", score)

