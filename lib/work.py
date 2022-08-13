import pyttsx3
import eng_to_ipa as ipa

from lib import db

class Work:
    
    def prounance_word(self, word):
        self.read_engine.say(word)
        self.read_engine.runAndWait()
    
    def phonetic_word(self, word):
        phonetic = ipa.convert(text=word, retrieve_all=True)
        return phonetic
       
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = db.DB(db_name)
        self.words = {}
        self.capacity = 20
        self.read_db()
        self.read_engine = pyttsx3.init()
        self.menu()
    
    def read_db(self):
        self.words = self.db.read_all()
        
    def print_menu(self, msg):
        print(20*'-')
        user = input(msg)
        return user

    def add_new_word(self):
        if len(self.words['1']['1']) >= self.capacity:
            print("That's enough for today.")
        else:
            word = input('Please enter the word : ')
            mean = input('Please enter the meaning : ')
            self.db.add_new([word, mean])
            self.read_db()
    
    def review(self):
        for key in ['5', '4', '3', '2', '1']:
            in_key = str(2**(int(key) - 1))
            if key in self.words.keys() and in_key in self.words[key].keys():
                if len(self.words[key][in_key]) != 0:
                    for i in range(len(self.words[key][in_key])):
                        flag = False
                        flag_answer = False
                        while not flag:
                            id = self.words[key][in_key][i][0]
                            word = self.words[key][in_key][i][1]
                            mean = self.words[key][in_key][i][2]
                            header = 'You are in ' + self.db_name.replace('.db', '') + '.Please choose one of these :\n'
                            if flag_answer:
                                print_word = '###\n' + word + '\n' + str(self.phonetic_word(word)) + '\n###\n' + 'The answer is : ' + mean + '\n'
                            else:
                                print_word = '###\n' + word + '\n' + str(self.phonetic_word(word)) + '\n###\n'
                            user = self.print_menu(header + print_word +  '1-Show the answer\n2-Pronounce the word\n3-Back\nDid you answer correct?[Y/N]')
                            if user in ['1', '2', '3', 'y', 'Y', 'n', 'N']:
                                if user == 'y' or user == 'Y':
                                    self.db.update_one(key, id)
                                    flag = True
                                elif user == 'n' or user == 'N':
                                    self.db.update_back(id)
                                    flag = True
                                elif user == '1':
                                    flag_answer = True
                                elif user == '2':
                                    self.prounance_word('word')
                                else:
                                    flag = True
                            else:
                                print('I did not understand what you said.Please try again.')
                    else:
                        self.db.update_all(key)
                else:
                    if key == '1':
                        print('Done! Please add some cards.')
                        break
            else:
                pass 
    
    def menu(self):
        while True:
            header = 'You are in ' + self.db_name.replace('.db', '') + '.Please choose one of these :\n'
            user = self.print_menu(header + '1-Reviewing this session words\n2-Add new word\n3-Back\n')
            if user in ['1', '2', '3']:
                if user == '1':
                    self.review()
                elif user == '2':
                    self.add_new_word()
                else:
                    break
            else:
                print('I did not understand what you said.Please try again.')