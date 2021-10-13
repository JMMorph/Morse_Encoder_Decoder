'''
Morse decoder by J. Miguel Medina

This code decodes a morse code from a written message, an audio file or an audio recording, the message for both audio options must 
follow these guidelines:
    
    The length of a dot "." is one unit
    The length of a line "-" is three units
    The space between parts of the same letter is one unit
    The space between letters is three units
    The space between words is seven units

Also the frequency of the tone is defined by a parameter, so you can change these in the first lines of code from the "complements.py" file,
just remember to save and uncomment the line "CM.gen_base()" of this code the first time you use a new configuration

'''

import matplotlib.pyplot as plt
import complements as CM


opt = 5;
while opt >4:
    print("Morse decoder V1. Select what you want to decode")
    print("1.- Decode written message ")
    print("2.- Decode audio file ")
    print("3.- Decode recording")
    print("4.- Exit")
    opt = int(input(''))
    if opt>4: print('Not an option, please try again')
    
if opt == 1:                                        # decode written message
    print('Insert the message here: ')
    w_message = input('')                           # Receive the text
    text = CM.decode(w_message)
    print('The decoded message says: ')
    print(text)
    
if opt ==2:
    name = input('Insert name of the wav file (without .wav): \n')
    [fs,audio] = CM.open_file(name)
    print('Processing audio signal...')
    [smorse,text] = CM.process(audio,fs)
    print('Signal processed, message decoded')
    
    print(text)
    
    plt.figure()
    plt.subplot(121)
    plt.title('Audio file')
    plt.plot(audio)
    plt.subplot(122)
    plt.plot(smorse)
    plt.title('Processed signal: '+text)
    plt.show()
    

if opt == 3:
    time = int(input('seconds to record: '))
    input('click to start recording')
    print('Recording')
    audio = CM.record(time)
    print('Recording finished') 
    print('Processing audio signal...')
    [smorse,text] = CM.process(audio)
    print('Signal processed, message decoded')
    
    plt.figure()
    plt.subplot(121)
    plt.title('Audio recorded')
    plt.plot(audio)
    plt.subplot(122)
    plt.plot(smorse)
    plt.title('Processed signal: '+text)
    plt.show()