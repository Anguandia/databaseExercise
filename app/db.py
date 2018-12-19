import psycopg2
from flask.cli import with_appcontext
import click
from models import Human, Simcard


class Db:
    def __init__(self, db_name='postgres'):
        self.db_name = db_name
        try:
            self.connection = psycopg2.connect(
                "dbname = postgres user = postgres password = kukuer1210 host = localhost \
                port = 5432"
                )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.cursor.execute(f'''create database {self.db_name}''')
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print(f'database {self.db_name} creaed')
        except Exception:
            pass
        self.connection = psycopg2.connect(
                f'''dbname = {self.db_name} user = postgres password = kukuer1210 host = localhost \
                port = 5432'''
                )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        try:
            create_humans = 'CREATE TABLE IF NOT EXISTS humans(\
                    human_id SERIAL PRIMARY KEY NOT NULL, name VARCHAR UNIQUE,\
                    address VARCHAR NOT NULL, age INT NOT NULL,\
                    single BOOLEAN\
                    )'
            self.cursor.execute(create_humans)
            self.save()
            print('table humans created')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        try:
            create_simcard_table_query = 'CREATE TABLE simcards(\
                    id SERIAL PRIMARY KEY NOT NULL, name  varchar NOT NULL,\
                    phone_number INT UNIQUE NOT NULL, serial INT UNIQUE NOT NULL,\
                    service_provider VARCHAR NOT NULL, human_id INT,\
                    is_active BOOLEAN\
                    )'
            self.cursor.execute(create_simcard_table_query)
            self.save()
            print('table simcards created')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except Exception as error:
            print('error', error)


    def save(self):
        self.connection.commit()


    def create(self, name, address, age, single=True):
        human = Human(name, address, age)
        try:
            create_human_query = '''INSERT INTO humans (name, address, \
            age, single) VALUES (%s,%s,%s,%s)'''
            self.cursor.execute(
                create_human_query, (
                    human.name, human.address,
                    human.age, human.single
                    ))
            self.save()
            print("human", human.__dict__, "saved to db")
        except (Exception, psycopg2.Error) as error:
            print("Failed to create human:", error)

    def get_humans(self):
        try:
            self.cursor.execute("SELECT * FROM humans ORDER BY human_id DESC")
            men = self.cursor.fetchall()
            humans = [Db.dict_human(human) for human in men]
            res = humans
        except Exception as error:
            res = f'no humans in humans'
            print(error)
        return res


    def fetch_human_name(self, name):
        try:
            self.cursor.execute((
                "SELECT * FROM humans WHERE name = %s"), (name,))
            human = self.cursor.fetchone()
            res = self.dict_human(human)
        except Exception as error:
            print(error)
            res = f'no human by name {name}'
        return res


    def fetch_human(self, human_id):
        try:
            self.cursor.execute(
                f'''SELECT * FROM humans WHERE human_id {human_id}''')
            human = self.cursor.fetchone()
            print(Db.dict_human(human))
            res = self.dict_human(human)
        except Exception as error:
            print(error)
            res = 'no human with id {human_id}'
        return res


    def fetch_human_address(self, address):
        try:
            self.cursor.execute(f'''SELECT * FROM humans WHERE address = {address}''')
            human = self.cursor.fetchone()
            print(self.dict_human(human))
            res = self.dict_human(human)
        except Exception as error:
            print(error)
            res = f'no address {address}'
        return res


    def edit_human(self, human_id, key, value):
        if key == 'name':
            sql_update_query = 'UPDATE humans SET name = %s WHERE human_id = %s'
        elif key == 'address':
            sql_update_query = 'UPDATE humans SET address = %s WHERE human_id = %s'
        elif key == 'age':
            sql_update_query = 'UPDATE humans SET age = %s\
                WHERE human_id = %s'
        elif key == 'single':
            sql_update_query = 'UPDATE humans SET singlr = %s\
                WHERE human_id = %s'
        else:
            res = f'human has no attribute {key}'
        try:
            self.cursor.execute(sql_update_query, (value, human_id))
            self.save()
            print('ok')
            res = '{} changed'.format(key)
        except (Exception, psycopg2.Error) as error:
            print(error)
            res = f"Error in update operation {error}"
        return res


    def delete_human(self, human_id):
        human = self.fetch_human(human_id)
        if human:
            try:
                sql_delete_query = 'delete from humans WHERE human_id = %s'
                self.cursor.execute(sql_delete_query, (human_id,))
                self.save()
                res = 'human {} deleted'.format(human['name'])
            except (Exception, psycopg2.Error) as error:
                res = 'error deleting human {}'.format(human['name'])
                print("Error deleting", error)
        res = 'no human {}'.format(human['name'])
        print(res)
        return res

    @staticmethod
    def dict_human(tup):
        human = {}
        keys = ['human_id', 'name', 'address', 'age', 'single']
        try:
            for key in keys:
                human[key] = tup[keys.index(key)]
            return human
        except Exception as e:
            print(e)

    @staticmethod
    def to_object(dic):
        from .models import Human
        human = Human('', '', '')
        for key in dic.keys():
            if key in human.__dict__.keys():
                human.__setattr__(key, dic[key])
            human.human_id = dic['human_id']
        return human


    def savesimcard(self, name, phone_number, serial, service_provider, human_id, is_active):
        #for i in range(len(kwargs)):
            simcard = Simcard(name, phone_number, serial, service_provider, human_id, is_active)
            try:
                create_simcard_query = '''INSERT INTO simcards (name, phone_number, serial, service_provider, human_id, is_active) VALUES\
                (%s, %s, %s, %s, %s, %s)'''
                self.cursor.execute(
                    create_simcard_query, (
                        simcard.name, simcard.phone_number, simcard.serial,
                        simcard.service_provider, simcard.human_id, simcard.is_active,
                        ))
                self.save()
                res = 'simcard registere'
            except (Exception, psycopg2.Error) as error:
                print(error)
                res = "Failed to create simcard"
            print(res)
            return res


    def update_simcard(self, input, id, key):
        if input:
            try:
                if key == 'phone_number':
                    sql_update_query = 'UPDATE simcards SET phone_number = %s\
                        WHERE id = %s;'
                elif key == 'is_active':
                    sql_update_query = 'UPDATE simcards SET is_active = %s\
                        WHERE id = %s;'
                elif key == 'human_id':
                    sql_update_query = 'UPDATE simcards SET human_id = %s\
                        WHERE id = %s;'
                elif key == 'name':
                    sql_update_query = 'UPDATE simcards SET name = %s\
                        WHERE id = %s; '
                    self.cursor.execute((sql_update_query), (input, id))
                self.save()
                print("success")
                result = f'{input} updated to \'{key}\''
            except (Exception, psycopg2.Error) as error:
                print("Error in update operation", error)
                result = 'update failed, contact support'
        else:
            result = f'please fill in value for {key}'
        return result


    def delete_simcard(self, id):
        try:
            sql_delete_query = 'DELETE FROM simcards WHERE id = %s'
            self.cursor.execute(sql_delete_query, (id,))
            self.save()
            print("deleted")
        except (Exception, psycopg2.Error) as error:
            print("Error in delete operation", error)


    def get_simcards(self):
        try:
            self.cursor.execute("SELECT * FROM simcards ORDER BY id DESC")
            simcards = self.cursor.fetchall()
            count = self.cursor.rowcount
            print(count, "simcards fetched", simcards)
            result = [self.dict_simcard(simcard) for simcard in simcards]
        except (Exception, psycopg2.Error) as error:
            print('problem in get simcards function', error)
            result = 'an error occured, please contact support'
        except (Exception) as error:
            print('error', error)
            result = 'simcard not found'
        return result

    def get_human_simcards(self, human_id):
        try:
            self.cursor.execute(
                "SELECT * FROM simcards WHERE human_id = {}\
                ORDER BY id DESC".format(human_id)
                )
            simcards = self.cursor.fetchall()
            res = [self.dict_simcard(simcard) for simcard in simcards]
            count = self.cursor.rowcount
            print(count, "simcards fetched")
            result = res,
        except (Exception, psycopg2.Error) as error:
            print('error in get_human_simcards function:', error)
            result = 'system error, contact support'
        except Exception as error:
            print(error)
            result = 'no simcards for this human'
        print(result)
        return result


    def get_simcard(self, id):
        try:
            self.cursor.execute(
                "SELECT * FROM simcards WHERE id = {}"
                .format(id))
            simcard = self.cursor.fetchone()
            print(simcard)
            return simcard
        except (Exception, psycopg2.Error) as error:
            print(error)

    @staticmethod
    def dict_simcard(simcard):
        do = {
            'id': simcard[0],
            'human_id': simcard[5],
            'name': simcard[1],
            'phone_number': simcard[2],
            'serial': simcard[3],
            'service_provider': simcard[4],
            'is_active': simcard[6],
        }
        return do
