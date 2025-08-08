# Gemini Video AI Summarizer

An advanced web application built with Python and Streamlit that uses Google's Gemini Pro model to analyze video content. Users can upload a video, ask questions, and receive comprehensive summaries that can be translated and converted to speech.


***

## ## Live Application

**You can access a live deployed demo here:**
[**➡️ Live Video Summarizer App**](https://your-live-app-url.com) ***

## ## Features

* **AI-Powered Video Analysis**: Upload a video file and ask complex questions about its content.
* **Comprehensive Summaries**: Generates detailed, essay-style summaries with titles, subjects, and key topics explained.
* **Multi-Language Translation**: Translates the generated summary into various languages, including Telugu, Hindi, French, and Spanish.
* **Text-to-Speech Output**: Listen to both the original English summary and the translated versions with integrated audio playback.
* **Interactive User Interface**: A clean and modern UI built with Streamlit for easy file uploads and interaction.

***

## ## Tech Stack

* **Core Language**: Python
* **Web Framework**: Streamlit
* **AI Model**: Google Gemini Pro (`gemini-2.0-flash`)
* **Key Libraries**:
    * `google-generativeai` for interacting with the Gemini API.
    * `gTTS` for text-to-speech conversion.
    * `python-dotenv` for managing environment variables.

***

## ## Getting Started

To run this project on your local machine, follow these steps.

### ### Prerequisites

Make sure you have Python 3.8+ and pip installed on your system.

### ### Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/gemini-video-summarizer.git](https://github.com/your-username/gemini-video-summarizer.git)
    cd gemini-video-summarizer
    ```

2.  **Create and Activate a Virtual Environment**
    * **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Create a `requirements.txt` file**
    * Create a file named `requirements.txt` and add the following lines:
        ```
        streamlit
        google-generativeai
        python-dotenv
        gTTS
        phi-agent
        ```

4.  **Install the Required Libraries**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Environment Variables**
    * Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Create a file named `.env` in the root project directory.
    * Add your API key to the `.env` file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

6.  **Run the Streamlit Application**
    ```bash
    streamlit run videosummarizer.py
    ```
    * After running the command, open your web browser and navigate to the local URL provided (usually `http://localhost:8501`).

***

## ## Project Structure
