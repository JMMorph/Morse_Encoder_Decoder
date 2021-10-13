'''
Morse generator by J. Miguel Medina

This code generates a morse code from a message defined by the user, it allows to generate written morse and the audio file
There are default parameters that are important for the decoder, first, the duration of the "dot" defines the duration of
everything else in the message, this means that the duration of the dot is the unit, so:
    
    The length of a dot "." is one unit
    The length of a line "-" is three units
    The space between parts of the same letter is one unit
    The space between letters is three units
    The space between words is seven units

Also the frequency of the tone is defined by a parameter, so you can change these in the first lines of code from the "complements.py" file,
just remember to save and uncomment the line "CM.gen_base()" of this code the first time you use a new configuration

'''

import winsound
import complements as CM
#CM.gen_base() # Execute this line just the first time after change the parameters "dd" and "fo" in complements.py
print('Hello, please enter the text to be translated to morse, avoid use of symbols other than letters and numbers')

# the variable "nombre" contains the text to generate the morse code
message = input('text: ')                # text to translate
morse,nums = CM.translate(message)       # apply the function 'translate', gets the binary code and the written morse

print('The text: \'' + message +'\' in Morse is:')
print(morse)                            
print('Do you want to generate the audio file with the message?')
opt = int(input('1.- Yes 2.- No\n'))

if opt == 1:    
    name = input('Name of the audio file to be saved: ')
    CM.gen_audio_file(nums,name)
    print('Sound saved as: '+name+'.wav')
    play = int(input('If you want to play the message press 1, else press 2\n'))
    if play == 1: winsound.PlaySound(name+'.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

print('Done, happy do help! :D')