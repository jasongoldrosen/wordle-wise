# wordle-wise
## Background
As of writing this on January 2022, [Wordle](https://www.powerlanguage.co.uk/wordle/) is an extremely popular daiy word game puzzle. 

It has been discussed in the [NYTimes](https://www.nytimes.com/2022/01/03/technology/wordle-word-game-creator.html), the [Washington Post](https://www.washingtonpost.com/lifestyle/2022/01/13/wordle-word-game-pandemic/), and elsewhere. I learned about it through Twitter where it has been a huge topic of coverstaion on my newsfeed. My friends send each other their daily scores in group chats. 

Who knows how long the buzz will last? But, while the game is top of mind, I wanted to create a simple project that takes your Wordle game and returns a list of the most probable solutions given what you know and do not know about it. The underlying dataset I use is from the Google Web Trillion Word Corpus and accessed via [Kaggle](https://www.kaggle.com/rtatman/english-word-frequency).

**Tasks Completed**
- Write script that can reliably solve Wordle puzzles on hard mode

**Next Steps**
- Estimate how often Wordle will correctly get answer and estimate distribution of how many guesses are required
- Allow for different strategies (e.g., choosing words with different letters to minimize the set of possible solutions)
- Study which strategies and combninations for strategies

## wordle-wise in action 
Puzzle from 2022-01-18 

```python
from wordle_wise.api import WordleGame

puzzle = WordleGame()
puzzle.summary()

# Guess 1
puzzle.make_guess(guess='ABOUT', result='__G__')
puzzle.summary()

# Guess 2
puzzle.make_guess(guess='PHONE', result='G_G__')
puzzle.summary()

# Guess 3
puzzle.make_guess(guess='PROOF', result='GGG__')
puzzle.summary()

# Guess 4 (winning guess)
puzzle.make_guess(guess='PROXY', result='GGGGG') 
puzzle.summary()
```

### Top words before any guesses
![image](https://user-images.githubusercontent.com/36316312/150012780-e28552e0-6e33-4bae-a9fc-854d75006882.png)

### Top words after guessing "ABOUT"

![image](https://user-images.githubusercontent.com/36316312/150012863-69f37b0a-bf39-4695-83b8-4d79d5b7a2cc.png)

### Top words after guessing "PHONE"

![image](https://user-images.githubusercontent.com/36316312/150012945-1cdfaa55-3a9c-478e-8ad7-2fe1512e90e8.png)

### Top words after guessing "PROOF"

![image](https://user-images.githubusercontent.com/36316312/150012989-fa9e455b-d936-4bb8-8ba7-ca39df59f185.png)

### PUZZLE SOLVED with "PROXY"
Result: solved in 4 guesses on "Hard Mode"

<img width="519" alt="image" src="https://user-images.githubusercontent.com/36316312/150011298-332baa4a-b992-4ea4-a958-f9ed5347d22b.png">


