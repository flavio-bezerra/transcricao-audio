import streamlit as st
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import librosa
import io
import os

# Configuração inicial do Streamlit
st.title("Transcrição de Áudio com Pré-processamento")
st.write("Faça upload de um arquivo de áudio (.m4a, .mp3, etc.) para transcrever o conteúdo.")

# Diretório para salvar e ler os modelos
MODEL_CACHE_DIR = "./models"
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)

# Inicializa o session_state para armazenar a transcrição e o estado do áudio
if "transcription" not in st.session_state:
    st.session_state.transcription = None
if "processed_audio" not in st.session_state:
    st.session_state.processed_audio = None
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False
if "uploaded_audio" not in st.session_state:
    st.session_state.uploaded_audio = None

# Função para converter o áudio para WAV (em memória)
def convert_to_wav(audio_bytes, input_format):
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=input_format)
    wav_buffer = io.BytesIO()
    audio.export(wav_buffer, format="wav")
    return wav_buffer.getvalue()

# Função para pré-processar o áudio (em memória)
def preprocess_audio(audio_bytes):
    # Carrega o arquivo de áudio
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")

    # Normaliza o volume do áudio
    audio = audio.normalize()

    # Converte o áudio para um array NumPy para processamento
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate

    # Aplica a redução de ruído
    reduced_noise_samples = nr.reduce_noise(y=samples, sr=sample_rate, prop_decrease=0.85)

    # Converte o array NumPy de volta para AudioSegment
    audio = AudioSegment(
        reduced_noise_samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    # Aplica um filtro passa-alta para remover ruídos graves
    audio = audio.high_pass_filter(200)  # Frequência de corte: 200 Hz

    # Aplica um filtro passa-baixa para destacar os médios e agudos
    audio = audio.low_pass_filter(5000)  # Frequência de corte: 5000 Hz

    # Retorna o áudio pré-processado como bytes
    processed_buffer = io.BytesIO()
    audio.export(processed_buffer, format="wav")
    return processed_buffer.getvalue()

# Função para transcrever o áudio
def transcribe_audio(audio_bytes, model_id):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Carrega o modelo e o processador (usando cache local)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, 
        torch_dtype=torch_dtype, 
        low_cpu_mem_usage=True, 
        use_safetensors=True,
        cache_dir=MODEL_CACHE_DIR  # Salva o modelo no diretório local
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(
        model_id, 
        cache_dir=MODEL_CACHE_DIR  # Salva o processador no diretório local
    )

    # Cria o pipeline de reconhecimento automático de fala
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )

    # Carrega o áudio usando librosa
    audio_data, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=16000)  # Resample para 16kHz

    # Transcreve o áudio SEM timestamps
    result = pipe(audio_data, return_timestamps=True)
    return result["text"]

# Adiciona uma caixa de seleção para escolher o modelo
model_options = {
    "Whisper Small PT (deepdml)": "deepdml/whisper-small-pt-cv17",
    "Whisper Small (Oficial)": "openai/whisper-small",
    "Whisper Large (Oficial)": "openai/whisper-large-v3"
}
selected_model = st.selectbox("Escolha o modelo de transcrição", list(model_options.keys()))
model_id = model_options[selected_model]

# Adiciona um botão para escolher entre áudio original e pré-processado
use_original = st.checkbox("Usar áudio original sem tratativas de ruídos", value=True)  # Valor padrão True

# Upload do arquivo de áudio
uploaded_file = st.file_uploader("Selecione um arquivo de áudio", type=["m4a", "mp3", "wav"])

# Layout dos botões (Resetar à esquerda, Iniciar à direita)
col1, col2 = st.columns([2, 1])  # Larguras desiguais para criar espaço entre os botões

with col1:
    st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
    start_transcription_button = st.button("Iniciar Transcrição", disabled=uploaded_file is None)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="text-align: left;">', unsafe_allow_html=True)
    if st.button("Resetar Processamento"):
        st.session_state.transcription = None
        st.session_state.processed_audio = None
        st.session_state.model_loaded = False
        st.session_state.uploaded_audio = None
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)


if uploaded_file is not None:
    # Lê o conteúdo do arquivo carregado
    audio_bytes = uploaded_file.read()

    # Determina o formato do arquivo de entrada
    input_format = uploaded_file.name.split(".")[-1]

    # Converte para WAV (em memória)
    wav_bytes = convert_to_wav(audio_bytes, input_format)

    # Armazena o áudio carregado no session_state
    st.session_state.uploaded_audio = wav_bytes

    # Verifica se o botão "Iniciar Transcrição" foi pressionado
    if start_transcription_button:
        if use_original:
            st.write("Áudio original selecionado. Iniciando transcrição...")
            transcription = transcribe_audio(wav_bytes, model_id)
        else:
            st.write("Pré-processamento ativado. Iniciando transcrição...")
            # Pré-processa o áudio (em memória)
            processed_bytes = preprocess_audio(wav_bytes)
            transcription = transcribe_audio(processed_bytes, model_id)

        # Armazena a transcrição e o áudio processado no session_state
        st.session_state.transcription = transcription
        st.session_state.processed_audio = wav_bytes

    # Exibe o resultado
    if st.session_state.transcription:
        st.subheader("Texto Transcrito:")
        st.write(st.session_state.transcription)

# Botão para exportar a transcrição para um arquivo TXT
if st.session_state.transcription:
    if st.button("Exportar Transcrição para TXT"):
        # Cria o conteúdo do arquivo TXT
        txt_content = st.session_state.transcription.encode("utf-8")
        
        # Permite o download do arquivo TXT
        st.download_button(
            label="Baixar Arquivo TXT",
            data=txt_content,
            file_name="transcricao.txt",
            mime="text/plain"
        )
        st.success("Arquivo TXT gerado com sucesso!")
else:
    st.warning("Nenhuma transcrição disponível para exportar.")