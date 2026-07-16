import os
import moviepy as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

#----------------------------------------------------------------------------------------
# Mp4_to_Text_Split ⇒ MP4ファイルを無音で分割し、テキスト出力する。(Y.K)
#   :param input_file : 入力MP4ファイルパス
#   :param output_file: 出力テキストファイル
#   :param silence_thresh: 無音とみなす音量(dB)（デフォルト: -40dB）
#   :param min_silence_len: 無音とみなす最小ミリ秒（デフォルト: 1000ms = 1秒）
#----------------------------------------------------------------------------------------
def Mp4_to_Text_Split(input_file, output_file, silence_thresh=-40, min_silence_len=1000):

    print(f"動画データを読み込み中: {input_file}")
    # 動画データから音声データを抽出（MP4から読み込み可能）
    audio = AudioSegment.from_file(input_file, format="mp4")
    
    print("無音区間を検出して分割中...")
    # 無音部分で分割
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len, # 何ミリ秒無音が続いたら分割するか
        silence_thresh=silence_thresh,   # 何dB以下の音を無音とするか
        keep_silence=500                 # 分割時に残す無音の長さ(ms)
    )
    
    print(f"合計 {len(chunks)} 個のファイルに分割されました。")
    
    # 無音の箇所で分割した音声データをWAVファイルに書き出し、テキストに変換する
    text = ""
    audio_file = "buff.wav"
    for i, chunk in enumerate(chunks):
        chunk.export(audio_file, format="wav", bitrate="192k")
        # 音声からテキストを抽出
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = text + recognizer.recognize_google(audio_data, language="ja") # 日本語指定
            print(f"buff_{i+1:03d}.wav のテキスト化が完了！")

    # テキストを保存
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)

    # テキスト化の為の、一時音声ファイルを削除
    if os.path.exists(audio_file):
        os.remove(audio_file)
    else:
        print(f"{audio_file} は存在しません。")

# 使用例
if __name__ == "__main__":
    INPUT_MP4 = "../data/input.mp4"    # 分割したいMP4ファイル
    OUTPUT_FILE = "../data/out.txt"    # 保存先のファイル
    
    Mp4_to_Text_Split(INPUT_MP4, OUTPUT_FILE, -40, 3000)
