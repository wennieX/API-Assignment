import psycopg2
import traceback


class DatabaseClient:
    def __init__(
            self, host="localhost", port=5432, user="admin", database="db", password=""
    ):
        self.conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        self.conn.autocommit = False

    def close(self):
        if self.conn:
            self.conn.close()

    def ingest_json(self, json_file):

        ingest_success = False
        with open(json_file) as f:
            data = f.read()

        cursor = self.conn.cursor()
        query_sql = """
        INSERT INTO information
        SELECT * FROM json_populate_recordset(NULL::information, %s);
        """

        try:
            cursor.execute(query_sql, (data,))
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into information table", error)
        finally:
            ingest_success = True
            cursor.close()
            return ingest_success

    def get_information(self, id):
        cursor = self.conn.cursor()
        q = """
        SELECT * from information 
        WHERE id = %s
        """
        try:
            cursor.execute(q, (id,))
        except psycopg2.errors.InFailedSqlTransaction as err:
            traceback.print_exc()
            return None

        results = cursor.fetchall()
        # Psycopg opens transactions even with SELECT queries, so we close it here
        self.conn.commit()
        cursor.close()
        if not results:
            return {}
        return results

    def all_persons_with_duplicate_email(self):
        cursor = self.conn.cursor()
        q = """
        SELECT first_name, last_name, email FROM information
        WHERE email IN (
        SELECT email FROM information GROUP BY email HAVING COUNT(email) > 1
        )
        """
        try:
            cursor.execute(q)
        except (Exception, psycopg2.Error) as error:
            print("Failed to select record from information table", error)
        finally:
            persons = cursor.fetchall()
            # Psycopg opens transactions even with SELECT queries, so we close it here
            self.conn.commit()
            cursor.close()

            return persons

    def persons_with_same_email(self, email):

        cursor = self.conn.cursor()
        query_sql_email = """
        SELECT first_name, last_name 
        FROM information
        WHERE email = %s
        """

        try:
            cursor.execute(query_sql_email, (email,))
        except psycopg2.errors.InFailedSqlTransaction as err:
            traceback.print_exc()
            return None
        persons = cursor.fetchall()

        self.conn.commit()
        cursor.close()

        return persons

    def update_information(self, person_id, update_data_dict):
        update_success = True
        cursor = self.conn.cursor()
        results = self.get_information(id=person_id)
        if results:
            update_sql = ""

            if len(update_data_dict.keys()) == 1:
                sql = "UPDATE information SET {} = %s WHERE id = {}"
                sql = sql.format(''.join(update_data_dict.keys()), person_id)
                # col = list(update_data_dict.keys())[0]
                val = list(update_data_dict.values())[0]
                update_sql = cursor.mogrify(sql, (val,))
            else:
                sql_template = "UPDATE information SET ({}) = %s WHERE id = {}"
                params = (tuple(update_data_dict.values()),)
                sql = sql_template.format(', '.join(update_data_dict.keys()), person_id)
                update_sql = cursor.mogrify(sql, params)

            print(update_sql)
            try:
                cursor.execute(update_sql)
                self.conn.commit()
            except (Exception, psycopg2.Error) as error:
                print("Failed to update record in information table", error)
                update_success = False
            finally:
                cursor.close()
                return update_success
        else:
            # print("id is not in the table")
            update_data_dict["id"] = person_id
            sql_template = "INSERT INTO information ({})  VALUES {} RETURNING id"
            sql = sql_template.format(','.join(update_data_dict.keys()), tuple(update_data_dict.values()))
            # print(sql)
            try:
                cursor.execute(sql)
            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record into information table", error)
                update_success = False
            finally:
                # db_id = cursor.fetchone()[0]
                self.conn.commit()
                cursor.close()
                return update_success

    def delete_information(self, id):
        cursor = self.conn.cursor()
        q = "DELETE FROM information WHERE id = %s"
        try:
            cursor.execute(q, (id,))
        except (Exception, psycopg2.Error) as error:
            print("Failed to delete record from information table", error)

        finally:
            rows_deleted = cursor.rowcount
            self.conn.commit()
            cursor.close()
            return rows_deleted













