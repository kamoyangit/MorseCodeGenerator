import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine

# モールスコードのマッピング
MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
        '7': '--...', '8': '---..', '9': '----.',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.',
        ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
        '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
    }

# テキスト（英文）の小文字を大文字に変換
def text_to_morse(text):
    morse = ''
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse += MORSE_CODE_DICT[char] + ' '
    return morse.strip()

# テキスト（英文）をモールスコードに変換
def morse_to_audio(morse_code, dot_length, frequency):
    dash_length = 3 * dot_length  # ダッシュはドットの3倍の長さ
    dot = Sine(frequency).to_audio_segment(duration=dot_length)
    dash = Sine(frequency).to_audio_segment(duration=dash_length)
    silence_short = AudioSegment.silent(duration=dot_length)  # ドットと同じ長さの間隔
    silence_long = AudioSegment.silent(duration=dash_length)  # ダッシュと同じ長さの間隔
    audio_output = AudioSegment.silent(duration=0)
    for code in morse_code:
        if code == '.':
            audio_output += dot + silence_short
        elif code == '-':
            audio_output += dash + silence_short
        elif code == ' ':
            audio_output += silence_long
    return audio_output

# メイン関数
def main():
    # UI部分の表示（タイトル、スライダー）
    st.title("Morse Code Generator")
    user_input = st.text_input("Enter text to convert to Morse Code:")
    duration = st.slider("Select the duration of a dot in milliseconds", 20, 200, 100)  # デフォルト値を100 msに設定
    frequency = st.slider("Select the frequency of the tone in Hz", 400, 1000, 700)  # デフォルト値を700 Hzに設定

    #if user_input:
    #    morse_code = text_to_morse(user_input)
    #    st.write("Morse Code: ", morse_code)
    #    audio = morse_to_audio(morse_code, duration, frequency)
    #    audio.export("morse_code.wav", format="wav")
    #    st.audio("morse_code.wav")

    if user_input:
        morse_code = text_to_morse(user_input)
        st.write("Morse Code: ", morse_code)
        audio = morse_to_audio(morse_code, duration, frequency)
        audio_path = "morse_code.wav"
        audio.export(audio_path, format="wav")
        st.audio(audio_path)
        with open(audio_path, "rb") as file:
            st.download_button(
                label="Download Morse Code as WAV",
                data=file,
                file_name="morse_code.wav",
                mime="audio/wav"
            )

# エントリーポイント
if __name__ == "__main__":
    main()
