import pandas as pd
import psycopg2
from flask import Flask, request
import matplotlib.pyplot as plt

connection = psycopg2.connect(host = 'database-1.cth04qnbqozs.us-east-2.rds.amazonaws.com', user = 'postgres',
                       password = 'postgres', port = '5432')

cursor = connection.cursor()

application = Flask(__name__)

@application.route('/births/<url>', methods = ['GET'])
@application.route('/births/<url>/<month>', methods = ['GET'])

def ex_1_2_3(url, month = ''):
    print(month)
    if url == 'ex1':
    
        cursor.execute('SELECT year, SUM(births) AS "nascimentos" FROM brths GROUP BY year ORDER BY nascimentos DESC;')
        recs = cursor.fetchall()
        sql = "SELECT SUM(births), month FROM brths WHERE year = '{}' GROUP BY month".format(recs[0][0])
        df = pd.read_sql(sql, connection)
        plt.bar(df['month'], df['sum'])
        plt.show()
        
        return recs[0][0], 200

    if url == 'ex2':
        
        cursor.execute("SELECT month, SUM(births)FROM brths WHERE gender = 'F' GROUP BY month ORDER BY sum DESC;")
        recset = cursor.fetchall()
        sql = "SELECT SUM(births), day FROM brths WHERE month ='{}' AND gender = 'F' GROUP BY day;".format(recset[0][0])
        df = pd.read_sql(sql, connection)
        plt.rcParams['figure.figsize'] = ('20', '8')
        plt.bar(df['day'], df['sum'])
        plt.show()    
        
        return recset[0][0], 200
    
   
    if url == 'ex3':
        
        sql = "SELECT SUM(births), day FROM brths WHERE month = '{}' AND gender = 'M' GROUP BY day;".format(month)
        df = pd.read_sql(sql, connection)
        plt.rcParams['figure.figsize'] = ('20', '8')
        plt.plot(df['day'], df['sum'])
        
        plt.show()
        
        return str(df['sum'].sum()), 200
    
    
if __name__ == '__main__':

    application.run()