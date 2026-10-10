import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from deep_translator import MyMemoryTranslator

words_by_level = {
"facil": ["gato", "perro", "manzana", "leche", "sol"],
"medio": ["banano", "escuela", "amigo", "ventana", "amarillo"],
"dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}


print("🎮 JUEGO DE VOCABULARIO")
print("-----------------------")

# Elegir nivel
print("Elige un nivel:")
print("1. Fácil")
print("2. Medio")
print("3. Difícil")

option = input("Escribe el número del nivel: ")

if option == "1":
    level = "facil"
elif option == "2":
    level = "medio"
elif option == "3":
    level = "dificil"
else:
    print("Opción no válida.")
    level = "facil"

print("Nivel seleccionado:", level)

#Puntacion y errores
score = 0
errors = 0

#El juego continurá hasta tener 3 errores
while errors < 3:
    word = random.choice(words_by_level[level])
    print("------")
    print("Traduce esta palabra al ingles: ", word)
    # Grabar voz
    duration = 5
    sample_rate = 44100

    print("🎤 Habla ahora...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    # Guardar grabación
    wav.write("output.wav", sample_rate, recording)

    print("Grabación completa.")
    print("Reconociendo tu respuesta...")

    # Reconocer voz
    recognizer = sr.Recognizer()

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    
    try:
        recognized = recognizer.recognize_google(
            audio,
            language="en-US"
        )
        reconigzed = recognized.lower()
        print("Dijiste: ", recognized)

     # Traducir la palabra al inglés
        translated = MyMemoryTranslator(
            source="spanish",
            target="english"
        ).translate(word)

        # Convertir la traducción a minúsculas
        translated = translated.lower()

        print("Traducción correcta: ", translated)

        # Comparar
        if recognized == translated:

            score = score + 1

            print("🎉 ¡Correcto!")
            print("Puntos:", score)

        else:

            errors = errors + 1

            print("❌ Incorrecto.")
            print("Errores:", errors, "de 3")
            print("Puntos:", score)
    except sr.UnknownValueError:

        errors = errors + 1

        print("❌ No se pudo reconocer el habla.")
        print("Errores:", errors, "de 3")

    except sr.RequestError as e:

        print("Error del servicio:", e)

print()
print("🏁 FIN DEL JUEGO")
print("----------------")
print("Puntuación final:", score)
print("Errores:", errors)

