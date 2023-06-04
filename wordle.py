# %%
wordfile = open('wordle_list.txt','r')
words = wordfile.readlines()
wordfile.close()
wordlist = []
for word in words:
    if ('\n' in word): wordlist.append(word[:-1])
    else: wordlist.append(word)

# %%

def genFrequency(wordlist):
    freq = {}
    for word in wordlist:
        lets = []
        for letter in word:
            if letter not in freq:
                freq[letter] = 1
            elif letter in lets:
                freq[letter] += 0.25
            else:
                freq[letter] += 1
            lets.append(letter)

    return list(dict(sorted(freq.items(), key=lambda item: item[1])).keys())[::-1]

#earotlisnc

# %%
c = 0
for word in wordlist:
    lets = []
    for letter in word:
        if letter in lets:
            c += 1
        lets.append(letter)

# print(c)

# %%

def genPlaceFrequency(wordlist):
    freq = [{}, {}, {}, {}, {}]
    for word in wordlist:
        count = 0
        for letter in word:
            if letter not in freq[count]:
                freq[count][letter] = 1
            else:
                freq[count][letter] += 1
            count += 1

    freqlst = [[], [], [], [], []]
    for i in range(5):
        #print(list(dict(sorted(freq[i].items(), key=lambda item: item[1])).keys())[::-1])
        freqlst[i] = list(dict(sorted(freq[i].items(), key=lambda item: item[1])).keys())[::-1]

    return freqlst

genPlaceFrequency(wordlist)

# %%

def cleanWordlist(wordlist, wrong, right, place, wrongplace):
    foundWords = []
    for word in wordlist:
        good = True
        count = 0
        rightletters = right.copy()
        for letter in word:
            if letter in wrong or place[count] and word[count] != place[count] or letter in wrongplace[count]:
                good = False
                break
            if letter in rightletters:
                rightletters.remove(letter)
            count += 1
        if len(rightletters) == 0 and good:
            foundWords.append(word)

    return foundWords

# %%

def findWords(wordlist, let):
    foundWords = []
    for word in wordlist:
        letInWord = False
        for letter in word:
            if let == letter: 
                letInWord = True
        if letInWord:
            foundWords.append(word)

    return foundWords

# %%

def findBestWords(wordlist):
    count = 0
    temp = wordlist.copy()
    times = 0
    while len(temp) > 5 and count < 26:
        freq = genFrequency(temp)
        newtemp = findWords(temp, freq[count])
        count += 1
        if len(newtemp) != 0:
            temp = newtemp
        times += 1
        if times > 20:
            break
    return temp

# print(findBestWords(wordlist))

# %%
import math
def findBestPlace(wordlist, remaining):
    freqplace = genPlaceFrequency(remaining)
    best = 0
    bestword = ""
    for word in wordlist:
        count = 0
        for place in range(5):
            count += freqplace[place].index(word[place])
        if (count > best):
            best = count
            bestword = word
    
    return bestword

    # look at index - sum indexs of each letter, lowest wins

# findBestPlace(['cater', 'crate', 'react', 'trace'])

# %%
def cleanWithOutput(word, colors, wrong, right, place, wrongplace):
    rightletters = {}
    wrongletters = {}
    for i in range(5):
        letter = word[i]
        if colors[i] == 'g':
            if letter in rightletters: rightletters[letter] += 1
            else: rightletters[letter] = 1
            place[i] = letter
        elif colors[i] == 'y':
            if letter in rightletters: rightletters[letter] += 1
            else: rightletters[letter] = 1
            if letter not in wrongplace[i]: wrongplace[i].append(letter)
        elif colors[i] == 'b':
            if letter in wrongletters: wrongletters[letter] += 1
            else: wrongletters[letter] = 1

    for prevletter in right:
        if prevletter not in rightletters:
            rightletters[prevletter] = 1

    right = []
    for letter in rightletters:
        for i in range(rightletters[letter]):
            right.append(letter)
    
    for letter in wrongletters:
        if letter not in right and letter not in wrong:
            wrong.append(letter)

    return (wrong, right, place, wrongplace)

# %%

def solveWordle():
    wrong = []
    right = []
    place = ['', '', '', '', '']
    wrongplace = [[], [], [], [], []]
    while True:
        newwordlist = cleanWordlist(wordlist, wrong, right, place, wrongplace)
        narrow = findBestWords(newwordlist)
        narrowplace = findBestPlace(narrow, newwordlist)
        print(newwordlist)

        print(narrow)
        print(narrowplace)

        word = input("Word guess: ")
        colors = input("Color output: ")
        if (colors == 'ggggg') or (word == 'quit'):
            break

        wrong, right, place, wrongplace = cleanWithOutput(word, colors, wrong, right, place, wrongplace)
        
solveWordle()