import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pygame

class ReadMic:
    def __init__(self, duration=5, sample_rate=44100, device_index=3, output_file="audio_gravado.wav", channels=None):
        """
        Parâmetros:
         - duration: Duração da gravação em segundos.
         - sample_rate: Taxa de amostragem.
         - device_index: Índice do dispositivo padrão.
         - output_file: Nome do arquivo de saída.
         - channels: Número de canais. Se None, será usado 1 canal por padrão.
        """
        self.duration = duration
        self.sample_rate = sample_rate
        self.device_index = device_index
        self.output_file = output_file
        self.channels = channels  # Se None, usará 1 canal por padrão na gravação

    @staticmethod
    def listar_dispositivos():
        """
        Lista todos os dispositivos disponíveis, mostrando seus índices e quantidade de canais de entrada e saída.
        """
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            print(f"Índice {i}: {dev['name']} | Entrada: {dev['max_input_channels']} canais | Saída: {dev['max_output_channels']} canais")

    def gravar_com_dispositivo(self, indice_dispositivo=None, duration=None, sample_rate=None, output_file=None):
        """
        Grava áudio usando o dispositivo especificado.
        
        Parâmetros opcionais:
         - indice_dispositivo: Índice do dispositivo de entrada a ser utilizado. Se None, usa self.device_index.
         - duration: Duração da gravação. Se None, usa self.duration.
         - sample_rate: Taxa de amostragem. Se None, usa self.sample_rate.
         - output_file: Nome do arquivo de saída. Se None, usa self.output_file.
        """
        # Usa os valores padrão da instância, caso os argumentos não sejam passados
        if indice_dispositivo is None:
            indice_dispositivo = self.device_index
        if duration is None:
            duration = self.duration
        if sample_rate is None:
            sample_rate = self.sample_rate
        if output_file is None:
            output_file = self.output_file

        # Obtém informações do dispositivo para ajustar o número de canais
        try:
            device_info = sd.query_devices(indice_dispositivo, 'input')
        except Exception as e:
            print(f"Erro ao acessar o dispositivo com índice {indice_dispositivo}: {e}")
            return None

        max_channels = device_info.get('max_input_channels', 1)
        # Se self.channels não foi definido, usamos 1 canal; se definido, usamos o valor, mas limitamos ao máximo suportado.
        channels = self.channels if self.channels is not None else 1
        if channels > max_channels:
            print(f"O dispositivo suporta apenas {max_channels} canal(is). Ajustando a gravação para {max_channels} canal(is).")
            channels = max_channels

        print(f"Gravando com o dispositivo '{device_info['name']}' (índice {indice_dispositivo}) "
              f"usando {channels} canal(is) por {duration} segundos a {sample_rate} Hz...")
        
        # Configura o dispositivo e inicia a gravação
        sd.default.device = indice_dispositivo
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
        sd.wait()
        print("Gravação finalizada.")

        # Salva o áudio no arquivo especificado
        self.save_audio(audio, output_file, sample_rate)
        return audio

    def save_audio(self, audio_data, output_file, sample_rate=None):
        """
        Salva o áudio gravado em um arquivo WAV.
        
        Parâmetros:
         - audio_data: Dados do áudio gravado.
         - output_file: Nome do arquivo de saída.
         - sample_rate: Taxa de amostragem. Se None, usa self.sample_rate.
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
        wav.write(output_file, sample_rate, audio_data)
        print(f"Áudio gravado em {output_file}")

def read_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    input("Pressione Enter para sair...")
    pygame.mixer.music.stop()