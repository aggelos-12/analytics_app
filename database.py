import sqlite3
import requests
from datetime import datetime
import os


# Αρχικοποίηση βάσης δεδομένων
def initialize_database():
    if not os.path.exists("database.db"):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.executescript("""
            CREATE TABLE COSTS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE  DATE,
                COST FLOAT,
                DESCRIPTION TEXT,
                CATEGORY TEXT,
                NOTES TEXT
            );
            
            CREATE TABLE EARNINGS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CATEGORY TEXT,
                PROFIT FLOAT,
                DESCRIPTION TEXT,
                ROI INTEGER,
                NOTES TEXT,
                DATE  DATE
            );

            CREATE TABLE INVESTMENTS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE  DATE,
                ENTRY FLOAT,
                DESCRIPTION TEXT,
                AMOUNT INTEGER,
                CURRENCY TINYTEXT,
                PLATFORM TEXT
            );

            CREATE TABLE LOSSES(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CATEGORY TEXT,
                LOSS FLOAT,
                DESCRIPTION TEXT,
                DATE  DATE,
                NOTES TEXT
            );

            CREATE TABLE PENDING_EARNINGS(
                ID INTEGER  PRIMARY KEY AUTOINCREMENT,
                CATEGORY TEXT,
                PROFIT FLOAT,
                DESCRIPTION TEXT,
                ROI INTEGER,
                NOTES TEXT,
                DATE DATE,
                IMMEDIATE_TRANSFER BOOL
            );

        """)

        connection.commit()
        connection.close()


# Θέτει την σύνδεση με την βάση
def get_connection():
    return sqlite3.connect("database.db")



# Διαγραφή πίνακα
def drop_table(table_name):
    connection = get_connection()
    cursor = connection.cursor()
    query  = f"""
        DROP TABLE IF EXISTS {table_name}
    """
    cursor.execute(query)
    connection.commit()
    connection.close()





# Στην περίπτωση όπου στο call δεν περαστεί κάποια παράμετρος
# επιστρέφει το συνολικό gross profit
# διαφορετικά επιστρέφει το gross profit μόνο ενός χρόνου
def get_total_gross_profit_year(year=None):
    # άνοιξε το connection με την βάση δεδομένων
    connection = get_connection()
    # άνοιξε το connection με τον cursor (ώστε να μπορείς να διαχειριστείς τα δεδομένα)
    cursor = connection.cursor()

    # η εντολή cursor.execute() αποθηκεύει το αποτέλεσμα οπότε για να το αποθκέυσω τρέχω την παρακάτω εντολή
    # επιστρέφει tuple οπότε είτε πάρε το πρώτο στοιχείο ([0]) απο αυτό είτε αν το tuple είναι κενό
    # εισχώρησε την τιμή 0.0 στην μεταβλητή

    if year:
        # sql query
        cursor.execute('SELECT SUM(PROFIT) FROM EARNINGS WHERE DATE LIKE (?)', (f"{year}%",))
        total_profit = cursor.fetchone()[0] or 0.0
    else:
        # sql query  
        cursor.execute('SELECT SUM(PROFIT) FROM EARNINGS')
        total_profit = cursor.fetchone()[0] or 0.0

    # κλείσε το connection με την βάση ώστε να μπορείς να την διαχειριστείς με άλλο function
    # ένα open connection δεσμεύει πόρους οπότε είναι απαρραίτητο να το κλείνεις
    # ο cursor κλείνει και αυτός αν κλείσεις το connection μόνο
    connection.close() 
    return total_profit


# Επιστρέφει το gross profit για κάθε μήνα ενός χρόνου
def get_gross_profits_each_month_of_a_year(year):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
                SELECT strftime('%m', DATE) AS MONTH,
                SUM(profit)
                FROM EARNINGS
                WHERE DATE LIKE (?)
                GROUP BY MONTH
                ORDER BY MONTH ASC
            """
    cursor.execute(query, (f"{year}%",))
    profits = cursor.fetchall()
    connection.close()
    return profits


# Επιστρέφει το gross profit για κάθε χρόνο
def get_gross_profit_each_year():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
             SELECT strftime('%Y', DATE) AS YEAR,SUM(PROFIT) FROM EARNINGS
             GROUP BY YEAR
             ORDER BY YEAR ASC
            """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

# Επιστρέφει τo συνολικό gross profit, χωρίς να συμπεριλιφθεί αυτό του φετινού χρόνου
def get_gross_profit_except_current_year(current_year):
    connection = get_connection()
    cursor = connection.cursor()
    
    query = """
        SELECT SUM(PROFIT) FROM EARNINGS
        WHERE STRFTIME('%Y',DATE) != ?
    """
    cursor.execute(query, (f"{current_year}",))
    data = cursor.fetchone()
    if data == None or data[0] == None:
        return 0
    else:
        return data[0]




# Στην περίπτωση όπου στο call δεν περαστεί κάποια παράμετρος
# επιστρέφει το συνολικό κόστος
# διαφορετικά επιστρέφει τα κόστη μόνο ενός χρόνου
def get_total_costs_year(year=None):
    connection = get_connection()
    cursor = connection.cursor()
    if year:
        query = """SELECT SUM(COST) FROM COSTS WHERE DATE LIKE (?)"""
        cursor.execute(query, (f"{year}%",))
    else:
        query = """SELECT SUM(COST) FROM COSTS"""
        cursor.execute(query)
    total_costs = cursor.fetchone()[0] or 0.0
    connection.close()
    return total_costs


# Επιστρέφει τo συνολικό  κόστος, χωρίς να συμπεριλιφθεί αυτό του φετινού χρόνου
def get_total_costs_except_current_year(current_year):
    
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT SUM(COST) FROM COSTS
        WHERE STRFTIME('%Y', DATE) != ?
    """
    
    cursor.execute(query, (f"{current_year}",))
    data = cursor.fetchone()
    if data == None or data[0] == None:
        return 0
    else:
        return data[0]


# Στην περίπτωση όπου στο call δεν περαστεί κάποια παράμετρος
# επιστρέφει το συνολικό loss
# διαφορετικά επιστρέφει τα losses μόνο ενός χρόνου
def get_total_losses_year(year=None):
    connection = get_connection()
    cursor = connection.cursor()
    #Αν δωθεί συγκεκριμένη χρονιά άθροισε τα Losses μόνο αυτής της χρονιάς, διαφορετικά άθροισε όλων των χρόνων
    if year:
        cursor.execute('SELECT SUM(LOSS) FROM LOSSES WHERE DATE LIKE (?)', (f"{year}%",)) 
    else:
        cursor.execute('SELECT SUM(LOSS) FROM LOSSES')    
    
    total_losses = cursor.fetchone()[0] or 0.0
    connection.close()
    return total_losses

# Επιστρέφει τo συνολικό loss, χωρίς να συμπεριλιφθεί αυτό του φετινού χρόνου
def get_total_losses_except_current_year(current_year):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT SUM(LOSS) FROM LOSSES
        WHERE STRFTIME('%Y', DATE) != ?
    """
    
    cursor.execute(query, (f"{current_year}",))
    data = cursor.fetchone()
    if data == None or data[0] == None:
        return 0
    else:
        return data[0]


# Επιστρέφει τα costs&losses (συνολικά) για κάθε χρόνο
def get_cost_losses_each_year():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
            SELECT YEAR, SUM(COST) FROM (
                SELECT strftime('%Y', DATE) AS YEAR, SUM(COST) AS COST
                FROM COSTS
                GROUP BY YEAR
                
                UNION ALL
                
                SELECT strftime('%Y', DATE) AS YEAR, SUM(LOSS) AS COST
                FROM LOSSES
                GROUP BY YEAR
            )
            GROUP BY YEAR
            ORDER BY YEAR ASC  
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

# Επιστρέφει τα costs&losses για έναν χρόνο
def get_cost_losses_year(year):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT YEAR, COALESCE(SUM(COST_LOSSES), 0) FROM
        (   SELECT strftime('%Y', DATE) AS YEAR, SUM(COST) AS COST_LOSSES FROM COSTS
            WHERE DATE LIKE ?
            GROUP BY YEAR
        UNION ALL
            SELECT strftime('%Y', DATE) AS YEAR, SUM(LOSS) AS COST_LOSSES FROM LOSSES
            WHERE DATE LIKE ?
            GROUP BY YEAR
        )
        
    """
    cursor.execute(query, (f"{year}%", f"{year}%"))
    
    data = cursor.fetchone()
    connection.close()
    if data == None:
        return 0
    else:
        return data[1]
    
    
# Επιστρέφει τα costs&losses για κάθε μήνα ενός χρόνου
def get_cost_losses_each_month_of_a_year(year):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
            SELECT MONTH, SUM(COST) FROM
            (
                SELECT strftime('%m', DATE) AS MONTH,
                SUM (COST) AS COST FROM COSTS
                WHERE DATE LIKE (?)
                GROUP BY MONTH

                UNION ALL

                SELECT strftime('%m', DATE) AS MONTH,
                SUM(LOSS) AS COST FROM LOSSES
                WHERE DATE LIKE(?)
                GROUP BY MONTH
            )
            GROUP BY MONTH
            ORDER BY MONTH ASC       
    """
    data = cursor.execute(query, (f"{year}%", f"{year}%",))
    data = cursor.fetchall()
    connection.close()
    return data



# Επιστρέφει για κάθε χρόνο το συνολικο cost και loss
# σε διαφορετική στήλη για το καθένα
def get_cost_losses_2_columns():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
            SELECT YEAR,COALESCE(SUM(COST), 0), COALESCE(SUM(TOTAL_LOSS),0) FROM (
                SELECT strftime('%Y', DATE) AS YEAR, SUM(COST) AS COST, NULL AS TOTAL_LOSS FROM COSTS
                GROUP BY YEAR

            UNION ALL
                SELECT strftime('%Y', DATE) AS YEAR, NULL AS COST, SUM(LOSS) AS TOTAL_LOSS  FROM LOSSES
                GROUP BY YEAR
            )
            GROUP BY YEAR
            ORDER BY YEAR ASC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data 


# Στην περίπτωση όπου στο call δεν περαστεί κάποια παράμετρος
# επιστρέφει το συνολικό net profit
# διαφορετικά επιστρέφει τo net profit μόνο ενός χρόνου
def get_total_net_profit_of_a_year(year=None):
    if year:
        total_net_profit = get_total_gross_profit_year(year) - (get_total_losses_year(year) + get_total_costs_year(year))
    else:
        total_net_profit = get_total_gross_profit_year() - (get_total_losses_year() + get_total_costs_year())
    return total_net_profit

# Επιστρέφει τo συνολικό net profit, χωρίς να συμπεριλιφθεί αυτό του φετινού χρόνου
def get_total_net_profit_except_current_year(current_year):
    total_net_profit = (get_total_gross_profit_year() - (get_total_losses_year() + get_total_costs_year())) - get_total_net_profit_of_a_year(current_year)
    return total_net_profit  

# Επιστρέφει τo net profit για κάθε χρόνο
def get_total_net_profit_of_each_year():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT YEAR, SUM(PROFIT - (COST + LOSS))  FROM(
            SELECT strftime('%Y', DATE) AS YEAR, SUM(PROFIT) AS PROFIT, 0 AS COST, 0 AS LOSS FROM EARNINGS GROUP BY YEAR
            UNION ALL
            SELECT strftime('%Y', DATE) AS YEAR, 0 AS PROFIT,SUM(COST) AS COST, 0 AS LOSS FROM COSTS GROUP BY YEAR
            UNION ALL
            SELECT strftime('%Y', DATE) AS YEAR, 0 AS PROFIT, 0 AS COST,SUM(LOSS) AS LOSS FROM LOSSES GROUP BY YEAR
        )
        GROUP BY YEAR
        ORDER BY YEAR ASC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data








# Χρησιμοποιείτε για να κάνει convert το νόμισμα της επένδυσης
# σε ευρώ (σε περίπτωση όπου δεν είναι ευρώ), έπειτα βρίσκει το
# συνολικό ποσό επενδύσεων 
def get_sum_investments():
    try:
        current_date = datetime.today()
        # API request
        response = requests.get("https://open.er-api.com/v6/latest/EUR", timeout=10)
        # Αν το call επιστρέψει error code γίνεται raise exception και ο κώδικας
        # μπαίνει κατευθείαν στο except clause
        response.raise_for_status()
        # Mετάτρεπω τα δεδομένα τα οποία επέστερεψε ο server ως raw text σε JSON
        # ώστε να είναι προσβάσιμα από τον κώδικα
        # π.χ. δεδομένα server "'{"amount": 1.0, "base": "USD", "rates": {"EUR": 0.92}}'"
        data = response.json()
        rates = data['rates']
        # USD TO EUR exhcange rate
        
        # GBP TO EUR exhcange rate
        usd_to_eur = 1 / rates["USD"]
        gbp_to_eur = 1 / rates["GBP"]

        connection = get_connection()
        cursor = connection.cursor()
        query = """
            SELECT COALESCE(SUM(
                                CASE CURRENCY
                                    WHEN 'USD' THEN ENTRY * ?
                                    WHEN 'GBP' THEN ENTRY * ?
                                    WHEN 'EUR' THEN ENTRY
                                    ELSE 0.0 END
                                )   
                        
            , 0.0)
            FROM INVESTMENTS
            
        """
        cursor.execute(query, (usd_to_eur, gbp_to_eur,))
        result = cursor.fetchone()[0]
        connection.close()
        if  result == 0.0:
            return 'There are no records to sum'
        else:
            return result
        
    # Αν για τον οπιαδήποτε λόγο δεν λειτουργει το API θα εμφανιστεί το response.text
    # error code (π.χ. 404, 500, 429)    
    except requests.exceptions.HTTPError as error:
        return f"API error: {response.text}"
    # Σε περίπτωση που κοπεί το internet, πέσει DNS ή γίνει timeout
    except requests.exceptions.RequestException as error:
        return f"Network error {error}"



# Επιστρέφει τον πίνακα INVESTMENTS
def get_investments():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM INVESTMENTS")
    entries = cursor.fetchall()
    connection.close()
    return entries

# Επιστρέφει τον πίνακα INVESTMENTS μόνο με τις στήλες DATE, ENTRY, DESCRIPTION, CURRENCY 
def get_investments_for_line_chart():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT DATE, ENTRY, DESCRIPTION, CURRENCY 
        FROM INVESTMENTS 
        ORDER BY DATE ASC"""
    )
    entries = cursor.fetchall()
    connection.close()
    return entries




# Επιστρέφει τον πίνακα COSTS
def get_costs():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
            SELECT * FROM COSTS
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

# Επιστρέφει τον πίνακα LOSSES
def get_losses():
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM LOSSES"""
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

# Επιστρέφει τον πίνακα EARNINGS
def get_earnings():
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM EARNINGS"""
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

# Επιστρέφει τον πίνακα PENDING_EARNINGS
def get_pending_earnings():
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM PENDING_EARNINGS"""
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

# Επιστρέφει τα categories του πίνακα PENDING_EARNINGS
def get_pending_earnings_categories():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT UPPER(CATEGORY) FROM PENDING_EARNINGS")
    data = cursor.fetchall()
    connection.close()
    return data

# Επιστρέφει τα categories του πίνακα EARNINGS
def get_earnings_categories():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT UPPER(CATEGORY) FROM EARNINGS")
    data = cursor.fetchall()
    connection.close()
    return data


# Επιστρέφει τα categories του πίνακα LOSSES
def get_costs_categories():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT UPPER(CATEGORY) FROM COSTS")
    data = cursor.fetchall()
    connection.close()
    return data


# Επιστρέφει τα categories του πίνακα LOSSES
def get_losses_categories():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT UPPER(CATEGORY) FROM LOSSES")
    data = cursor.fetchall()
    connection.close()
    return data


# Επιστρέφει τα currencies από τον πίνακα INVESTMENTS
def get_investments_currencies():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT CURRENCY FROM INVESTMENTS")
    data = cursor.fetchall()
    if not data:       
        connection.close()
        return [('EUR',)]
    else:
        connection.close()
        return data


# Προσθέτει νεο entry στον πίνακα cost
def add_cost_entry(date, cost, description, category, notes):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO COSTS (DATE, COST, DESCRIPTION, CATEGORY, NOTES) VALUES (?,?,?,UPPER(?),?)', (date, cost, description, category, notes))
    connection.commit()
    connection.close()



# Προσθέτει νεο entry στον πίνακα earning
def add_earning_entry(category, profit, description, roi, notes, date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO EARNINGS (CATEGORY, PROFIT, DESCRIPTION, ROI, NOTES, DATE) VALUES (UPPER(?), ?, ?, ?, ?, ?)', (category, profit, description, roi, notes, date))
    connection.commit()
    connection.close()

# Προσθέτει νεο entry στον πίνακα pending earning
def add_pending_earning_entry(category, profit, description, roi, notes, date, immediate_transfer):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO PENDING_EARNINGS (CATEGORY, PROFIT, DESCRIPTION, ROI, NOTES, DATE, IMMEDIATE_TRANSFER) VALUES (UPPER(?), ?, ?, ?, ?, ?, ?)', (category, profit, description, roi, notes, date, immediate_transfer))
    connection.commit()
    connection.close()

# Προσθέτει νεο entry στον πίνακα investments
def add_investment_entry(date, entry, description, amount, currency, account, platform):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO INVESTMENTS (DATE, ENTRY, DESCRIPTION, AMOUNT, CURRENCY, ACCOUNT, PLATFORM) VALUES (?, ?, ?, ?, ?, ?, ?)', (date, entry, description, amount, currency, account, platform))
    connection.commit()
    connection.close()

# Προσθέτει νεο entry στον πίνακα losses
def add_loss_entry(category, loss, description, date, notes):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO LOSSES (CATEGORY, LOSS, DESCRIPTION, DATE, NOTES) VALUES (UPPER(?), ?, ?, ?, ?)', (category, loss, description, date, notes))
    connection.commit()
    connection.close()
     
# Διαγράφει ένα entry από τον πίνακα loss
def delete_loss_entry(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM LOSSES WHERE ID = ? ', (id,))
    connection.commit()
    connection.close()

# Διαγράφει ένα entry από τον πίνακα cost
def delete_cost_entry(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM COSTS WHERE ID = ?", (id,))
    connection.commit()
    connection.close()

# Διαγράφει ένα entry από τον πίνακα earning
def delete_earning_entry(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM EARNINGS WHERE ID = ?", (id,))
    connection.commit()
    connection.close()

# Διαγράφει ένα entry από τον πίνακα pending earning
def delete_pending_earning_entry(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM PENDING_EARNINGS WHERE ID = ?", (id,))
    connection.commit()
    connection.close()

# Διαγράφει ένα entry από τον πίνακα investments
def delete_investment_entry(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM EARNINGS WHERE ID = ?", (id,))
    connection.commit()
    connection.close()

def delete_all_earnings_entry():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM EARNINGS WHERE ID > 1")
    connection.commit()
    connection.close()

def delete_all_costs_entry():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM COSTS WHERE ID > 1")
    connection.commit()
    connection.close()

def delete_all_investments_entry():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM INVESTMENTS WHERE ID > 1")
    connection.commit()
    connection.close()


if __name__ == "__main__":
    #print(get_losses())
    delete_all_costs_entry()
    #print(get_total_costs_year(2026))
    delete_all_earnings_entry()
    #delete_all_investments_entry()
    #print(get_gross_profit_except_current_year(2026))
    #delete_cost_entry(5)
    #print(get_investments_currencies())

