import pandas as pd
WORD_COLUMN = 'word'
FREQ_COLUMN = 'count'
ignore_characters = ['_', '', ' ']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','x','z']

def normalize(x):
    # Normalize so sum adds to 1
    return x / x.sum()

def get_wordle_candidates(
    word_bank,
    known_positions, 
    include_list, 
    exclude_list):

    # Make sure include_list contains all letters in known_positions
    include_list += [x for x in known_positions if x not in include_list and x not in ignore_characters]
    
    # Filter to words that contain specific letter from include_list
    for letter in include_list:
        conds = word_bank[WORD_COLUMN].str.contains(letter)
        word_bank = word_bank[conds]

    # Filter to words that DO NOT contain letter from exclude_list
    for letter in exclude_list:
            conds = word_bank[WORD_COLUMN].str.contains(letter)
            word_bank = word_bank[~conds]

    # Filter to words that contain specific letter in known position
    for pos, letter in enumerate(known_positions):
        if letter in ignore_characters:
            continue
        
        conds = word_bank[WORD_COLUMN].str[pos] == letter
        word_bank = word_bank[conds]

    # Normalize so sum adds to 1
    word_bank[FREQ_COLUMN] = normalize(word_bank[FREQ_COLUMN])
    word_bank.sort_values(FREQ_COLUMN,ascending=False,inplace=True)
        
    return word_bank

def get_wordle_word_bank(df, nletters=5):
    # Five letter words
    eligible_conds = (df[WORD_COLUMN].str.len() == nletters)
    df = df[eligible_conds]
    df[WORD_COLUMN] = df[WORD_COLUMN].str.upper()
    return df

def count_words_containing_letters(word_bank, letters):
    count_dict = {}
    for letter in letters:
        count_dict[letter] = word_bank[WORD_COLUMN].str.contains(letter).sum()
    return count_dict

def interpret_results(guess, result):
    include_list = [g for g,r in zip(guess, result) if r.upper() in ['Y','G']]
    exclude_list = [g for g,r in zip(guess, result) if r.upper() not in ['Y','G']]
    known_positions = {i:guess[i] for i,r in enumerate(result) if r.upper() == 'G'}
    return include_list, exclude_list, known_positions

class WordleGame:

    def __init__(self, word_length:int=5, rounds:int=6):
        self.rounds = rounds
        self.remaining_guesses = rounds
        self.known_positions = [x for x in ('_' * word_length)]
        self.include_list = []
        self.exclude_list = []
        self.most_probable_words = get_wordle_word_bank(pd.read_csv('data/unigram_freq.csv'))
        self.total_words = self.most_probable_words.shape[0]
        self.remaining_words = self.total_words
        self.scoreboard = []

    def make_guess(self, guess:str, result:str):
        if self.remaining_guesses == 0:
            raise ValueError("No more remaining guesses")
        else: 
            self.remaining_guesses -= 1

        # Make sure to use upper case words
        if guess != guess.upper():
            guess = guess.upper()

        if result != result.upper():
            result = result.upper()
  
        include_list, exclude_list, known_positions = interpret_results(guess, result)

        # Add net new included letters
        self.include_list += [x for x in include_list if x not in self.include_list]

        # Add net new excluded letters
        # Double-counted letters can show as both included (green or yellow) and excluded (black) e.g. the 2nd o in ('proof','ggg___') 
        self.exclude_list += [x for x in exclude_list if x not in self.exclude_list and x not in self.include_list]
        for idx,letter in known_positions.items():
            self.known_positions[idx] = letter

        # Update probable list of words
        self.most_probable_words = get_wordle_candidates(
            word_bank=self.most_probable_words,
            known_positions=self.known_positions, 
            include_list=self.include_list, 
            exclude_list=self.exclude_list)

        self.remaining_words = self.most_probable_words.shape[0]

        self.scoreboard += [guess]

        return None

    # def _interpret_results(self, guess, result):
    #     include_list = [g for g,r in zip(guess, result) if r.lower() in ['y','g']]
    #     exclude_list = [g for g,r in zip(guess, result) if r.lower() not in ['y','g']]
    #     known_positions = {i:guess[i] for i,r in enumerate(result) if r.lower() == 'g'}
    #     return include_list, exclude_list, known_positions

    def summary(self, candidatewords=5):
        print("----------- GAME SUMMARY -----------")
        print(f"Remaining Guesses: {self.remaining_guesses}")
        print(f"Word includes: {self.include_list}")
        print(f"Word excludes: {self.exclude_list}")
        print(f"Known positions: {self.known_positions}")
        print(f"Count of remaining words: {self.remaining_words} or {100 * self.remaining_words / self.total_words :.1f}%")
        print(f"\nMost Probable Words: \n {self.most_probable_words.head(candidatewords)}")
        print(f"Scoreboard")
        for x in self.scoreboard:
            print(x)
        return None
