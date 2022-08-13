import os
from lib import work

class Menu:
    
    def __check_files(self):
        if not os.path.isdir('db'):
            os.mkdir('db')
    
    def __init__(self):
        self.__check_files()
        self.menu()
    
    def db_list(self):
        db_files = os.listdir('db')
        db_files = [x for x in db_files if '.db' in x]
        return db_files
    
    def create_new(self):
        name = input("Please enter your new box name : ")
        open('db/' + name + '.db', 'w').close()
        self.menu()
    
    def print_menu(self, msg):
        print(20*'-')
        user = input(msg)
        return user
    
    def menu(self):
        while True:
            db_files = self.db_list()
            if len(db_files) == 0:
                user = self.print_menu("You dont't have any box.Please create new.\n1-Create new box\n2-Exit\n")
                if user in ['1', '2']:
                    if user == '1':
                        self.create_new()
                    else:
                        break
                else:
                    print('I did not understand what you said.Please try again.')
            else:
                user = self.print_menu("Please choose one :\n1-Review boxes\n2-Create new box\n3-Exit\n")
                if user in ['1', '2', '3']:
                    if user == '1':
                        msg = ''
                        for i, name in enumerate(db_files):
                            msg += str(i+1) + '-' + name.replace('.db', '') + '\n'
                        box = self.print_menu('Please choose your box for review :\n' + msg)
                        self.work = work.Work(db_files[int(box) - 1])
                    elif user == '2':
                        self.create_new()
                    else:
                        break
                else:
                    print('I did not understand what you said.Please try again.')
                