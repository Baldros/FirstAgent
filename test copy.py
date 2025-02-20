from readMic import ReadMic

# Avaliar quantidade de canais:
ReadMic.listar_dispositivos()

# Cria a instância da classe ReadMic definindo o device_index para o headset (por exemplo, índice 2)
read_mic = ReadMic(device_index=3, output_file="audio_gravado2.wav", duration=5, sample_rate=44100, channels=1)
print("Mic conectado")

# Grava o áudio utilizando o dispositivo correto (índice 2)
audio_data = read_mic.gravar_com_dispositivo(indice_dispositivo=3)
print("Áudio gravado")