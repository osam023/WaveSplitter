#!/usr/bin/env python
# coding:utf-8
import wave
import sys
import os
import getopt

"""
 this class is edit wave file divide/combile.
 
 TODO: support logfile.
"""
class WaveSplitter(object):
    __wave_data = None
    __wave_path = ''

    __filesize = 0
    __onefilesize = 0
    __split_size = 1

    __combine_channel = 2
    __combine_sample = 2
    __combine_framerate = 44100

    __output_name = "output"
    __workdir = ""

    __mode = 0 # 0:divid, 1:combile

    ## constructor.
    def __init__(self):
        pass

    ## wave file open.
    def set_wavefile(self, filename):
        self.__wave_path = os.path.dirname(os.path.abspath(filename))
        self.__wave_data = wave.open(filename, 'rb')
        self.__filesize = self.__wave_data.getnframes()
            
    ## split file size.
    def set_splitsize(self, num):
        try:
            self.__split_size = int(num)
        except ValueError, err:
            self.__split_size = 1

    ## divide wave file.
    def _divide(self):
        split_file_size = self.__filesize / self.__split_size
        
        pos = [0]
        tmp = 0
        for x in range(0, self.__split_size):
            tmp += split_file_size
            if self.__filesize > tmp:
                if tmp < self.__filesize - 10240:
                    pos.append(int(tmp))

        channels = self.__wave_data.getnchannels()
        sample = self.__wave_data.getsampwidth()
        framerate = self.__wave_data.getframerate()

        cnt = 0
        start = 0
        end = 0
        for x in pos:
            cnt += 1
            start = x
            try:
                if cnt < self.__split_size:
                    end = self.__filesize / self.__split_size
                else:
                    end = self.__filesize - ((self.__filesize / self.__split_size) * (self.__split_size - 1))
            except IndexError, ie:
                pass
                #print ie
            self._output_file(start, end, cnt, channels, sample, framerate)

    ## write wave file.
    def _output_file(self, start, end, count, channels, sample, framerate):
        self._check_workdir()

        filename = self.__workdir + self._prefix(count) + "_" + self.__output_name + ".wav"

        output_data = wave.open(filename, 'wb')
        output_data.setnchannels(channels)
        output_data.setsampwidth(sample)
        output_data.setframerate(framerate)
    
        self.__wave_data.setpos(start)
        output_data.writeframes(self.__wave_data.readframes(end))
        #print "create",
        #print self._prefix(count) + "_" + self.__output_name + ".wav",
        #print channels,
        #print sample,
        #print framerate
        output_data.close()

    ## checking work directory.
    ## if work directory not exists, create work directory.
    def _check_workdir(self):
        self.__workdir = self.__wave_path + "/out/"
        if not os.path.exists(self.__workdir):
            os.mkdir(self.__workdir)

    ## output file prefix.
    def _prefix(self, count):
        prefix = str(count)
        size = len(str(self.__split_size))
        for x in range(1, size):
            if size == len(prefix):
                break
            prefix = '0' + prefix
        return prefix

    ## combine wave files.
    def _combine(self):
        if self.__output_name == "output":
            self.__output_name == "combine.wav"
        
        divide_files = []
        for filename in os.listdir(self.__workdir):
            filename = self.__workdir + filename
            divide_files.append(wave.open(filename, 'rb'))

        output_data = wave.open(self.__output_name, 'wb')
        output_data.setnchannels(divide_files[0].getnchannels())
        output_data.setsampwidth(divide_files[0].getsampwidth())
        output_data.setframerate(divide_files[0].getframerate())
        
        for f in divide_files:
            output_data.writeframes(f.readframes(f.getnframes()))
            f.close()
        output_data.close()

    ## execute divide/combine.
    def run(self):
        if self.__mode == 0:
            self._divide()
            #print "divide success!!"
        elif self.__mode == 1:
            self._combine()
            #print "combine success!!"
        else:
            pass
            #print "error2."

    ## show class status.
    def show_status(self):
        pass
        #print self.__filesize
        #print self.__onefilesize
        #print self.__split_size
        #print self.__args
        #print self.__optlist

## main method.
def main():
    ws = WaveSplitter()
    ws.set_wavefile("loop2.wav")
    ws.set_splitsize(4)
    ws.run()

if __name__ == '__main__':
    main()
