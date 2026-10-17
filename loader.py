import database
import pandas as pd


def add_to_database(dataframe): 
    # Δημιουργώ το παρακάτω dictionary έτσι ώστε να
    # ελέγχω αν το dataframe που ανέβαζει ο χρήστης έχει
    # την σωστή σειρα στηλών για κάθε πίνακα της βάσης
    table_schema = { 
        "costs": ["DATE", "COST", "DESCRIPTION", "CATEGORY", "NOTES"],
        "earnings": ["CATEGORY", "PROFIT", "DESCRIPTION", "ROI", "NOTES", "DATE"],
        "investments": ["DATE", "ENTRY", "DESCRIPTION", "AMOUNT", "CURRENCY", "ACCOUNT", "PLATFORM"],
        "losses": ["CATEGORY", "LOSS", "DESCRIPTION", "DATE", "NOTES"],
        "pearnings": ["CATEGORY", "PROFIT", "DESCRIPTION", "ROI", "NOTES", "DATE", "IMMEDIATE_TRANSFER"]
    }

    # Το παρα
    columns_dtypes = {
        "DATE": "date",
        "COST": "numeric",
        "DESCRIPTION": "str",
        "CATEGORY": "str",
        "NOTES": "str",
        "PROFIT": "numeric",
        "ROI": "numeric",
        "ENTRY": "numeric",
        "AMOUNT": "numeric",
        "CURRENCY": "str",
        "ACCOUNT": "str",
        "PLATFORM": "str",
        "LOSS": "numeric",
        "IMMEDIATE_TRANSFER": "bool"
    }
    # Αποθηκεύω τα ονόματα των στηλών του dataframe
    columns_names = list(dataframe.columns)

    # Για κάθε blueprint πίνακα έλεγχω αν το dataframe ταιριάζει με ένα
    # από αυτά
    for table in table_schema:
        # Έλεγχω αν η σειρά των στηλών είναι όπως στα schemas
        if table_schema[table] == columns_names:
            for column in table_schema[table]:
                # Για κάθε στηλη μετέτρεψε κάθε στοιχείο σε numeric τύπο (int,float)
                # άρα αν είναι αριθμός τότε αφήνει το στοιχείο όπως είναι
                # αν το στοιχείο δεν είναι νούμερο, τότε θα επιστρέψει το στοιχείο NaN (λόγω του errors="coerce")
                # άρα με αυτό τον τρόπο κάνω filter τα στοιχεία (όχι ένα προς ένα)
                
                if columns_dtypes[column] == "numeric":
                    converted_column = pd.to_numeric(dataframe[column], errors="coerce")
                    dataframe[column] = converted_column
                    #print("numeric")
                    if converted_column.isna().any():
                        return f"Invalid format in column '{column}'. Please check your values."
                        
                elif columns_dtypes[column] == "date":
                    converted_column = pd.to_datetime(dataframe[column], errors="coerce", format="%Y/%m/%d").dt.date
                    dataframe[column] = converted_column.astype(str)
                    if converted_column.isna().any():
                        return f"Invalid format in column '{column}'. Please check your values."
                         
                elif columns_dtypes[column] == "str":
                    pass 
                
                
                
                    

                # το isna() επιστρέφει ένα series με boolean τιμές, οι οποίες θα είναι
                # False για κάθε στοιχειο που δεν είναι NaN, διαφορετικά επιστρέφει True
                # η any() επιστρέφει True εαν το series το οποίο δοθεί έχει τουλάχιστον μια True τιμή
                # Άρα ο κώδικας τοποθετεί NaN όπου η τιμή δεν συμβαδίζει με τον τύπο δεδομένων της στήλης
                # και με την any() έλεγχω αν υπάρχει τουλάχιστον μια τέτοια τιμή

            if table == "costs":
                print(table)
                for row in dataframe.itertuples(index=False):
                    database.add_cost_entry(row[0], row[1], row[2], row[3], row[4])
            elif table == "earnings":
                for row in dataframe.itertuples(index=False):
                    database.add_earning_entry(row[0], row[1], row[2], row[3], row[4], row[5])
            break
    return "data has been added"        
           
             
    
    

if __name__ == '__main__':
    pass