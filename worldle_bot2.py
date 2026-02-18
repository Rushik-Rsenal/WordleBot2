# General Principle:
# Find the entropy of all words
# Determine the word with the highest info gain
# Filter the words out
# Repeat

# Get all 5 lett\\\er words
# from itertools import product
import math

# five_letter_words = []
# with open("word_list_short.txt", "r") as f:
#     for line in f.readlines():
#         five_letter_words.append(line[0:5])

# # Possible permuations
# states = [0, 1, 2]

# # Generate all 5-digit combinations
# # Repeat=5 means we want 5 slots
# # 0 = Gray, 1 = Yellow, 2 = Green
# all_patterns = list(product(states, repeat=5))




def get_words_with_correct_letter(word_list, word_pattern, word):
    CORRECT = 2
    PARTIALLY_CORRECT = 1
    EXCLUDE = 0
    WORD_LEN = 5
    # First get the indexes of correctly guessed letters
    correct_letter_indexes = []
    for index in range(WORD_LEN):
        if int(word_pattern[index]) == CORRECT:
            correct_letter_indexes.append(index)

    # Next include words with a particular letter. Do this letter by letter.
    words_with_correct_letters = []
    
    # For each word in word list, if the word does not have correct letters, we don't append to list
    for w in word_list:
        contains_correct_letters = True
        for index in correct_letter_indexes:
            if w[index] != word[index]:
                contains_correct_letters = False
                break
        
        # If the word contains correct letters, append to list
        if contains_correct_letters:
            words_with_correct_letters.append(w)

    # Return list
    return list(words_with_correct_letters)


# Letter does exist in the word
# Letter is not at the specific position

def get_words_with_partially_correct_letters(word_list, word_pattern, word):
    CORRECT = 2
    PARTIALLY_CORRECT = 1
    EXCLUDE = 0
    WORD_LEN = 5

    # First get the indexes of partially correct letters

    partially_correct_letter_indexes = []
    for index in range(WORD_LEN):
        if int(word_pattern[index]) == PARTIALLY_CORRECT:
            partially_correct_letter_indexes.append(index)

    # First get the words that don't have the letter in that position
    good_words = []
    for w in word_list:
        does_not_have_letter_in_pos = True

        for index in partially_correct_letter_indexes:
            does_not_have_letter_in_pos = True
            if w[index] == word[index]:
                does_not_have_letter_in_pos = False
                break
        if does_not_have_letter_in_pos:
            good_words.append(w)


    # Now check if the letter exists in the word
    temp = []
    letterInWord = True
    for w in good_words:
        for index in partially_correct_letter_indexes:
            letterInWord = True
            chosenLetter = word[index]
            if chosenLetter not in w:
                letterInWord = False
                break

        if letterInWord:
            temp.append(w)


    good_words = temp
    return good_words


def get_words_after_excluding_letters(word_list, pattern, word):
    CORRECT = 2
    PARTIALLY_CORRECT = 1
    EXCLUDE = 0
    WORD_LEN = 5
    
    # First we get letters that are correct, partially correct and need to be excluded
    # If the letter to be excluded is not anywhere in correct or partially correct list, we can add it to a set
    correct_letters = []
    partially_correct_letters = []
    exclude_letters = []
    exclude_indexes =[]

    filtered_list = []

    for i in range(WORD_LEN):
        if int(pattern[i]) == CORRECT:
            correct_letters.append(word[i])
        elif int(pattern[i]) == PARTIALLY_CORRECT:
            partially_correct_letters.append(word[i])
        elif int(pattern[i]) == EXCLUDE:
            exclude_indexes.append(i)
            exclude_letters.append(word[i])

    filtered_exclude_list = []

    letter_excluded = True
    


    # We only have exclude letters
    for letter in exclude_letters:
        if (letter not in correct_letters) and (letter not in partially_correct_letters):
            filtered_exclude_list.append(letter)

    
   
    doesNotInclude = True
    for w in word_list:
        letter_excluded = True
        for index in exclude_indexes:
            if (w[index] == word[index]):
                letter_excluded = False
                break
        if letter_excluded == False:
            continue

        for letter in filtered_exclude_list:
            doesNotInclude = True
            if letter in w:
                doesNotInclude = False
                break
        if doesNotInclude:
            filtered_list.append(w)
    return filtered_list

def filter_words(word_list, pattern, word):
    # Get words with the correct letter position
    filtered_words = get_words_with_correct_letter(word_list, pattern, word)
    
    # Get words that are partially correct
    filtered_words1 = get_words_with_partially_correct_letters(filtered_words, pattern, word)

    # Exclude words with paritcular letter(s)
    filtered_words2 = get_words_after_excluding_letters(filtered_words1, pattern, word)

    return filtered_words2



# Takes in a list of words, calculates information gain for each word, returns a list of possible words, along with the expected infogain
def calculate_info_gain(word_list, all_patterns): 
    return_list = []
    word_list_len = len(word_list)

    # for every word in word_list, calculate the expected information gain for each pattern. 
    total_entropy = 0
    for word in word_list:
        entropy_list = []
        for pattern in all_patterns:
            filtered_words = word_list
                
            filtered_words = filter_words(filtered_words, pattern, word)
                
            # Calculate infogain
            probability = len(filtered_words)/ word_list_len

            if probability != 0:
                info_gain = math.log2(1/ probability)
                info_gain = info_gain * probability 
                entropy_list.append(info_gain)

        # Expected info gain
        total_entropy = sum(entropy_list)
        return_object = {
            "word": word,
            "expected_information": total_entropy
        }

        return_list.append(return_object)

    return return_list
    


# # # Guess CRANE
# filtered_list = five_letter_words
# # print("Enter CRANE as a first guess")
# guess = input("Enter the first guess: ")
# pattern = input("Enter the pattern: ")


# # For yyour next guess:
# print("For your next guess: ")
# info_list = calculate_info_gain(new_list)
# temp = info_list
# info_list = sorted(temp, key=lambda x: x['expected_information'])
# print(info_list[-1])
# print(info_list[-2])

# ------------------------ Main Loop -----------------------------
# pattern = "0"
# guess_count = 1
# new_list = five_letter_words
# while pattern != "22222" and guess_count < 7:
#     guess  = input("Enter a guess: ")
#     pattern = input("Enter the pattern: ")
    
#     new_list = filter_words(new_list, pattern, guess)
#     info_list = calculate_info_gain(new_list)

#     print("For your next guess")
#     temp = info_list
#     info_list = sorted(temp, key=lambda x: x['expected_information'], reverse=False)

#     if len(info_list) > 5:
#         print(info_list[-1])
#         print(info_list[-2])
#         print(info_list[-3])
#         print(info_list[-4])
#         print(info_list[-5])
#     elif len(info_list) >= 1:
#         print(info_list)
        
#     guess_count += 1
    
# if guess_count == 7:
#     print("Bruh you lost even with a bot.")
# else:
#     print("Nice You Won!")
# -----------------------------------------------------------------

# updated_list = five_letter_words
# def solver(guess, pattern, word_list, info_list):
#     # global updated_list
#     my_list = filter_words(word_list, pattern, guess)
#     info_list = calculate_info_gain(word_list)

#     temp = info_list
#     info_list = sorted(temp, key=lambda x: x['expected_information'], reverse=False)
#     updated_list = my_list
    
#     return info_list[-1]

