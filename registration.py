import db

def add_registration(tournament_id,user_id,):
    sql = "INSERT INTO registrations(tournament_id,user_id) VALUES (?,?)"
    db.execute(sql,[tournament_id,user_id])
    
def registered_people(tournament_id):
    sql = "SELECT user_id FROM registrations WHERE tournament_id = ?"
    result = db.query(sql,[tournament_id])
    return result if result else []

def del_registration(tournament_id, user_id):
    sql = "DELETE FROM registrations WHERE tournament_id = ? AND user_id = ?"
    db.execute(sql,[tournament_id,user_id])

def del_all_reg(tournament_id):
    sql = "DELETE FROM registrations WHERE tournament_id = ?"
    db.execute(sql,[tournament_id])