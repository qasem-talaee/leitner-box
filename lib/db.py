import sqlite3

class DB:
    
    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word CHAR(50),
                mean CHAR(1000),
                pos INTEGER,
                in_pos INTEGER
                );'''
        self.conn.execute(query)
        
    def __init__(self, db):
        self.path = 'db/' + db
        self.conn = sqlite3.connect(self.path)
        self.create_table()
        
    def read_all(self):
        query = "SELECT * FROM words"
        cursor = self.conn.execute(query)
        results = cursor.fetchall()
        out = {}
        for result in results:
            pos_key = str(result[3])
            if not pos_key in out.keys():
                out[pos_key] = {}
            in_pos_key = str(result[4])
            if not in_pos_key in out[pos_key].keys():
                out[pos_key][in_pos_key] = []
            out[pos_key][in_pos_key].append([result[0], result[1], result[2]])
        cursor.close()
        return out
    
    def add_new(self, data):
        query = "SELECT * FROM words WHERE word LIKE ?;"
        data_exsit = (f'%{data[0]}%',)
        cursor = self.conn.cursor()
        cursor.execute(query, data_exsit)
        if len(cursor.fetchall()) == 0:
            cursor.close()
            query = "INSERT INTO words (word,mean,pos,in_pos) VALUES (?,?,?,?);"
            data = (data[0], data[1], 1, 1)
            cursor = self.conn.cursor()
            cursor.execute(query, data)
            self.conn.commit()
            cursor.close()
            print('The word added successfully.')
        else:
            print('The word was exist.')
    
    def update_back(self, id):
        query = "UPDATE words SET pos=?,in_pos=? WHERE id=?;"
        data = (1, 1, id)
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()
        cursor.close()
        
    def update_one(self, key, id):
        query = "UPDATE words SET pos=?,in_pos=? WHERE id=?;"
        data = (int(key) + 1, 1, id)
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        self.conn.commit()
        cursor.close()
        
    def update_all(self, key):
        key = int(key)
        query = "SELECT * FROM words WHERE pos=? AND in_pos<>?;"
        data = (key, 2**(key - 1))
        cursor = self.conn.cursor()
        cursor.execute(query, data)
        results = cursor.fetchall()
        if len(results) != 0:
            for result in results:
                id = result[0]
                in_pos = result[4]
                query = "UPDATE words SET in_pos=? WHERE id=?;"
                data = (int(in_pos) + 1, id)
                cursor = self.conn.cursor()
                cursor.execute(query, data)
                self.conn.commit()