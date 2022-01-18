from wordle_wise.api import WordleGame

x = WordleGame()
x.summary()

x.make_guess(guess='ABOUT', result='__G__')
x.summary()

x.make_guess(guess='phone', result='g_g__')
x.summary()

x.make_guess(guess='proof', result='ggg__') #Instead of yellow this came back as black and that threw off the algo
x.summary()

x.make_guess(guess='proxy', result='ggggg') 
x.summary()
