import sqlite3

class DbOperator():
    connection = sqlite3.connect('subs.db')
    cursor = connection.cursor()
    query = 'select sqlite_version();'
    cursor.execute(query)
    log_file = "logs.txt"
    result = cursor.fetchall()
    hash_dict = {}
    print("SQLite initiliazed. Version is : {}".format(result))

    table = ''' CREATE TABLE IF NOT EXISTS subs(
                    id INTEGER PRIMARY KEY ,
                    chat_id varchar(30) NOT NULL,
                    user_id varchar(30) NOT NULL,
                    username varchar(50) NOT NULL,
                    menu_sub BOOLEAN DEFAULT FALSE,
                    sub_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_staff BOOLEAN DEFAULT FALSE
                    );
                    '''
    cursor.execute(table)
    connection.commit()

    def save_log(self,text):
        with open("{}".format(self.log_file), "a") as file:
                    file.write(f"\n{text}")
        print(f"LOG FILE INFO : {text}")


    
    def dict_ekle(self,hash1,text):
        self.hash_dict[hash1] = text
    def dict_cek(self,hash):
        toreturn = self.hash_dict.get(hash)
        self.hash_dict.clear()
        return toreturn

     def addSub(self,sender):
            username = sender.username
            chat_id = sender.id
            if not username:
                username = "Unknown"
            userId = sender.id
            cursor = self.cursor
            current_subs = self.getSubs()
            print(current_subs)
            check = self.checkSub(userId)
            if check:
                return False
            else:
                if current_subs:
                    execute = f'''INSERT INTO subs (chat_id, user_id, username) VALUES ('{chat_id}','{userId}','{username}')'''
                else:
                    execute = f'''INSERT INTO subs (chat_id, user_id, username, is_staff) VALUES ('{chat_id}','{userId}','{username}',TRUE)'''
    
    
            cursor.execute(execute)
            self.connection.commit()
            return True
    
            cursor.execute(execute)
            self.connection.commit()
            return True
        
        def deleteSub(self,sender):
            cursor = self.cursor
            userId = sender.id
            check = self.checkSub(userId)
            if check:
                statement = '''DELETE FROM subs WHERE user_id = ?'''
                cursor.execute(statement, (userId,))
                self.connection.commit()
                return True
            else:
                return False
    def checkSub(self,userid):
        cursor = self.cursor
        statement = '''SELECT username FROM subs WHERE user_id = ?'''
        cursor.execute(statement,(userid,))
        output = cursor.fetchone()
        if output:
            return True
        else:
            return False
    def checkMenuSub(self,userid):
        cursor = self.cursor
        statement = '''SELECT menu_sub FROM subs WHERE user_id = ?'''
        cursor.execute(statement,(userid,))
        output = cursor.fetchone()[0]
        if output == 1:
            return True
        else:
            return False
    def getSubs(self):
        cursor = self.cursor
        subs_id = []
        statement = '''SELECT user_id FROM subs'''
        cursor.execute(statement)
        output = cursor.fetchall()
        if output:
            for row in output:
                subs_id.append(row[0])
        return subs_id
    def getMenuSubs(self):
        cursor = self.cursor
        subs_id = []
        statement = '''SELECT user_id FROM subs WHERE menu_sub = TRUE'''
        cursor.execute(statement)
        output = cursor.fetchall()
        if output:
            for row in output:
                subs_id.append(row[0])
        return subs_id
    def getAdmins(self):
        cursor = self.cursor
        admins_id = []
        statement = '''SELECT user_id FROM subs WHERE is_staff = TRUE'''
        cursor.execute(statement)
        output = cursor.fetchall()
        if output:
            for row in output:
                admins_id.append(row[0])
        return admins_id
    
    def addStaff(self,arg_id):
        cursor = self.cursor
        check= self.checkSub(arg_id)
        if check:
            checkStaff = self.checkStaff(arg_id) 
            if checkStaff == 1:
                return "Kullanici zaten admin.",False  
            statement = '''UPDATE subs SET is_staff = TRUE WHERE user_id = ?;'''
            cursor.execute(statement,(arg_id,))
            self.connection.commit()
            return f"{arg_id} kodlu kullanici basariyla admin yapildi.",True
        else:      
            return "Kullanici abone degil ya da kullanici idsi yanlış.",False

    def addMenuSub(self,userid):
        cursor = self.cursor
        if self.checkMenuSub(userid=userid):
            return False
        try:
            statement = '''UPDATE subs SET menu_sub = TRUE where user_id = ?'''
            cursor.execute(statement,(userid,))
            self.connection.commit()
            return True
        except:
            return False
    def leaveMenuSub(self,userid):
        cursor = self.cursor
        if not self.checkMenuSub(userid=userid):
            return False
        try:
            statement = '''UPDATE subs SET menu_sub = FALSE where user_id = ?'''
            cursor.execute(statement,(userid,))
            self.connection.commit()
            return True
        except:
            return False
    
    def deleteStaff(self,arg_id):
        cursor = self.cursor
        check= self.checkSub(arg_id)
        if check:
            check = self.checkStaff(arg_id) 
            if check == 0:
                return "Kullanici admin değil.",False  
            statement = '''UPDATE subs SET is_staff = FALSE WHERE user_id = ?;'''
            cursor.execute(statement,(arg_id,))
            self.connection.commit()
            return f"{arg_id} kodlu kullanicinin adminliği alındı.",True
        else:      
            return "Kullanici abone degil ya da kullanici adı yanlış.",False

    def checkStaff(self,user_id):
        cursor = self.cursor
        if self.checkSub(user_id):
            statement = '''SELECT is_staff FROM subs WHERE user_id = ?'''
            cursor.execute(statement,(user_id,))
            output = cursor.fetchone()[0]
            return output
        return 2

    def getId(self,username):
        cursor = self.cursor
        statement = '''SELECT user_id FROM subs WHERE username = ?'''
        cursor.execute(statement,(username,))
        return cursor.fetchone()





