import database
import pandas as pd
from datetime import datetime

current_year = datetime.now().year



def calculate_percentage_difference_year_to_year(func):
    # Τύπος για υπολογισμός διαφοράς ποσοστού : ((new value - old value) / abs(old value)) * 100
    # Δεν πολλαπλασίαζω με το 100 διότι το κάνει αυτόματα η st.metric 
    current_value = func(current_year)
    past_value = func(current_year - 1)
    
    # Σε περίπτωση που είναι άδεια η βάση δεδομένων
    if past_value == 0:
        return None
    percentage_diff = ((current_value - past_value) / abs(past_value))
    return percentage_diff


def calculate_percentage_difference_for_gross_profit():
    # Τύπος για υπολογισμός διαφοράς ποσοστού : ((new value - old value) / abs(old value)) * 100
    # Δεν πολλαπλασίαζω με το 100 διότι το κάνει αυτόματα η st.metric 
    current_value = database.get_total_gross_profit_year()
    print(current_value)
    past_value = database.get_gross_profit_except_current_year(current_year)
    print(past_value)
    if past_value == 0:
        return 0
    percentage_diff = ((current_value - past_value) / abs(past_value))
    return percentage_diff

def calculate_percentage_difference_for_net_profit():
    # Τύπος για υπολογισμός διαφοράς ποσοστού : ((new value - old value) / abs(old value)) * 100
    # Δεν πολλαπλασίαζω με το 100 διότι το κάνει αυτόματα η st.metric 
    current_value = database.get_total_net_profit_of_a_year()
    print(current_value)
    past_value = database.get_total_net_profit_except_current_year(current_year)
    print(past_value)
    if past_value == 0:
        return 0
    percentage_diff = ((current_value - past_value) / abs(past_value))
    return percentage_diff



def calculate_percentage_difference_for_costs():
    # Τύπος για υπολογισμός διαφοράς ποσοστού : ((new value - old value) / abs(old value)) * 100
    # Δεν πολλαπλασίαζω με το 100 διότι το κάνει αυτόματα η st.metric 
    current_value = database.get_total_costs_year()
    past_value = database.get_total_costs_except_current_year(current_year)
    if past_value == 0:
        return None
    percentage_diff = ((current_value - past_value) / abs(past_value))
    return percentage_diff

def calculate_percentage_difference_for_losses():
    # Τύπος για υπολογισμός διαφοράς ποσοστού : ((new value - old value) / abs(old value)) * 100
    # Δεν πολλαπλασίαζω με το 100 διότι το κάνει αυτόματα η st.metric 
    current_value = database.get_total_losses_year()
    past_value = database.get_total_losses_except_current_year(current_year)
    if past_value == 0:
        return None
    percentage_diff = ((current_value - past_value) / abs(past_value))
    return percentage_diff

def calculate_percentage_difference_for_costs_and_losses():
    # χρησιμοποιώ τα προηγούμενα ποσοστά για να υπολογίζω την
    # διαφορά για το ολικό costs&losses
    # Tύπος : (cost% * (total_costs_except_current_year/costs_and_losses_except_current_year)) * (loss% * (total_losses_except_current_year/costs_and_losses_except_current_year))
    cost_percentage_diff = calculate_percentage_difference_for_costs()
    loss_percentage_diff = calculate_percentage_difference_for_losses()
    if cost_percentage_diff == None:
        return None
    
   
    total_costs = database.get_total_costs_except_current_year(current_year)
    total_losees = database.get_total_losses_except_current_year(current_year)
    total_costs_losses = total_costs + total_losees

    cost_weight = total_costs/total_costs_losses
    loss_weight = total_losees/total_costs_losses

    percentage_diff = (cost_percentage_diff * cost_weight) + (loss_percentage_diff * loss_weight)

    return percentage_diff

# Επιστρέφει τον πίνακα ΕARNINGS ως panas dataframe
def get_earnings():
    # ο πίνκας ΕARNINGS σε μορφή [(element1), (element1)]
    data_earnings = database.get_earnings()
    # μετατρέπεται σε τύπο pandas
    dataframe_earnings = pd.DataFrame(data_earnings, columns=['ID', 'CATEGORY', 'PROFIT', 'DESCRIPTION', 'ROI', 'NOTES', 'DATE'])
    #Σε περίπτωση όπου ο πίνακας είναι άδειος, διαγράφεται η στήλη ID
    if dataframe_earnings.empty:
        dataframe_earnings = dataframe_earnings.drop(columns=['ID'])
        return dataframe_earnings
    # μετατρέπω την DATE στήλη σε datetime αντικείμενο, επιπλέον βάζω format mixed, δίοτι όταν
    # ο χρήσης προσθέτει ένα entry από το st.data_editor δεν θα έχει το ίδιο format με αυτό που
    # έχει θέσει η βάση οπότε έτσι θα μπορέσει η to_datetime να είναι δυναμική όταν αλλάζει
    # το date string σε datetime αντικείμενο
    dataframe_earnings['DATE'] = pd.to_datetime(dataframe_earnings['DATE'], format='mixed')
    # ταξινομώ το dataframe με βάση την ημερομηνία
    dataframe_earnings = dataframe_earnings.sort_values(by="DATE", ascending=False)
    return dataframe_earnings

# Επιστρέφει τον πίνακα LOSSES ή COSTS ως panas dataframe
def get_losses_or_costs(choice):
    if choice == "losses":
        # Αποθηκεύω όλα τα losses
        data_losses = database.get_losses()
        # Τα μετατρέπω σε pandas δεδομένα
        dataframe_losses = pd.DataFrame(data_losses, columns=['ID', 'CATEGORY', 'LOSS', 'DESCRIPTION', 'DATE', 'NOTES'])
        #Σε περίπτωση όπου ο πίνακας είναι άδειος, διαγράφεται η στήλη ID
        if dataframe_losses.empty:
            return dataframe_losses.drop(columns=['ID'])
        # Η στήλη DATE είναι τύπος str, επιπλέον έχει formats 
        # ( '2024-05-01 00:00:00' από το πίνακα sql και '2024-05-01' από το κουμπί add loss)
        # Μετατρέπω τα strings σε datetime τύπο με format='mixed' ώστε να διαβαστούν σωστά όλα τα formats,
        # επιτρέποντας στο st.column_config.DateColumn να τα μορφοποιήσει σε 'DD-MM-YYYY' στο UI
        dataframe_losses['DATE'] = pd.to_datetime(dataframe_losses['DATE'], format='mixed')
        dataframe_losses = dataframe_losses.sort_values(by='DATE', ascending=False)
        return dataframe_losses
    else:
        data_costs = database.get_costs()
        dataframe_costs = pd.DataFrame(data_costs, columns=['ID','DATE', 'COST', 'DESCRIPTION', 'CATEGORY', 'NOTES']) 
        #Σε περίπτωση όπου ο πίνακας είναι άδειος, διαγράφεται η στήλη ID
        if dataframe_costs.empty:
            return dataframe_costs.drop(columns=['ID'])
        dataframe_costs['DATE'] = pd.to_datetime(dataframe_costs['DATE'], format='mixed')
        dataframe_costs = dataframe_costs.sort_values(by='DATE', ascending=False)
        return dataframe_costs

# Επιστρέφει τον πίνακα INVESTMENTS ως panas dataframe
def get_investments():
    current_date = datetime.today()
    data_investmens = database.get_investments()
    data_investmens = pd.DataFrame(data_investmens, columns=['ID', 'DATE', 'ENTRY', 'DESCRIPTION', 'AMOUNT', 'CURRENCY', 'PLATFORM', 'ACCOUNT'])
    data_investmens['DATE'] = pd.to_datetime(data_investmens['DATE'], format='mixed')
    #Σε περίπτωση όπου ο πίνακας είναι άδειος, διαγράφεται η στήλη ID
    if data_investmens.empty:
        return data_investmens.drop(columns=['ID'])
    
    # φιλτράρω τα δεδομένα έτσι ώστε να επιστρέφονται μόνο οι επενδύσεις οι οποίες είναι
    # ακόμα ενεργές βάση ημερομηνίας
    data_investmens = data_investmens[data_investmens["DATE"] > current_date]
    data_investmens = data_investmens.sort_values(by='DATE')
    return data_investmens

# Επιστρέφει τον πίνακα INVESTMENTS ως panas dataframe με τις στήλες "DATE", "ENTRY", "DESCRIPTION", "CURRENCY"
def get_investments_line_chart():
    current_date = datetime.today()
    dataframe_investments_for_chart = database.get_investments_for_line_chart()
    dataframe_investments_for_chart = pd.DataFrame(dataframe_investments_for_chart, columns=["DATE", "ENTRY", "DESCRIPTION", "CURRENCY"])
    dataframe_investments_for_chart["DATE"] = pd.to_datetime(dataframe_investments_for_chart["DATE"], format="mixed")
    
    # φιλτράρω τα δεδομένα έτσι ώστε να επιστρέφονται μόνο οι επενδύσεις οι οποίες είναι
    # ακόμα ενεργές βάση ημερομηνίας
    dataframe_investments_for_chart = dataframe_investments_for_chart[dataframe_investments_for_chart["DATE"] > current_date]
    return dataframe_investments_for_chart

# Επιστρέφει τον πίνακα PENDING_EARNINGS ως panas dataframe
def get_pending_earnings():
    data_pending_earnings = database.get_pending_earnings()
    dataframe_pending_earnings = pd.DataFrame(data_pending_earnings, columns=['ID', 'CATEGORY', 'PROFIT', 'DESCRIPTION', 'ROI', 'NOTES', 'DATE', 'IMMEDIATE_TRANSFER'])
    #Σε περίπτωση όπου ο πίνακας είναι άδειος, διαγράφεται η στήλη ID
    if dataframe_pending_earnings.empty:
        return dataframe_pending_earnings.drop(columns=['ID'])
    
    dataframe_pending_earnings['DATE'] = pd.to_datetime(dataframe_pending_earnings['DATE'], format='mixed')
    dataframe_pending_earnings = dataframe_pending_earnings.sort_values(by="DATE", ascending=False)
    return dataframe_pending_earnings

# Επιστρέφει κατηγορίες πινάκων
def get_categories(func):
    data_categories = func()
    data_categories = [element[0] for element in data_categories]
    return data_categories


#def merge_costs_and_losses():

    

def add_template_row(dataframe, table):
    if table == "earnings":
        new_row = pd.Series({ 
            "CATEGORY": "your category",
            "PROFIT": 0,
            "DESCRIPTION": "your description",
            "ROI" :0,
            "NOTES": "your notes",
            "DATE": "yyyy/mm/dd"
        })
    elif table == "costs":
        new_row = pd.Series({ 
            "DATE": "yyyy/mm/dd",
            "COST": 0.0,
            "DESCRIPTION": "your description",
            "CATEGORY": "your category",
            "NOTES": "your notes"
            
        })
    elif table == "losses":
        new_row = pd.Series({
            "CATEGORY": "your category",
            "LOSS": 0.0,
            "DESCRIPTION": "your description", 
            "DATE": "yyyy/mm/dd",
            "NOTES": "your notes"
            
        })
    elif table == "investments":
        new_row = pd.Series({
            "DATE": "yyyy/mm/dd",
            "ENTRY": 0.0,
            "DESCRIPTION": "your description", 
            "AMOUNT": 0,
            "CURRENCY": "EUR",
            "PLATFORM": "your platform",
            "ACCOUNT": "your account"
        })
    elif table == "pearnings":
        new_row = pd.Series({ 
            "CATEGORY": "your category",
            "PROFIT": 0.0,
            "DESCRIPTION": "your description",
            "ROI" :0,
            "NOTES": "your notes",
            "DATE": "yyyy/mm/dd",
            "IMMEDIATE_TRANSFER": 1
        })        


    dataframe = pd.concat([dataframe,new_row.to_frame().T])
    return dataframe

def download_csv(table):
    if table == "earnings":
        dataframe = get_earnings()
        if dataframe.empty:
            dataframe = add_template_row(dataframe, "earnings")
            
    elif table == "costs":
        dataframe = get_losses_or_costs("costs")
        if dataframe.empty:
            dataframe = add_template_row(dataframe, "costs")

    elif table == "pearnings":
        dataframe = get_pending_earnings()
        if dataframe.empty:
            dataframe = add_template_row(dataframe, "pearnings")
    
    elif table == "losses":
        dataframe = get_losses_or_costs("losses")
        if dataframe.empty:
            dataframe = add_template_row(dataframe, "losses")

    elif table == "investments":
        dataframe = get_investments()
        if dataframe.empty:
            dataframe = add_template_row(dataframe, "investments")
    return dataframe

if __name__=='__main__':
    print(get_losses_or_costs("losses"))