# 🎤 Transcrição Automática de Áudio

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)]( https://streamlit.io )  
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]( https://www.python.org/ )  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)]( https://opensource.org/licenses/MIT )

Este projeto foi desenvolvido a partir de uma conversa casual no corredor, onde uma amiga compartilhou uma demanda prática: ela havia gravado uma reunião e precisava transcrever o áudio para criar a ata da reunião. A tarefa manual de transcrição é trabalhosa, demorada e propensa a erros. Para resolver esse problema, criamos uma ferramenta automatizada que facilita a transcrição de áudios com qualidade e eficiência.

O objetivo principal do projeto é permitir que qualquer pessoa faça upload de um arquivo de áudio (como `.m4a`, `.mp3` ou `.wav`) e obtenha uma transcrição textual clara e organizada. Além disso, a ferramenta oferece opções de pré-processamento para melhorar a qualidade do áudio antes da transcrição, garantindo resultados mais precisos.

---

## 🚀 Funcionalidades Principais

1. **Upload de Arquivo de Áudio**:
   - O usuário pode fazer upload de arquivos de áudio nos formatos `.m4a`, `.mp3` ou `.wav`.

2. **Pré-processamento de Áudio**:
   - Normalização do volume.
   - Redução de ruído.
   - Filtros passa-alta e passa-baixa para destacar frequências relevantes e remover ruídos indesejados.

3. **Transcrição Automática**:
   - Utiliza modelos avançados de IA, como os modelos **Whisper** da OpenAI ou outros modelos customizados, para transcrever o conteúdo do áudio com alta precisão.

4. **Escolha de Modelos de Transcrição**:
   - O usuário pode escolher entre diferentes modelos de transcrição, incluindo:
     - **Whisper Small PT (deepdml)**: Modelo personalizado para o português brasileiro.
     - **Whisper Small (Oficial)**: Modelo oficial da OpenAI para transcrição geral.
     - **Whisper Large (Oficial)**: Modelo oficial mais robusto, ideal para maior precisão.

5. **Exportação da Transcrição**:
   - Após a transcrição, o texto pode ser exportado para um arquivo `.txt` para uso posterior (por exemplo, na criação da ata da reunião).

6. **Interface Amigável**:
   - A aplicação utiliza o **Streamlit**, uma biblioteca Python para criação de interfaces web interativas, garantindo uma experiência intuitiva e fácil de usar.

---

### **Demonstração:**

<div style="text-align: center;">
  <img src="demonstration-image.gif" alt="Gatinho dançando" />
</div>

---

## 💻 Como Executar o Projeto

### **Pré-requisitos**

1. **Python 3.8+** instalado no sistema.
2. Um ambiente virtual (opcional, mas recomendado).
3. As dependências listadas no arquivo `requirements.txt`.
4. FFmpeg instalado no sistema (necessário para processamento de áudio).

### **Passos para Executar**

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/flavio-bezerra/transcricao-audio.git 
   cd transcricao-audio
   ```

2. **Instale as dependências usando o script `install.bat`**:
   - Na raiz do projeto, execute o arquivo `install.bat` para instalar automaticamente todas as dependências necessárias, incluindo o FFmpeg.
   - O script executa o seguinte processo:
     - Atualiza o `pip` para a versão mais recente.
     - Instala as bibliotecas listadas no arquivo `requirements.txt`.
     - Instala o FFmpeg no sistema usando o gerenciador de pacotes `winget` (Windows).
   - Comando para executar o script:
     ```bash
     install.bat
     ```

3. **Execute o aplicativo**:
   Use o comando abaixo para iniciar o servidor Streamlit:
   ```bash
   streamlit run app.py
   ```
   Outra posibilidade é criar um atalho do arquivo: 
    ```bash 
    run_app.bat
    ```
     e utilizar o icone que está na pasta raiz:

    ```bash 
    logo.icon
    ```

4. **Acesse a interface**:
   Abra o navegador e acesse o endereço fornecido pelo terminal (geralmente `http://localhost:8501`).
   
**Obs.:** Na primeira execução do Dashboard, o processo poderá ser mais demorado, pois os modelos serão baixados automaticamente para a pasta *models*. Esses arquivos não estão incluídos no repositório Git devido ao seu tamanho — somados, ultrapassam 4 GB.

---

## 🛠️ Instruções de Uso

1. **Faça upload de um arquivo de áudio**:
   - Clique no botão "Selecione um arquivo de áudio" e escolha o arquivo desejado (`.m4a`, `.mp3`, `.wav`).

2. **Escolha o modelo de transcrição**:
   - Selecione o modelo de IA que deseja usar para a transcrição no menu suspenso.

3. **Configure o pré-processamento (opcional)**:
   - Marque/desmarque a opção "Usar áudio original sem tratativas de ruídos" para habilitar/desabilitar o pré-processamento.

4. **Inicie a transcrição**:
   - Clique no botão "Iniciar Transcrição" para processar o áudio e gerar a transcrição.

5. **Exporte o resultado**:
   - Após a transcrição, clique no botão "Exportar Transcrição para TXT" para baixar o arquivo `.txt`.

6. **Resetar o processo**:
   - Caso deseje começar novamente, clique no botão "Resetar Processamento".

---

## 📦 Dependências

As principais bibliotecas utilizadas neste projeto são:

- **Streamlit**: Framework para criar interfaces web interativas.
- **PyDub**: Biblioteca para manipulação de arquivos de áudio.
- **Noisereduce**: Biblioteca para redução de ruído em sinais de áudio.
- **Librosa**: Biblioteca para análise e processamento de áudio.
- **Transformers (Hugging Face)**: Biblioteca para carregar e usar modelos de IA, como o Whisper.
- **Torch**: Framework de aprendizado profundo usado pelos modelos de IA.

Para instalar todas as dependências, execute o script `install.bat` na raiz do projeto:
```bash
install.bat
```

O script `install.bat` executa o seguinte PowerShell Script (`setup.ps1`):
- Atualiza o `pip`.
- Instala as bibliotecas do arquivo `requirements.txt`.
- Instala o FFmpeg no sistema usando o gerenciador de pacotes `winget`.

---

## 🌟 Motivação

Este projeto nasceu de uma necessidade real: a dificuldade de transcrever gravações de reuniões manualmente. Ao automatizar esse processo, esperamos ajudar pessoas como a nossa amiga a economizar tempo e esforço, permitindo que foquem em atividades mais estratégicas, como revisar e formatar a ata final.

Além disso, este projeto demonstra como tecnologias modernas, como IA e processamento de áudio, podem ser aplicadas para resolver problemas cotidianos de forma simples e acessível.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Se você quiser melhorar o projeto, adicionar novas funcionalidades ou corrigir bugs, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para sua contribuição:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Faça suas alterações e envie um pull request.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Você pode usar, modificar e distribuir o código livremente, desde que mantenha os créditos originais.

---

## 📧 Contato

Se tiver dúvidas, sugestões ou quiser colaborar, entre em contato:

- **Email**: flaviomenegueco@gmail.com
- **LinkedIn**: [https://www.linkedin.com/in/flavio-m-bezerra/](https://www.linkedin.com/in/flavio-m-bezerra/ )
- **GitHub**: [https://github.com/flavio-bezerra](https://github.com/flavio-bezerra)

---

Esperamos que esta ferramenta seja útil para você e que facilite a criação de atas de reunião e outras tarefas relacionadas à transcrição de áudio! 🎤📝
