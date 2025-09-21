import db

def add_tournament(title,descr,host_id,qualifier,whenevent):
    sql = "INSERT INTO tournaments(title,description_of_event,host_id,qualifier,whenevent) VALUES (?,?,?,?,?)"
    db.execute(sql,[title,descr,host_id,qualifier,whenevent])


def get_tournaments():
    sql = "SELECT title,description_of_event,host_id,whenevent FROM tournaments ORDER BY whenevent DESC "
    return db.query(sql)

def delete_user_tourenaments(username):
    sql = "DELETE FROM tournaments WHERE host_id = ?"
    db.execute(sql, [username])