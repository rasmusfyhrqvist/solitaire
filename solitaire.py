import os, math, random, time

red = '\033[31m'
white = '\033[0m'
blue = '\033[38;5;17m'
yellow = '\033[38;5;214m'

class card:
  def __init__(self, id):
    self.suit = suits[math.floor(id/13)]
    self.value = (id%13)+1
    self.strValue = str(self.value).replace('11','J').replace('12','Q').replace('13','K').replace('1','A').replace('A0','10')
    self.group = (suits.index(self.suit)>1)
  
  def __str__(self):
    # Tulostetaan kortti
    color = (red if self.group else blue)
    return color+(self.suit+' '+self.strValue).ljust(4,' ')+white


suits = ('♠','♣','♥','♦')
deck = list(map(lambda i: card(i), list(range(52))))
random.shuffle(deck)

turned = []
ready = [['    ']]*4
error = ''

# Luodaan pelipöytä sekä "lukitut", eli kääntämättömät kortit
game = list(map(lambda i:[deck.pop()], list(range(7))))
locked = list(map(lambda i:list(map(deck.pop,list(range(i)))), list(range(7))))


# *********** FUNKTIOT ALKAA ***********

def displayGame():
  os.system('clear')
  print('\n\n    PASIANSSI\n\n')
  # Tulostetaan valmiit pinot
  print('  Valmiit pinot: | '+str(ready[0][-1])+'| '+str(ready[1][-1])+'| '+str(ready[2][-1])+'| '+str(ready[3][-1])+'|\n')
  # Tulostetaan pakan päällimmäinen kortti jos pakassa on kortteja
  print(('  Uusi kortti: | '+str(deck[-1])+' |' if len(deck)>0 else '  Pakka on tyhjä       ')+'    Nostettu: '+str(len(turned))+' kpl')
  print('\n\n\n       1     2     3     4     5     6     7\n')
  
  cardsChecked = [False]*7
  i = 0
  while not all(cardsChecked):
    rowString = '    '
    for p in range(7):
      if len(locked[p])>i:
        rowString += '|'+yellow+' -?- '+white
      elif len(game[p])>(i-len(locked[p])):
        rowString += '| '+str(game[p][i-len(locked[p])])
      else:
        rowString += '|     '
        cardsChecked[p] = True
    i += 1
    print(rowString+'|')
  print('\n\n\n    '+(red+error+white if len(error)>0 else ''))
  print('\n\n  Mikä on seuraava siirtosi?\n')
  
def displayHelp():
  os.system('clear')
  print('\n\n    PASIANSSI - APU\n\n')
  print('  Alla on selitetty mitä eri komennot tekevät:\n')
  print('    SIIRRÄ n m l\n    Siirtää sarakkeesta n, m kpl korttia sarakkeeseen l\n\n')
  print('    NOSTA n?\n    Nostaa kortin sarakkeeseen n tai kääntää kortin pakasta\n\n')
  print('    PINOA n\n    Siirtää sarakkeen n päällimmäisen kortin maansa pinoon\n\n')
  print('    APUA\n    Näyttää tämän apu-näkymän\n\n')
  print('    LOPETA\n    Lopettaa pelin\n\n')
  input('  Paina ENTER  jatkaaksesi ')

def getErrors(cmd):
  if cmd[0]=='apua' or cmd[0]=='lopeta':
    # Jos komento on apua tai lopeta
    return [cmd[0]]
  elif cmd[0]=='nosta' or cmd[0]=='pinoa':
    if len(cmd)==1 and cmd[0]=='nosta':
      return ['nosta-pakasta']
    if len(cmd)<2:
      raise ValueError('Ei tapeeksi parametrejä. Kokeile uudelleen.')
    try:
      params = [int(cmd[1])]
    except ValueError as err:
      # Jos parametria ei pysty muuntamaan numeroksi asetetaan virheellinen numero ja käsitellään myöhemmin
      params = [-1]

    # Tarkistetaan, että kyse on validista pinosta
    if cmd[0]=='pinoa' and params[0]==0:
      return ['pinoa-pakasta']
    elif params[0] < 1 or params[0] > 7:
      raise ValueError('Valitse sarake väliltä 1-7')
    else:
      return [cmd[0], params[0]-1]

    
  elif cmd[0]=='siirrä':
    if len(cmd)<4:
      raise ValueError('Ei tapeeksi parametrejä. Kokeile uudelleen.')

    try:
      params = [int(cmd[1]), int(cmd[2]), int(cmd[3])]
    except ValueError:
      params = [-1,-1,-1]

    if min(params[0],params[2])<1 or max(params[0],params[2])>7:
      raise ValueError('Valitse sarakkeet väliltä 1-7')
    elif params[1]<1:
      raise ValueError('Nosta vähintään yksi kortti')

    return ['siirrä',params[0]-1, params[1], params[2]-1]
    
  else:
    raise ValueError('Komentoa ei tunnistettu')

# *********** FUNKTIOT LOPPUU ***********


# displayHelp()
while True:
  try:
    # Näytetään peli
    displayGame()
    # Kysytään seuraavaa siirtoa ja nollataan virheet
    error = ''
    cmd = getErrors(str(input('  > ')).lower().split(' '))
  
    match cmd[0]:
      case 'nosta-pakasta':
        print('nosta-pakasta')
        if(len(deck)+len(turned)<1):
          raise ValueError('Pakassa ei ole kortteja')
        elif(len(deck)==0):
          turned.reverse()
          deck = turned
          turned = []
        else:
          turned += [deck.pop()]

    
      case 'pinoa-pakasta':
        if(len(deck)<1):
          raise ValueError('Pakassa ei ole kortteja')
        
        selected = deck[-1]
        selectedSuit = suits.index(selected.suit)
        
        if(selected.value == 1):
          ready[selectedSuit] = [deck.pop()]
        elif(ready[selectedSuit][-1] == '    '):
          raise ValueError('Ässä on pinottava ensin')
        elif(selected.value != ready[selectedSuit][-1].value +1):
          raise ValueError('Korttia ei voi pinota')
        else:
          ready[selectedSuit] += [deck.pop()]

    
      case 'nosta':
        if (len(deck)<1):
          raise ValueError('Pakassa ei ole kortteja')
          
        column = cmd[1]
        selected = deck[-1]

        if (selected.value == 13 and len(game[column])>0):
          raise ValueError('Kuninkaan voi sijoittaa vain tyhjään sarakkeeseen')
        elif(selected.value == 13):
          game[column] += [deck.pop()]
        elif len(game[column])==0:
          raise ValueError('Vain kuninkaan voi sijoittaa tyhjään sarakkeeseen')
        elif game[column][-1].value != selected.value +1:
          raise ValueError('Kortit on pinottava nousevassa arvojärjestyksessä')
        elif game[column][-1].group == selected.group:
          raise ValueError('Korttien on oltava eri värisiä')
        else:
          game[column] += [deck.pop()]


    
      case 'pinoa':
        column = cmd[1]
        if(len(game[column])<1):
          raise ValueError('Sarakkeessa ei ole kortteja')
        
        selected = game[column][-1]
        selectedSuit = suits.index(selected.suit)
        
        if(selected.value == 1):
          ready[selectedSuit] = [game[column].pop()]
        elif(ready[selectedSuit][-1] == '    '):
          raise ValueError('Ässä on pinottava ensin')
        elif(selected.value != ready[selectedSuit][-1].value +1):
          raise ValueError('Korttia ei voi pinota')
        else:
          ready[selectedSuit] += [game[column].pop()]

        if(len(game[column])==0 and len(locked[column])>0):
          game[column] += [locked[column].pop()]

    
      case 'siirrä':
        source = cmd[1]
        amount = cmd[2]
        target = cmd[3]

        if len(game[source])<amount:
          raise ValueError('Sarakkeessa ei ole tarpeeksi kortteja')
        
        topCard = game[source][-1*amount]

        if topCard.value == 13 and len(game[target]) > 0:
          raise ValueError('Kuninkaan voi sijoittaa vain tyhjään sarakkeeseen')
        elif topCard.value != 13:
          if len(game[target]) == 0:
            raise ValueError('Vain kuninkaan voi sijoittaa tyhjään sarakkeeseen')
          elif game[target][-1].value != topCard.value +1:
            raise ValueError('Kortit on pinottava nousevassa arvojärjestyksessä')
          elif game[target][-1].group == topCard.group:
            raise ValueError('Korttien on oltava eri värisiä')
        temp = []
        for i in range(amount):
          temp += [game[source].pop()]
        for i in range(amount):
          game[target] += [temp.pop()]

        if(len(game[source]) == 0 and len(locked[source])>0):
          game[source] += [locked[source].pop()]
    
      case 'apua':
        displayHelp()
      case 'lopeta':
        break
  except ValueError as err:
    error = str(err)

os.system('clear')
print('\n\n    KIITOS PELISTÄ!\n\n')
time.sleep(1.5)
os.system('clear')