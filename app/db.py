import psycopg2
from flask.cli import with_appcontext
import click


def connect(db_name='levelup'):
    connection = psycopg2.connect(
        "dbname = {} user = postgres password = kukuer1210 host = localhost \
        port = 5432".format(db_name)
        )
    connection.autocommit = True
    return connection

cursor = connect().cursor()


def close(db_name='levelup', error=None):
    if connect():
        connect().close()


def cur(db_name='levelup'):
    cursor = connect(db_name='levelup').cursor()
    return cursor


def init_db():
    cur('postgres').execute('create database levelup')
    save('postgres')
    close('postgres')
    print('database creaed')
    create_humans = 'CREATE TABLE IF NOT EXISTS humans(\
            human_id SERIAL PRIMARY KEY NOT NULL, name varchar,\
            address VARCHAR NOT NULL, age INT NOT NULL,\
            single BOOLEAN\
            )'
    cursor.execute(create_humans)
    save()
    print('table humans created')
    create_simcard_table_query = 'CREATE TABLE IF NOT EXISTS simcard(\
            id SERIAL PRIMARY KEY NOT NULL, name  varchar NOT NULL,\
            phone_number INT UNIQUE NOT NULL, serial INT UNIQUE NOT NULL,\
            service_provider VARCHAR NOT NULL, human_id INT UNIQUE,\
            is_active BOOLEAN\
            )'
    cursor.execute(create_simcard_table_query)
    save()
    print('table simcards created')


def save(db_name='levelup'):
    connect(db_name).commit()


def init_app(app):
    app.teardown_appcontext(close)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def create(human):
    try:
        create_human_query = '''INSERT INTO humans (name, address, \
        age, single) VALUES (%s,%s,%s,%s)'''
        cursor.execute(
            create_human_query, (
                human.name, human.address,
                human.age, human.single
                ))
        save()
        print("human", human.__dict__, "saved to db")
    except (Exception, psycopg2.Error) as error:
        print("Failed to create human:", error)


def get_humans():
    cursor.execute("SELECT * FROM humans ORDER BY humanid DESC")
    men = cursor.fetchall()
    humans = [dict_human(human) for human in men]
    return humans


def fetch_human_name(name):
    cursor.execute((
        "SELECT * FROM humans WHERE name = %s"), (name,))
    human = cursor.fetchone()
    return dict_human(human)


def fetch_human(humanid):
    try:
        cursor.execute((
            "SELECT * FROM humans WHERE humanid = %s"), (humanid,))
        human = cursor.fetchone()
        print(dict_human(human))
        return human.__dict__
    except Exception as error:
        print(error)


def fetch_human_address(address):
    try:
        cursor.execute((
            "SELECT * FROM humans WHERE address = %s"), (address,))
        human = cursor.fetchone()
        print(dict_human(human))
        return dict_human(human)
    except Exception as error:
        print(error)


def edit_human(humanid, key, value):
    if key == 'name':
        sql_update_query = 'UPDATE humans SET name = %s WHERE humanid = %s'
    elif key == 'address':
        sql_update_query = 'UPDATE humans SET address = %s WHERE humanid = %s'
    elif key == 'age':
        sql_update_query = 'Update humans SET age = %s\
            WHERE humanid = %s'
    elif key == 'single':
        sql_update_query = 'Update humans SET singlr = %s\
            WHERE humanid = %s'
    else:
        res = f'human has no attribute {key}'
    try:
        cursor.execute(sql_update_query, (value, humanid))
        save()
        print('ok')
        res = '{} changed'.format(key)
    except (Exception, psycopg2.Error) as error:
        print(error)
        res = f"Error in update operation {error}"
    return res


def delete_human(humanid):
    human = fetch_human(humanid)
    if human:
        try:
            sql_delete_query = 'delete from humans WHERE humanid = %s'
            cursor.execute(sql_delete_query, (humanid,))
            save()
            res = 'human {} deleted'.format(human['name'])
        except (Exception, psycopg2.Error) as error:
            res = 'error deleting human {}'.format(human['name'])
            print("Error deleting", error)
    res = 'no human {}'.format(human['name'])
    print(res)
    return res


def dict_human(tup):
    human = {}
    keys = ['humanid', 'name', 'address', 'age', 'single']
    try:
        for key in keys:
            human[key] = tup[keys.index(key)]
        return human
    except Exception as e:
        print(e)


def to_object(dic):
    from .models import Human
    human = Human('', '', '')
    for key in dic.keys():
        if key in human.__dict__.keys():
            human.__setattr__(key, dic[key])
        human.humanid = dic['humanid']
    return human


def savesimcard(simcard):
        try:
            create_simcard_query = ' INSERT INTO simcards (humanid, name, phone_number,\
            serial, service_provider, is_active) VALUES\
            (%s,%s,%s, %s,%s, %s)'
            cursor.execute(
                create_simcard_query, (
                    simcard.humanid, simcard.name, simcard.phone_number,
                    simcard.serial, simcard.service_provider, simcard.is_active,
                    ))
            save()
            res = 'simcard registere'
        except (Exception, psycopg2.Error) as error:
            print(error)
            res = "Failed to create simcard"
        print(res)
        return res


# def update_simcard(input, id, key):
#     if input:
#         try:
#             if key == 'serial':
#                 sql_update_query = 'Update simcards SET serial = %s\
#                     WHERE parcelid = %s;'
#             elif key == 'is_active':
#                 sql_update_query = 'Update simcards SET is_active = %s\
#                     WHERE parcelid = %s;'
#             # elif key == 'cancel':
#             #     sql_update_query = 'Update simcards SET is_active = canceled\
#             #         WHERE parcelid = %s;'
#             else:
#                 key == 'location'
#                 sql_update_query = 'Update simcards SET current_location = %s\
#                     WHERE parcelid = %s; '
#
#             cursor.execute((sql_update_query), (input, id))
#             save()
#             print("success")
#             result = '{} updated to \'{}\''.format(key, input)
#         except (Exception, psycopg2.Error) as error:
#             print("Error in update operation", error)
#             result = ('update failed, contact levelup', 500)
#     else:
#         result = ('please fill in value for {}'.format(key), 400)
#     return result
#
#
# def delete_simcard(parcelid):
#     try:
#         sql_delete_query = 'delete from simcards WHERE parcelid = %s'
#         cursor.execute(sql_delete_query, (parcelid,))
#         save()
#         print("deleted")
#     except (Exception, psycopg2.Error) as error:
#         print("Error in delete operation", error)
#
#
# def get_simcards():
#     try:
#         cursor.execute("SELECT * FROM simcards simcard BY parcelid DESC")
#         save()
#         simcards = cursor.fetchall()
#         count = cursor.rowcount
#         print(count, "simcards fetched", simcards)
#         result = [dict_simcard(simcard) for simcard in simcards]
#     except (Exception, psycopg2.Error) as error:
#         print('problem in get simcards function', error)
#         result = ('an error occured, please contact support', 500)
#     except (Exception) as error:
#         print('error', error)
#         result = ('simcard not found', 404)
#     return result
#
#
# # def get_parcelid()
#
#
# def get_human_simcards(humanid):
#     try:
#         cursor.execute(
#             "SELECT * FROM simcards WHERE humanid = {}\
#             simcard BY parcelid DESC".format(humanid)
#             )
#         simcards = cursor.fetchall()
#         res = [dict_simcard(simcard) for simcard in simcards]
#         count = cursor.rowcount
#         print(count, "simcards fetched")
#         result = (res, 200)
#     except (Exception, psycopg2.Error) as error:
#         print('error in get_human_simcards function:', error)
#         result = ('system error, contact support', 500)
#     except Exception as error:
#         print(error)
#         result = ('no simcards for this human', 404)
#     return result
#
#
# def get_simcard(parcelid):
#     try:
#         cursor.execute(
#             "SELECT * FROM simcards WHERE parcelid = {}"
#             .format(parcelid))
#         simcard = cursor.fetchone()
#         print("simcard fetched")
#         return dict_simcard(simcard)
#     except (Exception, psycopg2.Error) as error:
#         print(error)
#
#
# def check_token(token):
#     try:
#         cursor.execute((
#             'select * FROM revoked_tokens WHERE token = %s'),
#             (str(token),))
#         revoked = cursor.fetchone()
#         print(revoked)
#         return revoked
#     except (Exception, psycopg2.Error) as e:
#         print(e)
#
#
# def dict_simcard(simcard):
#     do = {
#         'parcelid': simcard[0],
#         'humanid': simcard[1],
#         'name': simcard[2],
#         'phone_number': simcard[3],
#         'serial': simcard[4],
#         'service_provider': simcard[5],
#         'is_active': simcard[6],
#         'service_class': simcard[7],
#         'category': simcard[8],
#         'current_location': simcard[9],
#         'description': simcard[10],
#         'charge': simcard[11]
#     }
#     return do
#
#
# # def edit_human_password(human, old_password, new_password):
# #     if human.validate_password(old_password):
# #         try:
# #             sql_update_query = 'Update humans SET password_hash = %s WHERE\
# #                 humanid = %s'
# #             cursor.execute(sql_update_query, (
# #                 human.set_password(new_password), human.humanid))
# #             save()
# #             return 'password changed'
# #         except (Exception, psycopg2.Error) as error:
# #             return("Error in update operation", error)
# #     else:
# #         return "wrong current password"s
#
