import db



def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])
    return result[0] if result else None

def get_tournaments_person(username):
    sql = "SELECT id,title,description_of_event,qualifier,whenevent FROM tournaments WHERE host_id = ?"
    result = db.query(sql, [username])
    return result if result else None

def search(query):
    sql ="""SELECT id,title,description_of_event,host_id,whenevent,qualifier FROM tournaments WHERE title LIKE ?"""
    return db.query(sql, ["%" + query +"%"])

def user_register_count(user_id):
    print(user_id)
    sql = """SELECT *  FROM registrations WHERE user_id = ? """
    result = db.query(sql,[user_id])
    print(result)
    return len(result) if result else 0