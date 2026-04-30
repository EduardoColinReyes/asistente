from gtts import gTTS
import pygame
import os

# Inicializar el mezclador de audio de pygame
pygame.mixer.init()

def hablar(texto):
    # Crear el audio con Google en español ('es')
    tts = gTTS(text=texto, lang='es')
    
    # Guardar el audio temporalmente
    archivo_audio = "respuesta_temporal.mp3"
    tts.save(archivo_audio)
    
    # Reproducir el audio
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()
    
    # Esperar a que termine de hablar
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    # Limpiar liberando el archivo y borrándolo
    pygame.mixer.music.unload()
    os.remove(archivo_audio)