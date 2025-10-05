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
    sql = "SELECT title,description_of_event,qualifier,whenevent,id FROM tournaments WHERE host_id = ?"
    result = db.query(sql, [username])
    return result if result else None