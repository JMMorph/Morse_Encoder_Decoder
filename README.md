# Morse_Encoder_Decoder
This project allows to code and decode english to morse, from audio files, live audio recording and written messages
# Regarding the code
The theory behind this code is in wikipedia: https://en.wikipedia.org/wiki/Morse_code
so the Encoder and the decoder must follow these rules:

    The length of a dot "." is one unit
    The length of a line "-" is three units
    The space between parts of the same letter is one unit
    The space between letters is three units
    The space between words is seven units

# Encoder

The encoder is in the file "Generator.py", when you execute it, you must introduce the text, and then, you will hace the option to genereate an audio file, save it and play it before. When you specify the name of the file, do not include ".wav" or any format by default the file will be ".wav" format. Yaou can test this code just writting any text to obtain the written morse and select the opcions to save the audio file, then check the decoder.

The signal base for the message is a sinus wave with a frequency of 330 Hz, you can change this in the firstl lines of "complements.py", but if you do this, you will need to uncomment the line: "CM.gen_base()" in order to generate a new database for the Decoder. You can also change the dot duration in the "complements.py" file, and so, the duration of all other elements.

# Decoder 
The decoder is in the "MorseDecoder.py", you can select between text, audio file or audio recording.
You can test all options:
1.- Select "Decode written message" and paste this message: .. - /.-- --- .-. -.- ... /.--. . .-. ..-. . -.-. - .-.. -.--
2.- Select "Decode audio file" and type "example" to test with the example.wav file included
3.- Select "Decode recording" and play the example.wav with another player.
