import azure.cognitiveservices.speech as speechsdk
import os
import sys
import datetime
import re
# Creates an instance of a speech config with specified subscription key and service region.
speech_key = "5ea2a77e8cfe4574a4213f0cb3ca3f17"
service_region = "eastus"
def get_azure_wav(audio_file,txt,path,speaker,style):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    #Note: the voice setting will not overwrite the voice element in input SSML.
    #speech_config.speech_synthesis_voice_name = "zh-CN-XiaochenNeural"
    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    ssml_template = """
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts"
           xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="zh-CN">
        <voice name="{speaker}" style="{style}">{content}</voice>
    </speak>
    """
    data = {
        "speaker": speaker,
        "content": txt,
        "style": style
    }
    ssml = re.sub(r"\{(\w+)\}", lambda match: data.get(match.group(1), ""), ssml_template)
    result = speech_synthesizer.speak_ssml_async(ssml).get()

    #result = speech_synthesizer.speak_text_async(txt).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data_stream = speechsdk.AudioDataStream(result)

        # You can save all the data in the audio data stream to a file
        file_name =path+audio_file
        audio_data_stream.save_to_wav_file(file_name)
        print("Audio data for text [{}] was saved to [{}]".format(txt, file_name))

        # You can also read data from audio data stream and process it in memory
        # Reset the stream position to the beginning since saving to file puts the position to end.
        audio_data_stream.position = 0

        # Reads data from the stream
        audio_buffer = bytes(16000)
        total_size = 0
        filled_size = audio_data_stream.read_data(audio_buffer)
        while filled_size > 0:
            print("{} bytes received.".format(filled_size))
            total_size += filled_size
            filled_size = audio_data_stream.read_data(audio_buffer)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

#删除azure生成的wav文件
def delete_azure_wav(audio_file,path):
    file_name = path + audio_file
    os.remove(file_name)


#call the main function
if __name__ == "__main__":
    #通过命令行传入参数，下面是处理参数的逻辑
    if len(sys.argv) != 4:
         print("请输入语音文件路径")
         sys.exit()
    else:
       audio_file = sys.argv[1]
       txt= sys.argv[2]
       path = sys.argv[3]
    #给audio_file后面加上日期时间戳，以便于保存到存储库中
    now = datetime.datetime.now(datetime.timezone.utc)
    audio_file += "_" + str(now.strftime("%Y-%m-%d_%H:%M:%S"))+".wav"
    get_azure_wav(audio_file,txt,path)