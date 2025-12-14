
import random
import string
import os 
from datetime import datetime
import base64, sys



def generate_password(
    length: int,
    chose_lower: bool,
    chose_upper: bool,
    chose_digits: bool,
    chose_symbols: bool,
    pronounceable: bool,
    ) -> str:


    lower_case = string.ascii_lowercase
    upper_case = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%&_?"
    #print(lower_case[:10])
    AMBIGUOUS = set[str]("lI10O") # optional to exclude similar-looking chars
    
    password_chars = ""
    password_length = length

    chars_in_password = [] #list used to determine the strength of the password
    if chose_upper:
        password_chars += upper_case
        chars_in_password.append("uc")
    if chose_lower:
        password_chars += lower_case
        chars_in_password.append("lc")
    if chose_digits:
        password_chars += digits
        chars_in_password.append("di")
    if chose_symbols:
        password_chars += symbols
        chars_in_password.append("sy")


    clean_password_chars = ""
    for ch in password_chars:
        if ch not in AMBIGUOUS:
            clean_password_chars += ch
    #print(clean_password_chars)
    def regular_pass(clean_password_chars, password_length):
        password = []
        if chose_lower:
            password.append(random.choice(lower_case))
        if chose_upper:
            password.append(random.choice(upper_case))
        if chose_digits:
            password.append(random.choice(digits))
        if chose_symbols:
            password.append(random.choice(symbols))
        while len(password) < password_length:
            password.append(random.choice(clean_password_chars))
            
        random.shuffle(password) 
        password = "".join(password)
        return password

    def pronounceble_pass(clean_password_chars, password_length):
        password = []
        consonants = ""
        vowels = "aeiouAEIOU"
        for ch in clean_password_chars:
            if ch not in vowels:
                consonants += ch

        if chose_lower:
            password.append(random.choice(consonants.lower()))
            password.append(random.choice(vowels.lower()))
        if chose_upper:
            password.append(random.choice(consonants.upper()))
            password.append(random.choice(vowels.upper()))
        if chose_digits:
            password.append(random.choice(digits))
            #password.append(random.choice(vowels))
        if chose_symbols:
            password.append(random.choice(symbols))
            #password.append(random.choice(vowels))
        while len(password) < password_length:
            if len(password) + 1 < password_length and chose_upper:
                #if chose_upper and len(password) < password_length:
                password.append(random.choice(clean_password_chars))
                vowels_no_o = vowels.replace("o", "")
                password.append(random.choice(vowels_no_o.upper()))
            elif chose_lower and len(password) + 1 < password_length:
                password.append(random.choice(clean_password_chars))
                password.append(random.choice(vowels.lower()))
            else:
                if chose_upper and len(password) < password_length:
                    password.append(random.choice(upper_case))
                if chose_lower and len(password) < password_length:
                    password.append(random.choice(lower_case))    
        password = "".join(password)
        return password

    def reg_pron(clean_password_chars, password_length):
        regular_pronounceble = pronounceable
        if regular_pronounceble:
            return pronounceble_pass(clean_password_chars, password_length)
        
        else:
            return regular_pass(clean_password_chars, password_length)


    password = reg_pron(clean_password_chars, password_length)
    
      
    
    return password