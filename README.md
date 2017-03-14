# Audio File Split Tool: wave\_splitter
wave\_splitter provide audio split feature. This tool have to use Python version 2.7. Cannot run this tools under Python 3.X.

## Install
1. Install third party library called [Click](http://click.pocoo.org/5/) into your Python environment.

   $ pip install click
   
2. Clone wave\_splitter where you want it installed(ex: ~/.bin). Installed path is better set environment PATH.

	$ echo "export PATH=$PATH/.bin" >> ~/.bash_profile

3. Restart your shell.

**NOTE:**
If you cannot execute wave\_splitter, Set execute authority that program($ chmod +x wave\_splitter).

## Usage
You can split the audio file by executing below command. If you have to more information, use --help option.

$ wave\_splitter --split-size [ _split size_ ] --input-file [ _input file path_ ] --output-dir [ _output directory path_ ]

### Option Variables
option(long) | option(short)| required | description
---|---|---|---
--split-size|-s|NO|Split size number. Default is 2.
--input-file|-i|YES|Input audio file path.
--output-dir|-o|NO|Output directory path. Default is **./out/**

## License
See LICENSE file.
