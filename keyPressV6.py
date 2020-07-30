# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
Created on Tue Jul 28 23:01:30 2020

stackoverflow.com/questions/3523174/raw-input-in-python-without-pressing-enter
www.devdungeon.com/content/curses-windows-python

***must pip install windows-curses to run on Windows
doesn't work in ipython console (tries to continuously connect to kernel) 
doesn't work properly in pyCharm console (requires Enter after each input)
works properly when run in Linux terminal (and endwin() is used to shutdown app)
works in pydroid 3 app on Android

***all stdout (i.e. print statements) output gets buffered until curses code is complete
even if the stdout code precedes the curses code

***must size the terminal to provide sufficient space,
if terminal size is too small, app will crash
"""
import curses
import time

# text = input("Please enter your text \n")
inputText = "This is a test of the first letter program. It uses the curses module in Python to capture key inputs " \
            "from the user and show them on a console that is painted on top of the system console."

if isinstance(inputText, str):
    # convert input string into list of words
    txtList = inputText.split()
    numWords = len(txtList)
    # print(numWords)

# join list slices into strings
# print(' '.join(txtList[:]))
# print(' '.join(txtList[:numWords - 1]))
# -----------------------------------------------

win = curses.initscr()
# curses.noecho()
num_rows, num_cols = win.getmaxyx()

# curses.start_color()
# Completed Text
# curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
# Hidden Text
# curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)

message = 'Please enter the first letter of the selected input text: (0 to exit, 1 to preview)'
win.addstr(0, 0, message)
win.addstr(2, 0, '') # position of cursor

# win.addstr(0, 0, inputText)
# win.addstr(10, 0, '')  # final position of cursor

count = 0
bufferSize = 20  # number of words that can be shown on screen at any given time in quiz mode
hintSize = 5  # number of words ahead of current word that user can see
start = 0
end = numWords
while True:
    word = txtList[count]

    # calculate start index for quiz mode, based on buffer size
    if count > bufferSize:
        start = start + 1

    # calculate end index for preview mode, based on hintSize
    if count < (numWords - hintSize):
        end = count + hintSize
    else:
        end = numWords

    # phrase1 = ' '.join(txtList[:count + 1])
    # phrase2 = ' '.join(txtList[count + 1:])

    ch = win.getch()
    c = chr(ch)
    if c.lower() == '0':
        keyPress = 'Exiting program - you typed {}'.format(c)

        win.clear()
        win.addstr(0, 0, keyPress)
        win.addstr(2, 0, '')
        win.refresh()
        break
    if c.lower() == '1':
        keyPress = 'Preview Mode - you typed {}'.format(c)

        # only show # of words specified by buffer size plus a preview of hint size (default: 5 words)
        # due to limited screen space
        preview = ' '.join(txtList[start:end])

        win.clear()
        win.addstr(0, 0, keyPress)
        win.addstr(2, 0, preview)
        win.addstr(6, 0, '')
        win.refresh()
    elif c.lower() == word[0].lower():
        keyPress = 'Quiz Mode - you typed {})'.format(c)
        correctWord = ' - The current word is: {}'.format(word)
        correctMsg = ' - Correct!'
        buffer = '          '

        # only show # of words specified by buffer size due to limited screen space
        phrase = ' '.join(txtList[start:count + 1])
        count = count + 1

        win.clear()
        win.addstr(0, 0, phrase + buffer)
        win.addstr(4, 0, keyPress + correctWord + correctMsg + buffer)
        win.addstr(6, 0, '')
        win.refresh()
    else:
        keyPress = 'Quiz Mode - you typed {})'.format(c)
        correctWord = ' - The current word is: {}'.format(word)
        incorrectMsg = ' - Incorrect'
        buffer = '          '

        # only show # of words specified by buffer size due to limited screen space
        phrase = ' '.join(txtList[start:count + 1])
        count = count + 1

        win.clear()
        win.addstr(0, 0, phrase + buffer)
        win.addstr(4, 0, keyPress + correctWord + incorrectMsg + buffer)
        win.addstr(6, 0, '')
        win.refresh()

    if count == numWords:
        keyPress = 'Quiz Mode Complete!'
        buffer = '          '

        win.clear()
        win.addstr(0, 0, keyPress + buffer)
        win.refresh()
        break

time.sleep(2)
# curses.echo()

# required to prevent Linux terminal from hanging after app completion
curses.endwin()

print("Rows:    %d" % num_rows)
print("Columns: %d" % num_cols)
