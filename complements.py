import numpy as np
from scipy.io import wavfile
import pyaudio
from scipy import ndimage as ndi

# General variables used for both codes

# Dot duration in seconds
dd = 0.04 
# Frequancy of the tone in Hertz
fo = 330

dict_to_morse = {' ': '/'  , 'a': '.- ' , 'b': '-... ', 'c':'-.-. ', 'd':'-.. ' , 'e':'. '  , 'f':'..-. ', 'g':'--. ',
                   'h':'.... ', 'i':'.. '  , 'j':'.--- ' , 'k':'-.- ' , 'l':'.-.. ', 'm':'-- ' , 'n':'-. '  , 'o':'--- ',
                   'p':'.--. ', 'q':'--.- ', 'r':'.-. '  , 's':'... ' , 't':'- '   , 'u':'..- ', 'v':'...- ', 'w':'.-- ',
                   'x':'-..- ', 'y':'-.-- ', 'z':'--.. ' , 
                   '1':'.---- ', '2':'..--- ', '3':'...-- ', '4':'....- ', '5':'..... ','6':'-.... ','7':'--... ',
                   '8':'---.. ', '9':'----. ', '0':'----- ', '.':'a'
                  }

dict_to_text = {v: k for k, v in dict_to_morse.items()}

#---------------------------------------------------------------------------------------------------------
# ---- Function to generate the data base
#---------------------------------------------------------------------------------------------------------

def gen_base():
    dotm   = round(fo*dd)                  #estima longitud de los signos
    line   = round(3*fo*dd)                #estima longitud de lineas
    dmax   = 5*line + 4*dotm               #estima longitud máxima de una letra
    rep    = int(dotm)                     #define cantidad de repeticiones
    text = '0123456789abcdefghijklmnopqrstuvwxyz'
    total  = len(text)
    cont   = 0
    base   = np.zeros((total,dmax))
    
    for i in text:                        #recorre todos los caracteres
        morse,nums = translate(i)               #traducce cada uno
        senal  = np.zeros((1,dmax))         #crea senal vacia
        letra  = np.ravel(np.tile(nums,(rep,1)).T) #crea letra en morse binario
        senal[0,0:rep*len(nums)] = letra[0:dmax]   #la acota
        base[cont,:]=senal                  #la guarda en la base de datos
        cont=cont+1                         #aumenta el contador
    
    np.savez('base.npz',base=base)          #guarda la base de datos



#---------------------------------------------------------------------------------------------------------
# ----------------------------------------------Function to translate a string to written morse
#---------------------------------------------------------------------------------------------------------
    
def translate(texto):                     
    
    numeric =    {'.':[1,0],'-':[1,1,1,0],' ':[0,0],'/':[0,0] ,'a':[1] } # binary code
    morse = ''                          # Create a string
    nums = []                            # Create a list to save the numbers
    
    for t in texto:                     # for all characters in the input string                      
        morse += dict_to_morse.get(t.lower(),'a') # Use the lower case
        
    for n in morse:                     # translate morse in binary code
        nums = nums + numeric[n]
        
    return morse,nums                   # return the written morse and the binary code

def decode(morse):
    words = morse.split("/")
    text = ''
    for word in words:
        characters = word.split(" ")
        for ch in characters:
            ch_text = dict_to_text.get(ch+' ','')
            text += ch_text
        text += ' '
        
    return text




#---------------------------------------------------------------------------------------------------------
# --- Function to generate the audio file eith the morse message
#---------------------------------------------------------------------------------------------------------

def gen_audio_file(nums,name):
    
    # For the audio file:
    samples= 44100                          # define samples per second     (Sps)
    d=dd*len(nums)                          # define whole message duration (seconds)
    timing=np.arange(d*samples)             # define time vector
    seno=np.sin(2*np.pi*fo*timing/samples)  # define shape of the signal (Sinus by default)
    
    # Creating the signal:
    rep   = int(samples*dd)                 # define repetitions quantity 
    mask  = np.zeros((1,len(seno)))         # create the mask to turn on and off the sound
    mask[0,0:rep*len(nums)] = np.ravel(np.tile(nums,(rep,1)).T)
    
    signal = mask*seno                      # apply mask to the signal
    signal = np.int16(signal*1*32767)       # ajust amplitude and generate integers
    signal = signal.reshape(len(timing))    # add numpy signal format 
    
    wavfile.write(name+'.wav',samples,signal)       # generate sound file, save it as 'SoundMessage.wav'
    return 1




#---------------------------------------------------------------------------------------------------------
# --- Function to open audio file
#---------------------------------------------------------------------------------------------------------
def open_file(name):
    samplerate, data = wavfile.read(name +'.wav')
    return [samplerate,data]
    




#---------------------------------------------------------------------------------------------------------
# --- Function to record audio from microphone
#---------------------------------------------------------------------------------------------------------

def record(seconds):
    #=========================== RECORDING ============================#
    chunk = 1024                                        # 512 samples per chunk
    sample_format = pyaudio.paInt16                     # 16 bits resolution
    channels = 1
    fs = fo*30                                          # sampling speed (times 30, Nyquist shannon theorem)
    
    
    audio_obj = pyaudio.PyAudio()                       # Crear el objeto de audio
    #winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
    stream = audio_obj.open(format=sample_format, channels=channels, rate=fs,
                    frames_per_buffer=chunk, input=True)
    
    tramas = []                                         # Almacenar las tramas de audio
    sonido = []                                         # Se lee del buffer los valores numericos
    for i in range(0, int(fs / chunk * seconds)):
        datos = stream.read(chunk)
        tramas.append(datos)
        sonido.append( np.frombuffer(datos, dtype=np.int16) )
    
    stream.stop_stream()                                #detiene la grabación
    stream.close()
    audio_obj.terminate()
    return np.ravel(sonido)





#---------------------------------------------------------------------------------------------------------
# Function to process the audio signal and convert to morse
#---------------------------------------------------------------------------------------------------------

def process(senal0,fs = fo*30): # receive the data and the sampling frequency
    # if the sampling frequncy is not defined, it assumes that fs= 30*frecuency of the signal from the morse audio generator
    
    # Signal filtering
    vent   = int(fs/fo)                                 # window size
    dot    = round(fo*dd)                               # length of each symbol
    line   = round(3*fo*dd)                             # length of the lines
    esp    = round(5*fo*dd)                             # length of blank space
    dmax   = 5*line + 4*dot                             # maximum length of ch
    tol    = 5                                          # tolerance of processing
    
    senal1 = senal0 / np.max(np.abs(senal0))            # Normalizes the signal
    senal2 = mediamovil(abs(senal1),vent)               # apply moving average
    senal3 = energia(senal2,vent)                       # Calculate the energy spectrum of the signal
    senal4 = senal3>0.05 * 1                            # binarize the energy
    high   = np.where(senal4==1)                        # search "1" regions
    smorse = senal4[ np.min(high): np.max(high)]*1      # Obtain the morse as a signal
    
    mspace = np.asmatrix(1-smorse)                                            # detect the spaces as a matrix
    mspace = ndi.binary_erosion(mspace, structure=np.ones((1,line-tol)))*1    # erode blank spaces
    mspace = ndi.binary_dilation(mspace, structure=np.ones((1,line-tol)))*1   # dilation of blank spaces
    
    sspace = mspace.reshape(mspace.shape[1])            # space between characters
    regs   = 1-sspace                                   # regions with characters
    vspace,n  = ndi.label(regs)                         # label regions with characters
    prev   = 0                                          # position of the past word
    text =''                                            # create a string for the text
    
    for i in range(1,n+1):                              # for each indentified character
        etiqueta = np.where(vspace==i)                  # select the region of the character
        ini   = np.min(etiqueta)                        # determine the first position
        fin   = np.max(etiqueta)                        # determine the last position
        letra = smorse[ini : fin]                       # segment only that character
        letra = np.concatenate([letra,np.zeros(abs(dmax-len(letra)))])  # fill with zeros
        letra = letra[0:dmax]                           # if it's bigger than the limit stablished
        if (ini - prev) + tol>=esp:                     # determine if there is a big space
            text += ' '                                # if there is, that means that there is another word
        text += clasifica(letra)                       # classify the character
        prev  = fin  
    
    return [smorse,text]




#---------------------------------------------------------------------------------------------------------
#---------------------------------Funcion para filtro de media móvil
#---------------------------------------------------------------------------------------------------------
    
def mediamovil(senal,orden):                            #recibe señal y orden del filtro
    senal=np.concatenate([np.zeros(orden),senal])       #agrega ceros al inicio segun el orden
    medmov=[]                                           #declara la variable para el filtro
    for i in range(orden,len(senal),1):                 #recorre la señal
        y=np.sum( senal[i-orden:i])/orden               #promedia los valores
        medmov.append(y)                                #almacena el valor filtrado
    
    return np.array(medmov)                             #regresa la señal filtrada





#---------------------------------------------------------------------------------------------------------
#---------------------------------Funcion para calcular la energía
#---------------------------------------------------------------------------------------------------------
def energia(senal,ventana):                             #recibe la señal y el tamaño de ventana
    Energia = []                                        #declara variable para almacenar la señal
    for i in range (0, len(senal)-ventana,ventana):     #recorre la señal con el paso segun la ventana
        y = senal[ i : (i + ventana) ]                  #calcula la energía de esa ventana
        Energia.append( (1/ventana) * np.sum(y**2) )    #calcual y almacena el valor en la variable Energia
    
    return np.array(Energia)                            #Devuelve los n valores segun el numero de ventanas





#---------------------------------------------------------------------------------------------------------
# Function to classify each character using euclidian distance    
#---------------------------------------------------------------------------------------------------------
    
def clasifica(vec):                                     #recibe la señal a clasificar
    carga = np.load('base.npz')                         #carga la base de datos
    base  = carga['base']                               #asigna a una variable llamada base
    mat   = np.tile(vec,(base.shape[0],1))              #replica la señal a clasificar
    char  = np.argmin( np.sqrt(np.sum((mat-base)**2,axis=1)) ) #saca la menor dist. euclidiana
    if char > 9:                                        #si no es un numero del 0 al 9
        dict_letters = {10:'a',11:'b',12:'c',13:'d',14:'e',15:'f',16:'g',17:'h',
                       18:'i',19:'j',20:'k',21:'l',22:'m',23:'n',24:'o',25:'p',
                       26:'q',27:'r',28:'s',29:'t',30:'u',31:'v',32:'w',33:'x',
                       34:'y',35:'z'
                      }
        resp = dict_letters.get(char,'#')               #busca en el diccionario el caracter
    else:
        resp=str(char)                                  #si no, directamente es el numero
    return resp                                         #regresa el valor tipo string


gen_base()
