# Audio File Split Tool: wave\_splitter

wave\_splitter provide audio split feature. This tool have to use Python version 2.7. Cannot run this tools under Python 3.X.

## Install

1. Install third party library called [Click](http://click.pocoo.org/5/) into your Python environment.

    ```sh
    $ pip install click
    ```
   
2. Clone wave\_splitter where you want it installed(ex: ~/.bin). Installed path is better set environment PATH.

    ```sh
    $ git clone https://github.com/osam023/WaveSplitter.git ~/.bin
    $ echo "export PATH=$PATH:$HOME/.bin" >> ~/.bash_profile
    ```
    **ATTENTION:** If you already have **.bin** directory, then you change current directory to **.bin**. And clone the wave_splitter.

3. Restart your shell.

4. Check the wave\_splitter install success.

   ```sh
   $ wave_splitter --version
   ```

**NOTE:**
If you cannot execute wave\_splitter, Set execute authority that program(```$ chmod +x wave_splitter```).

## Usage

You can split the audio file by executing below command. If you have to more information, use --help option.

```sh
$ wave_splitter --split-size [split size] --input-file [input file path] --output-dir [output directory path]
```

### Option Variables

option(long) | option(short)| required | description
---|---|---|---
--split-size|-s|NO|Split size number. Default is 2.
--input-file|-i|YES|Input audio file path.
--output-dir|-o|NO|Output directory path. Default is **./out/**

## License

See LICENSE file.
