#!/usr/bin/python2.5
# FALLOUT 3 Terminal hacker assistant
# stephen@sa7ori.org

#NOTE: python 3.1 is gay
#navi-two:~ s7ephen$ cat test.py 
#a = [1,2,3]
#for num in a:
#    print num
#navi-two:~ s7ephen$ python2.5 test.py 
#1
#2
#3
#navi-two:~ s7ephen$ python test.py 
#  File "test.py", line 3
#    print num
#            ^
#SyntaxError: invalid syntax
#navi-two:~ s7ephen$ ls -alt `which python`
#lrwxr-xr-x  1 root  wheel  24 Aug 10 16:24 /usr/bin/python -> /usr/local/bin/python3.1
#navi-two:~ s7ephen$ 
#
# Anyway the Fallout 3 Terminal In-Game thing works like this
# you are given a buncha words of equal string length, when you guess a word
# if your guess is not correct the game will tell you how many letters are in
# the same place in the correct word. EG : If the correct word is "THING" and
# you guess "BRING" it will report 3/5 because "I", "N", and "G" have the same
# placement in the main word.

import sys
import pprint as pp

def count_letters(word, wordlist, trycount):
    """ Figure out the new subset of words based on the words entered. """
    print "\n",word," and the following words have letters in the same placement"
    wordlen = len(word)
    filtered = []
    for w in wordlist:
        match_count = 0
        for i in range(len(word)):
            if word[i] == w[i]:
                match_count += 1
        if match_count == trycount: #we found a word that has same number of matches
            filtered.append(w) 
    return filtered

print """

    ...oooOOO Welcome to the Fallout 3 Terminal Hacker OOOooo...

"""
print """Enter words in the wordlist. 
You can enter the words all at once as CSV (nospaces after comma) or one at a time.
If you enter them one at a time, press CTRL-C when done."""
wordlist = []
i = 0
try:
    while True:
        prompt = "Word (or wordlist)? "+str(i)+"> "
        tmp = raw_input(prompt)
        if tmp.__contains__(","):
            wordlist = str.split(tmp,',')
            break
        wordlist.append(str.strip(tmp))
        i+=1 
except KeyboardInterrupt:
    pass

for word in wordlist:
    if len(word) != len(wordlist[0]):
        
        csv_courtesy = ""
        print "THERE IS SOMETHING WRONG at ",word," ALL WORDS SHOULD BE OF SAME LENGTH!"
        for word in wordlist:
            csv_courtesy+=word
            csv_courtesy+=","
        print "Here is your wordlist (cut-and-paste) to reuse. \n*** "
        print csv_courtesy[:len(csv_courtesy)-1] # chop off the last comma
        print "\n***\nExiting."
        sys.exit(1)

print "\nNow try a word in the game. Which one did you try?"
for i in range(len(wordlist)):
    print "\t",i,". ", wordlist[i]
num=raw_input("num of word?> ")
num = int(num)
print "How many of ",len(wordlist[num])," did it say matched? ",
try1 = raw_input("?> ")
try1 = int(try1)
print "Ok, of those these are the possible words.\nTry one of these in the game..."
newlist = count_letters(wordlist[num],wordlist,try1)
for i in range(len(newlist)):
    print "\t",i,". ", newlist[i]
num = raw_input("Enter the number of the one you tried. ")
num = int(num)
print "How many of ",len(newlist[num])," did it say matched? ",
try2 = raw_input("?> ")
try2 = int(try2)
lastlist = count_letters(newlist[num],newlist,try2)
print "It should be one of the following words"
pp.pprint(lastlist)

