from database.DB_connect import DBConnect
from model.prodotto import Prodotto
from model.categoria import Category

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_nodi(c):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.*
                    from products p
                    where p.category_id=%s"""

        cursor.execute(query,(c,))

        for row in cursor:
            results.append(Prodotto(**row))



        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_archi(data1,data2,cat):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = f"""with prodotti_validi as (
                    SELECT oi.product_id as id, count(oi.order_id) as peso
                    from order_items oi, orders o
                    where oi.order_id=o.order_id and DATE(o.order_date) between  '{data1}' and '{data2}'
                    group by oi.product_id)
                    
                    select pv.id as id1, pv.peso as peso1, pv1.id as id2, pv1.peso as peso2 
                    from prodotti_validi pv, prodotti_validi pv1
                    where pv.id in (SELECT p.product_id from products p where p.category_id=%s) 
                    and pv1.id in (SELECT p.product_id from products p where p.category_id=%s) and pv.id<>pv1.id"""

        params=[cat, cat]
        cursor.execute(query, params)

        for row in cursor:
            results.append((row["id1"], row["peso1"],row["id2"], row["peso2"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from categories c"""

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))
        cursor.close()
        conn.close()
        return results