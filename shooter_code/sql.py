from sqlite3 import *

file = connect("data/data.db")
cs = file.cursor()
cs.execute(
    "CREATE TABLE IF NOT EXISTS shooters (shooter_id STRING NOT NULL PRIMARY KEY, name STRING, speed INTEGER, "
    "lasersights BOOLEAN, "
    "recharge_speed STRING, u_recharge_speed INTEGER, penetration STRING, u_penetration INTEGER, "
    "drop_off STRING, u_drop_off INTEGER, p_lasersights STRING, p_recharge_speed STRING, p_penetration STRING, p_drop_off STRING, owned BOOLEAN)")


def insert_shooter(*data):
    cs.execute(f"INSERT INTO shooters(shooter_id, name, speed, lasersights, recharge_speed, u_recharge_speed, penetration, "
               f"u_penetration, drop_off, u_drop_off, p_lasersights, p_recharge_speed, p_penetration, p_drop_off, owned) values('{data[0]}', '{data[1]}', {data[2]}, {data[3]}, '{data[4]}', {data[5]}, "
               f"'{data[6]}', {data[7]}, '{data[8]}', {data[9]}, '{data[10]}', '{data[11]}', '{data[12]}', '{data[13]}', {data[14]})")


insert_shooter('basic', 'basic shooter', 7, False, '_70|65|60|55', 0, '_0|25|50', 0, '_100|40', 0, '_80', '_100|200|350', '_50|100', '_110', True)
insert_shooter('sniper', 'sniper', 10, False, '_100|85|70', 0, '_50|75|100', 0, '_20|10|0', 0, '_20', '_50|260', '_150|200', '_80|90', True)
insert_shooter('rapid', 'rapid fire shooter', 5, False, '_30|25|20', 0, '_0|5|10', 0, '_10', 0, '_320', '_150|300|450', '_250|300', '_', False)
insert_shooter('machine', 'super fast shooter', 7, False, '_15|7|4', 0, '_0|10|15', 0, '_0', 0, '_600', '_300|400|500', '_120|120', '_', False)
# insert_shooter('god', 'god shooter', 13, False, '_1', 0, '_100', 0, '_20', 0)

cs.execute(
    "CREATE TABLE IF NOT EXISTS user(name STRING NOT NULL PRIMARY KEY, start_health INTEGER, high_score INTEGER, "
    "tokens INTEGER, current_shooter STRING, test_setting BOOLEAN)")

cs.execute("INSERT INTO user(name, start_health, high_score, tokens, current_shooter, test_setting) "
           "values('AAA', 1, 0, 1000, 'basic', FALSE)")

file.commit()
file.close()
