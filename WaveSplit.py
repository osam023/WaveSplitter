#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave
import os
import click

OUTPUT_FILE_NAME = 'output'
COMBINE_CHANNEL = 2
COMBINE_SAMPLE = 2
COMBINE_FRAMERATE = 44100

"""
 This class is edit wave file divide/combine.
 
 TODO: support logfile.
"""
class WaveSplitter(object):
    __wave_path = ''
    __split_size = 1

    __output_dir = ''
    __workdir = ''

    __mode = 0 # 0:divid, 1:combine

    ## constructor.
    def __init__(self):
        pass

    ## wave file open.
    def set_wavefile(self, filename):
        self.__wave_path = os.path.dirname(os.path.abspath(filename))
        self.__wave_filename = filename
            
    ## split file size.
    def set_splitsize(self, num):
        try:
            self.__split_size = int(num)
        except ValueError, err:
            self.__split_size = 1

    ## divide wave file.
    def _divide(self):
        filename = os.path.join(self.__wave_path, self.__wave_filename)
        wave_data =  wave.open(filename, 'rb')
        filesize = wave_data.getnframes()
        split_file_size = filesize / self.__split_size

        position = [0]
        tmp = 0
        for item in range(0, self.__split_size):
            tmp += split_file_size
            if filesize > tmp:
                if tmp < filesize - 10240:
                    position.append(int(tmp))

        channels = wave_data.getnchannels()
        sample = wave_data.getsampwidth()
        framerate = wave_data.getframerate()

        counter = 0
        start = 0
        end = 0
        for item in position:
            counter += 1
            start = item
            try:
                if counter < self.__split_size:
                    end = filesize / self.__split_size
                else:
                    end = filesize - ((filesize / self.__split_size) * (self.__split_size - 1))
                self._output_file(start, end, counter, channels, sample, framerate, wave_data)
            except IndexError, ie:
                wave_data.close()
                break
        wave_data.close()
            
    ## write wave file.
    def _output_file(self, start, end, count, channels, sample, framerate, wave_data):
        self._check_workdir()

        output_filename = self._prefix(count) + '_' + OUTPUT_FILE_NAME + '.wav'
        filename = os.path.join(self.__workdir, output_filename)

        output_data = wave.open(filename, 'wb')
        output_data.setnchannels(channels)
        output_data.setsampwidth(sample)
        output_data.setframerate(framerate)
    
        wave_data.setpos(start)
        output_data.writeframes(wave_data.readframes(end))
        output_data.close()

    def set_outputdir(self, output_dir):
        self.__output_dir = output_dir

    ## checking work directory.
    ## if work directory not exists, create work directory.
    def _check_workdir(self):
        self.__workdir = os.path.join(self.__wave_path, self.__output_dir)
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
        if self.__output_name == 'output':
            self.__output_name == 'combine.wav'
        
        divide_files = []
        for filename in os.listdir(self.__workdir):
            filename = os.path.join(self.__workdir, filename)
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
        elif self.__mode == 1:
            self._combine()
        else:
            pass

## main method.
@click.command(help='Wave file splitter')
@click.option('-s', '--split-size', 'split_size', type=int, help='split size', default=2, required=False)
@click.option('-i', '--input-file', 'input_file', type=str, help='input file path(wave file only)', required=True)
@click.option('-o', '--output-dir', 'output_dir', type=str, help='output directory path', default='out', required=False)
def main(split_size, input_file, output_dir):
    ws = WaveSplitter()
    ws.set_splitsize(split_size)
    ws.set_wavefile(input_file)
    ws.set_outputdir(output_dir)
    ws.run()

if __name__ == '__main__':
    main()
