import pyaudio
import wave
from aip import AipSpeech


class AudioRecognition(object):
    def __init__(self):
        p = pyaudio.PyAudio()
        self.dir = p.get_device_info_by_index(0)
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1  # 单声道
        self.fs = 16000  # 采样频率
        self.seconds = 3  # 每次录制时间
        self.filename = "../output.wav"  # 输出文件名
        self.result = '未识别'  # 识别结果
        # aip接口
        self.APP_ID = '22467299'
        self.API_KEY = 'Mk0phOlttBGslvc3OI0j0ob0'
        self.SECRET_KEY = '6pbEKy0e2SsTDyW63gnyZSEwQ4t2mh8a'

    def record(self):  # 录入
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
        stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True,
                        )
        frames = []
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
            if i % 5 == 0:
                print("*")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def recognition(self):  # 识别
        client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

        # 读取文件
        def get_file_content(file_path):
            with open(file_path, 'rb') as fp:
                return fp.read()

        # 识别本地文件
        result = client.asr(get_file_content(self.filename), 'wav', 16000, {
            'dev_pid': 1537,  # 默认1537（普通话 输入法模型）
        })
        self.result = result['result'][0]
    @staticmethod
    def microphone():  # 设备识别,打印系统音频设备参数
        p = pyaudio.PyAudio()
        print(p)
        for i in range(p.get_device_count()):
            print(p.get_device_info_by_index(i))
        print(p.get_device_info_by_index)

def output():
    a = AudioRecognition()
    print("开始录制")
    a.record()
    print("正在识别......")
    a.recognition()
    print("结果")
    print(a.result)
    return a.result
if __name__ == '__main__':
    # 从录制到识别出结果整个过程
    a = AudioRecognition()
    #print("开始录制")
    #a.record()
    print("正在识别......")
    a.recognition()
    print("结果")
    print(a.result)
    # a.microphone()
