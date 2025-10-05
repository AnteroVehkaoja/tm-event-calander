import db

def add_tournament(title,descr,host_id,qualifier,whenevent):
    sql = "INSERT INTO tournaments(title,description_of_event,host_id,qualifier,whenevent) VALUES (?,?,?,?,?)"
    db.execute(sql,[title,descr,host_id,qualifier,whenevent])


def get_tournaments():
    sql = "SELECT id,title,description_of_event,host_id,whenevent FROM tournaments ORDER BY whenevent DESC "
    result = db.query(sql)
    return result if result else []


def get_tournament(tournament_id):
    sql = "SELECT id,title,description_of_event,host_id,qualifier,whenevent FROM tournaments WHERE id = ?"
    result = db.query(sql,[tournament_id])
    return result if result else None

def delete_user_tourenaments(username):
    sql = "DELETE FROM tournaments WHERE host_id = ?"
    db.execute(sql, [username])

def update_tournament(title,descr,qualifier,whenevent,tournament_id):
    sql = "UPDATE tournaments SET title = ?,description_of_event = ?,qualifier = ?,whenevent = ? WHERE id = ?"
    db.execute(sql,[title,descr,qualifier,whenevent,tournament_id])