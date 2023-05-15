import psycopg2
import urllib.request

# Default Database Setup
db = "mq4"
user_name = "postgres"
passwd = "1234"
host_ip = "192.168.68.226"
port_num = "5432"

# Establishing database connection
def connect_db(db_name=db, login_user=user_name, login_password=passwd, db_host=host_ip, db_port=port_num):
    try:
        curr_db = psycopg2.connect(database=db_name, user=login_user, password=login_password, host=db_host, port=db_port)
        curr_db.set_client_encoding("UTF8")
        return curr_db
    except psycopg2.Error as error:
        print("Database Connection Error!\n===== [Error message] =====\n\n",error,"\n===== [END] =====")
        return None
    except Exception as error:
        print("Database Other Error :",error)
        return None

# Disconnect database
def disconnect_db(target_database_connection):
    try:
        target_database_connection.close()
        return
    except:
        return

# Input data to databases
# Data Format Example
# --> input_datetime (TIMESTAMP WITHOUT time zone) >> e.g. = "2022-02-02 12:12:12"
# --> input_sensor_name ( VARCHAR(10) ) >> e.g. = "CH4"
# --> input_readings ( INTEGER ) >> e.g. = 512
def write_data_to_db(curr_db, input_readings, input_voltage):
    # Executing SQL statements
    cursor = curr_db.cursor()
    #sql_statement = "INSERT INTO sensor_data (time, sensor_name, readings_ch4_ppm) VALUES (%s,%s,%s)"
    sql_statement = "INSERT INTO sensor_data (ch4_ppm, voltage) VALUES (%s, %s)"
    insert_data = (input_readings, input_voltage)
    try:
        cursor.execute(sql_statement,insert_data)
    except psycopg2.Error as error:
        print("Unable to execute query!\n===== [Error message] =====\n\n",error,"\n===== [END] =====")
        cursor.close()
        return
    except Exception as error:
        print("Other Error :",error)
        cursor.close()
        return
    curr_db.commit()
    cursor.close()
    return

# Check if internet is connected
def wifi_is_connected():
    try:
        urllib.request.urlopen('https://www.google.com/')
        return True
    except:
        return False

# This function is just for testing database connection
def test():
    print("You are running testing code!!")
    print("Please call other function to use this program!")
    
    if not wifi_is_connected():
        print("Unable to connect to database. Please check your internet connection.")
    else:
        print("Wifi connected! Trying to connect to database.")
        curr_db = connect_db()
        cursor = curr_db.cursor()
        sql_statement = "SELECT COUNT(*) FROM sensor_data"
        try:
            cursor.execute(sql_statement)
            result = cursor.fetchall()
        except psycopg2.Error as error:
            print("Unable to execute query!\n===== [Error message] =====\n\n",error,"\n===== [END] =====")
        except Exception as error:
            print("Other Error :",error)
        print("Total data amount in database [",db,"] = ", result[0][0])
        print("Conncetion Success!! Closing connection!")
        curr_db.commit()
        cursor.close()
        disconnect_db(curr_db)

if __name__ == '__main__':
    #test()
    write_data_to_db(connect_db(), 4330)
