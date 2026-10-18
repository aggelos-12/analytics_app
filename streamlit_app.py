import streamlit as st
from datetime import datetime
import database
import utils
import plotly.express as px
import calendar
import pandas as pd
import time
import plotly.graph_objects as go
from datetime import timedelta
import loader


st.set_page_config(page_title="My app", layout="wide")

# Με την μεταβλητή page δημιουργώ μια multipage εφαρμογή
# ανάλογα με την τιμή της τρέχω το αντίστοιχο function
# το οποίο αντιπρωσεύει ένα page

# το st.session_state κρατάει τα δεδομένα απο προηγούμενα interaction του
# χρήστη έτσι όταν γίνεται rerun ο κώδικας δεν μηδενίζονται τα δεδομένα
# ανταυτού κρατάνε το προηγούμενο state τους
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Τώρινος χρόνος
current_year = datetime.now().year

# Customize τα κουμπιά του UI (GLOBAL)
st.markdown(
    """
        <style>
            /* εμφάνιση κουμπιών */ 
            [data-testid="stMain"] button[kind="secondary"] {
                background: #363636 !important;
                border-radius: 10px;            
                padding: 10px 24px;                
                box-shadow: 0 4px 12px rgba(110, 69, 226, 0.35);
            }
            /* hover effect */
            [data-testid="stMain"] button[kind="secondary"]:hover {
                background: #D3D3D3 !important;
                color: black;
            }
                                    
            }
        </style>
    """
,unsafe_allow_html=True)

# Customize pop up μηνύματα του UI (GLOBAL)
st.markdown(
"""
    
    <style>
        /* εμφάνιση pop up μηνύματος */ 
        [data-testid="stToast"]{
            background-color: #222222;
            border-radius: 25px;
            animation-name: fadeout;
            animation-duration: 8s;
            animation-fill-mode: forwards;
            font-weight: 100 !important;
           
            
        }
        [data-testid="stToast"] p {
            font-weight: 500 !important;
            
        }
        
       @keyframes fadeout { 
            from {opacity:100%}
            to {opacity:0%; visibility:hidden;}
       }

       }
    </style>        
"""
,unsafe_allow_html=True)


# Customize upload button global
st.markdown("""
    <style>

        /* εξατόμικευση upload button global */
        .st-key-upload-button-global {
            display: flex !important;
            margin-left:38%;
                            
        }

        /* εξατόμικευση θέσης-μεγέθους */
        .st-key-upload-button-global [data-testid="stFileUploader"] {
            margin-left: 33%; 
            height: 0px !important;
            background-color: blue !important;
            
        }
                
        .st-key-upload-button-global label{
            display:none !important;
        }

        /* εξατομίκεση button (section) */
        .st-key-upload-button-global section{
            background-color: transparent !important;
            display: flex !important; 
            height: 0px !important;
            margin-top: 11%;
        }

        /* αφαίρεση instruction (200 MB etc) */
        [data-testid=stFileUploaderDropzoneInstructions] > div span{ 
            display: none;
        }

        /* εξατομίκεση κουμπιού */
        div.st-key-upload-button-global [data-testid="stFileUploaderDropzone"] button {
            margin-left: 10%;
            font-weight: 500;
            background-color: #151E2A !important;
            box-shadow: none !important;
            
        }
        
        
        /* εξατομίκεση κουμπιού σε state hover */
        div.st-key-upload-button-global [data-testid="stFileUploaderDropzone"] button:hover {
            margin-left: 10%;
            color: white;
            background-color: #151E2A !important;    
        }

        

        /* εξατομίκεση κειμένου μέσα στο κουμπί σε state hover */
        div.st-key-upload-button-global [data-testid="stFileUploaderDropzone"] button:hover div  {
            animation: textScale 0.2s forwards;
        }

        @keyframes textScale {
            from {
                transform: scale(1);
            }
            to {
                transform: scale(1.07);
            }
        }
    </style>
""",unsafe_allow_html=True)


# ================================================================

#                           SIDEBAR

# ================================================================
time.sleep(0.05)


with st.sidebar:

    st.markdown(
        """
            <style>
                /* εξατομίκευση sidebar */
                [data-testid="stSidebar"] {
                    background-color: #0E1117 !important;
                    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
                }
                /* hide collapse sidebar button */
                [data-testid="stSidebarCollapseButton"] {
                    display: none;
                }

                /* εξατομίκευση buttons */
                [data-testid="stSidebar"] div.stButton > button {
                    background-color: transparent !important;
                    color: #8E95A5 !important;
                    border: 1px solid transparent !important;
                    border-radius: 8px !important;
                    padding: 8px 12px !important;
                    font-weight: 500 !important;
                    font-size: 14px !important;
                
                }

                /*  wrapper για τα buttons ώστε να έχουν alignment στα αριστερά */
                [data-testid="stSidebar"] div.stButton > button > div {
                    display: flex !important;
                    justify-content: flex-start !important;
                }


                /* εξατομίκευση hover */
                [data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
                    background-color: rgba(255, 255, 255, 0.04) !important;
                    color: #E2E8F0 !important;
                    border-color: rgba(255, 255, 255, 0.05) !important;
                    transition: all 0.4s linear;
                }

                /* εξατομίκευση επιλεγμένου button  */
                [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
                    background: linear-gradient(90deg, rgba(56, 189, 248, 0.08) 0%, rgba(30, 41, 59, 0.5) 100%) !important;
                    color: #FFFFFF !important;
                    border: 1px solid rgba(56, 189, 248, 0.15) !important;
                    border-left: 3.5px solid #0284C7 !important; /* Vivid Blue Accent */
                    font-weight: 600 !important;
                }

                
                .sidebar-nav-title {
                    font-size: 11px;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    color: #4B5563;
                    padding: 16px 10px 4px 10px;
                    margin: 0;
                }
            </style>
    """,unsafe_allow_html=True,)

  # Logo
    st.markdown("""
        <div style="display:flex; justify-content:left; gap:10px;margin-bottom:20px;border-bottom:1px solid #394353; padding: 4px 6px 20px 6px;">
            <div 
                style="
                display:flex;
                width: 36px;
                height:36px;
                background-color:#1E293B;
                border-radius:9px;
                border:solid 1px #394353;
                align-items:center;
                justify-content:center;
                ">⚡
            </div>
            <div style="font-weight: 600; font-size: 15px;margin-top:5px;">Analytics App</div>
        </div>
        
    """,unsafe_allow_html=True)

  
    def nav_item(label, icon_name, page_target):
        is_active = st.session_state.page == page_target
        if st.button(
            label,
            icon=icon_name,
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.page = page_target
            st.rerun()

    # Dashboard , Costs & Losses navigation
    nav_item("Dashboard", ":material/home:", "Dashboard")
    nav_item("Costs & Losses", ":material/trending_down:", "Costs&Losses")

    # FINANCIALS 
    st.markdown('<p class="sidebar-nav-title">FINANCIALS</p>', unsafe_allow_html=True)
    
    nav_item("Earnings", ":material/trending_up:", "Earnings")
    nav_item("Investments", ":material/finance:", "Investments")

    # Τemplates CSV list
    st.markdown('<p class="sidebar-nav-title">Templates</p>', unsafe_allow_html=True)
    st.markdown("""
        <style>
            /* customize τα donwload buttons για τα templates */
            .st-key-upload-container div[data-testid="stDownloadButton"] button {                       
                background-color: #1E2230 !important;          
                color: #E2E8F0 !important;                     
                border: 1px solid #23262B !important;
                border-radius: 8px !important;                 
            }
        </style>
        
    """, unsafe_allow_html=True)

    # selectbox στο οποίο ο χρήστης επιλέγει ποιό template θέλει να κατεβάσει
    template = st.selectbox(
        "Select template",
        options=["Earnings", "Pending Earnings", "Investments", "Costs", "Losses"],
        accept_new_options=False,
        key="template-selectbox",
        placeholder="Select template",
        index=None
        
    )

    # Ανάλογα με την επιλογή το selectbox, εμφανίζεται το αντίστοιχο κουμπί
    # ώστε να κατεβάσει ο χρήστης το αντίστοιχο CSV
    with st.container(key="download-button-container"):
        if template == "Earnings":
            st.download_button(
                label="Earnings",
                data=utils.download_csv("earnings").to_csv(index=False).encode("utf-8"),
                file_name="earnings.csv",
                mime="text/csv",
                icon=":material/download:",
            )
            
        elif template == "Pending Earnings":
            st.download_button(
                label="Pending Earnings",
                data=utils.download_csv("pearnings").to_csv(index=False).encode("utf-8"),
                file_name="pending_earnings.csv",
                mime="text/csv",
                icon=":material/download:", 
            )
        elif template == "Investments":
            st.download_button(
                label="Ivestments",
                data=utils.download_csv("investments").to_csv(index=False).encode("utf-8"),
                file_name="ivestments.csv",
                mime="text/csv",
                icon=":material/download:", 
            )
        elif template == "Costs":
           
            st.download_button(
                label="Costs",
                data=utils.download_csv("costs").to_csv(index=False).encode("utf-8"),
                file_name="costs.csv",
                mime="text/csv",
                icon=":material/download:", 
            )
        elif template == "Losses":
            st.download_button(
                label="Losses",
                data=utils.download_csv("losses").to_csv(index=False).encode("utf-8"),
                file_name="losses.csv",
                mime="text/csv",
                icon=":material/download:" 
            )
    
    # Eξατομίκεση για το selectbox και τα download buttons
    st.markdown("""
        <style>
            .st-key-template-selectbox div[data-rac][role="group"] {
                border: 0.5px solid #23262B;
                background-color: #171A20;
            }
            .st-key-template-selectbox label { 
                display: none !important;
            }

            .st-key-download-button-container button { 
                background-color: #171A20;
                border: 0.5px solid #23262B;
            }


        </style>
    """, unsafe_allow_html=True)



# upload button 
def upload_button():
    return st.file_uploader("", type="csv",  key="upload-button-global", accept_multiple_files=True)


# upload file container  
def upload_file_container():
# Customize το upload file div
    st.markdown("""
        <style>

            div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: #151D29;
                border: 1px solid rgba(41, 181, 232, 0.25);
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            }
                
            .upload_icon {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 20px;
            }

            .card-title {
                color: #FFFFFF;
                font-size: 26px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 10px;
                line-height: 1.3;
            }

            .card-subtitle {
                color: #9499B3;
                font-size: 14px;
                text-align: center;
                margin-bottom: 25px;
                line-height: 1.5;
            }

                
            
        </style>
    """,unsafe_allow_html=True,)


    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        # μπλέ container
        with st.container(border=True, key="upload-container"):
                
            st.markdown("""
                <!-- μπλέ container το οποίο πειλαμβάνει όλα τα υπόλοιπα elements -->
                <div class="upload_icon">
                    <!-- upload file icon -->
                    <svg width="68" height="68" viewBox="0 0 24 24" fill="none" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0px 0px 18px rgba(120, 119, 240, 0.5));">
                        <path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" />
                        <polyline points="14 2 14 8 20 8" />
                        <path d="M12 18V12" />
                        <path d="M9 15L12 12L15 15" />
                    </svg>
                </div>
                <!-- Title div -->
                <div class="card-title">Welcome to Your Analytics Dashboard</div>
                <!-- Subheader div -->
                <div class="card-subtitle">
                    <span>To get started, please upload your data file (CSV) below.</span>
                    <p>(required costs and earnings CSV)</p>
                    <p>Download a template to get started, fill in your figures, and upload the file.</p>
                </div>

                <style>

                /* εξατομίκευση μπλέ container */
                .st-key-upload-container {
                    background-color: #151D29 !important;
                    display: flex;
                    border: 1px solid rgba(41, 181, 232, 0.3) !important;
                    border-radius: 16px !important;
                    padding: 24px !important;
                    justify-content: center;
                }
                /* εξατόμικευση upload button */
                .st-key-upload-button {
                    justify-content: center !important;
                    align-items: center !important;
                             
                }
                        
                .st-key-upload-button label{
                    display:none !important;
                }

                .st-key-upload-button section {
                    background-color: #151D29 !important;           
                }

                /* εξατόμικευση div στο οποίο περικλείετε το upload button */
                div.st-key-upload-button { 
                    display:flex;
                    text-align:center;
                    justify-content: center;
                }
                </style>
                    
            """,unsafe_allow_html=True,)

            # upload button
            uploaded_file = st.file_uploader("", type=["csv"], key="upload-button", accept_multiple_files=True)
                
            for file in uploaded_file:
                dataframe = pd.read_csv(file)
                    
                # Για κάθε CSV το κάνω format με το module loader
                # ανάλογα με το text το οποίο επιστραφεί εμφανίζεται το αντίστοιχο μήνυμα
                result = loader.add_to_database(dataframe)
                # Περίπτωση όπου τα δεδομένα δεν είναι σωστά
                if result != "data has been added":
                    st.error(body=result)            
                else:
                    
                    st.success("Data has been added successfully")


# ================================================================

#                       DASHBOARD PAGE

# ================================================================





    
def render_dashboard():

    mainc1, _ ,mainc3 = st.columns(3)
    with mainc1:
        st.title("Dashboard")
    
 
    # Περίπτωση όπου οι πίνακες earnings και costs είναι κενοί
    if utils.get_earnings().empty or utils.get_losses_or_costs("costs").empty:
        upload_file_container()
                   
        # σταματάει το πρόγραμμα εδώ εφόσον δεν έχει τα απαρραίτητα δεδομένα
        # έτσι ώστε να εκτυπώσει τα charts και να υπολογίσει τα στατιστικά            
        st.stop()            

    with mainc3:
        uploaded_file = upload_button()

    # Δημιουργεί 5 στήλες (σαν containers) στα οποία χωρίζεται η οθόνη
    c1, c2, c3, c4, c5 = st.columns(5)
    # Customize τα metrics τα οποία εμφανίζονται στο dashboard
    # !important βάζει σε προτεραίοτητα την συγκεκριμένη εντολή έναντι οποιαδήποτε άλλης
    # η οποία εφαρμόζεται σε αυτό το στοιχείο

    st.markdown("""
                <style>
                    [data-testid="stMetricLabel"] p {
                        font-size:15px !important;
                        text-transform: capitalize;
                        
                    }
                </style>
                """
                , unsafe_allow_html=True)

    # METRICS
    with c1:
        with st.container(border=True):
            st.metric(label = f"Gross profit {current_year}", value = f"{database.get_total_gross_profit_year(current_year):,.2f}€", delta=utils.calculate_percentage_difference_year_to_year(database.get_total_gross_profit_year), format="percent", delta_description="vs. last year")
    with c2:
        with st.container(border=True):
            st.metric(label = f"Net profit {current_year}", value = f"{database.get_total_net_profit_of_a_year(current_year):,.2f}€", delta=utils.calculate_percentage_difference_year_to_year(database.get_total_net_profit_of_a_year), delta_description="vs. last year", format="percent")
    with c3:
        with st.container(border=True):
            st.metric(label = f"Total Cost & Losses {current_year}", value = f"{database.get_total_losses_year(current_year)+database.get_total_costs_year(current_year):,.2f}€", format="percent", delta=utils.calculate_percentage_difference_year_to_year(database.get_cost_losses_year), delta_description="vs. last year", delta_color="inverse")
    with c4:
        with st.container(border=True):
            st.metric(label = f"Total losses {current_year}", value = f"{database.get_total_losses_year(current_year):,.2f}€")
    with c5:
        with st.container(border=True):
            st.metric(label = f"Total costs {current_year}", value = f"{database.get_total_costs_year(current_year):,.2f}€")
   

    # Κάτω από τα metrics η οριζόντια γραμμή
    st.divider()    
            

    col1, col2 = st.columns(2)

    # Tα δεδομένα της παρακάτω εντολής είναι σε μορφή : [('.', '.'), ('.', '.'), ('.', '.')]
    gross_profit_for_each_month = database.get_gross_profits_each_month_of_a_year(current_year)
    
    # GROSS PROFIT IS 0 
    if not gross_profit_for_each_month:
        st.toast(body=" Gross profit for the current year is 0", icon="⚠️", duration="infinite")
        
    # Για να μετατρέψω την παραπάνω λίστα σε 2 μοναδικές λίστες αρκεί
    # να πάρω το πρώτο και δεύτερο στοιχείο από το κάθε tuple και να το προσθέσω σε 
    # κάθε λίστα αντίστοιχα
    # Για κάθε element ('.', '.') της λίστας πάρε το πρώτο στοιχείο του tuple
    # και εκχώρησε το στην λίστα months
    months = [calendar.month_abbr[int(element[0])] for element in gross_profit_for_each_month]#calendar.month_abbr μετατρέπει τα 01,02 σε jan, feb etc
    profit = [element[1] for element in gross_profit_for_each_month]
    profit = [f"{element:.2f}" for element in profit]

    total_costs_losses_each_month = database.get_cost_losses_each_month_of_a_year(current_year)
    
    # COSTS & LOSSES ARE 0
    if not total_costs_losses_each_month:
        st.toast(body=" Costs&Losses for the current year are 0", icon="⚠️", duration="infinite")
        st.stop()
    
    months2 = [calendar.month_abbr[int(element[0])] for element in total_costs_losses_each_month]
    cost_losses = [element[1] for element in total_costs_losses_each_month]
    cost_losses = [f"{element:.2f}" for element in cost_losses]
    
    # Bar chart για gross profits per month
    
    with col1:
        with st.container(border=True):
            st.subheader("Profits per month (Gross)")
            bar = px.bar(
                            x=months, y=profit,
                            text=profit,
                            color_discrete_sequence=["#3B82F6"],
                            labels = {
                                "x" : "Month",
                                "y": "Profit"
                            }
                        )
            bar.update_xaxes(title_font_size=22, tickfont_size=17)
            bar.update_yaxes(title_font_size=22, tickfont_size=17)
            bar.update_traces(textposition="outside",  marker_cornerradius=10, textfont_size=15)
            st.plotly_chart(bar)

    
    

    # Bar chart για cost&losses per month         
    with col2:
        with st.container(border=True):
            st.subheader("Costs & Losses per month")
            bar = px.bar(
                x= months2, y=cost_losses,
                text=cost_losses,
                color_discrete_sequence=["#3B82F6"],
                labels={
                    "x" : "Month",
                    "y" : "Costs & Losses"
                }
            )
            bar.update_xaxes(title_font_size=22, tickfont_size=17)
            bar.update_yaxes(title_font_size=22, tickfont_size=17)

            bar.update_traces(textposition="outside", marker_cornerradius=10, textfont_size=15)
            st.plotly_chart(bar)





# =================== search function ===================


@st.dialog("search query", width="large")
def render_search_query(search_query):
    # search feature για την costs&losses σελίδα
    if st.session_state.page == "Costs&Losses":
        if st.session_state.show_costs:
            dataframe_costs = utils.get_losses_or_costs("costs")
            results  = dataframe_costs[dataframe_costs["DESCRIPTION"].str.contains(search_query, case=False, na=False)]     
        else:
            dataframe_losses= utils.get_losses_or_costs("losses")
            results  = dataframe_losses[dataframe_losses["DESCRIPTION"].str.contains(search_query, case=False, na=False)]
        edited_df = st.data_editor(
            results, 
            num_rows="delete",
            column_config={
                            "DATE" : st.column_config.DateColumn(format="DD-MM-YYYY"),
                            "ID": None
                        }, 
            hide_index=True,
        
        )
    # search feature για την earnings σελίδα
    elif st.session_state.page == "Earnings":
        dataframe_earnings = utils.get_earnings()
        results  = dataframe_earnings[dataframe_earnings["DESCRIPTION"].str.contains(search_query, case=False, na=False)]        
        edited_df = st.data_editor(
            results, 
            num_rows="delete",
            column_config={
                            "DATE" : st.column_config.DateColumn(format="DD-MM-YYYY"),
                            "ID": None
                        }, 
            hide_index=True, column_order=['DATE', 'CATEGORY', 'PROFIT', 'DESCRIPTION', 'ROI', 'NOTES']
        
        )
    elif st.session_state.page == "Investments":
        dataframe_investments = utils.get_investments()
        results  = dataframe_investments[dataframe_investments["DESCRIPTION"].str.contains(search_query, case=False, na=False)]        
        edited_df = st.data_editor(
            results, 
            num_rows="delete",
            column_config={
                            "DATE" : st.column_config.DateColumn("Date",format="DD-MM-YYYY"),
                            "ID": None
                        }, 
            hide_index=True,
        
        )





# ================================================================

#                       COSTS & LOSSES PAGE

# ================================================================





# Φόρμα καταχώρησης νέου entry 
# χρησιμοποιώ τον built-in decorator @st.dialog της Streamlit,
# ο οποίος μετατρέπει τη συνάρτηση open_add_cost_entry_form σε pop-up παράθυρο,
# όταν καλείται η συνάρτηση, το περιεχόμενό της (το st.form) 
# απομονώνεται και προβάλλεται μέσα στο pop-up.
@st.dialog("Add cost")
def open_add_cost_entry_form():
    with st.form("add cost"):
        date = st.date_input("Date")
        category = st.selectbox(
            label = "Select Category", options=utils.get_categories(database.get_costs_categories),index=0,
            accept_new_options = True, help="Select/Add Category"
        )  
        cost = st.number_input("Amount (€)", min_value=0.0)
        description = st.text_input("Description")
        notes = st.text_input("Notes")
        
        submit = st.form_submit_button("Add")
        
            
        if submit:
            database.add_cost_entry(date, cost, description, category, notes)
            st.rerun()


          
# Φόρμα καταχώρησης loss entry
@st.dialog("Add loss")
def open_add_loss_entry_form():
    with st.form("add loss"):
        date = st.date_input("Date")
        category = st.selectbox(
            label = "Select Category", options=utils.get_categories(database.get_losses_categories), index=0,
            accept_new_options = True, help="Select/Add Category"
        )         
        loss = st.number_input("Amount (€)", min_value=0.0)
        description = st.text_input("Description")
        notes = st.text_input("Notes")
         
        submit = st.form_submit_button("Add")
            
        if submit:
            database.add_loss_entry(category, loss, description, date, notes)
            st.rerun()





# Η παρακάτω μεταβλητή χρησιμοποιείτε ώστε να εμφανίζεται
# είτε ο πίνακας costs είτε ο πίνακας losses
# όταν είνα Τrue εμφανίζεται ο costs αντίθετα ο losses
if "show_costs" not in st.session_state:
    st.session_state.show_costs = True

# Αλλάζει την τιμή της st.session_state.show_costs
# το not χρησιμοποιείτε ώστε να αντιστρέφεται η τιμή,
# μια καθολική τιμή όπως : st.session_state.show_costs = False
# θα επέφαιρε πάντα το ίδιο αποτέλεσμα
def toggle_button_label():
    st.session_state.show_costs = not st.session_state.show_costs







def render_costs_losses():
    
    mainc1, _ ,mainc3 = st.columns(3)
    with mainc1:
        st.title("Costs & Losses")

    # Περίπτωση όπου οι πίνακες costs και losses είναι κενοί 
    if not(database.get_costs() or database.get_losses()):
        upload_file_container()
        st.stop()

    with mainc3:
        uploaded_file = upload_button()

    c1, c2 = st.columns([6, 1.5], vertical_alignment="bottom")
    
    with c1:
            
        searchc, tablec, exportc = st.columns([10,1.8,1.8], vertical_alignment="bottom")
        # Search form
        with searchc:
            with st.form("form", border=False):
                # Κάνω hide τα instruction τα οποία δίνει το streamlit στο text input (search query)
                st.markdown(
                    """
                    <style>
                        div[data-testid="stTextInput"] [data-testid="InputInstructions"] {
                            display: none;
                        }
                    </style>
                    """
                    ,unsafe_allow_html=True)
                fc1, fc2 = st.columns(2)
                with fc1:
                    search_query = st.text_input("Search entry", placeholder="Filter by description", label_visibility="collapsed")
                with fc2:
                    submit_button = st.form_submit_button("search")
            if submit_button and search_query.strip():
                render_search_query(search_query)

        # Tables costs & losses
        with tablec:
            # Ανάλογα με την τιμή του st.session_state.show_costs παρουσιάζεται
            # ο αντίστοιχος πίνακας, παρακάτω ορίζεται το κείμενο που εμφανίζεται στο
            # κουμπί το οποίο είναι υπεύθυνο για την εναλλαγή μεταξύ των πινάκων    
            if st.session_state.show_costs:
                label = "Show Losses"
            else:
                label = "Show Costs"
            # Όταν ο χρήστης πατάει το παρακάτω κουμπί καλείτε η toggle_button_label
            st.button(label, on_click=toggle_button_label)
            if (st.session_state.show_costs):
                with c1:
                    # Εμφάνησε τον πίνακα costs

                    # Στην dataframe_costs επιστρέφεται ο πίνακας μέσω της get_losses_or_costs,
                    # όπου ανάλογα την τιμή της παραμέτρου επιλέγει ποιόν πίνακα να επιστρέψει
                    dataframe_costs = utils.get_losses_or_costs("costs")
                    if dataframe_costs.empty:
                        st.write("There are no data.")
                    else:
                        edited_df = st.data_editor(
                            dataframe_costs, 
                            num_rows="delete",
                            height=685,
                            disabled=list(dataframe_costs.columns.values),
                            column_config={
                                            "DATE" : st.column_config.DateColumn(format="DD/MM/YYYY"),
                                            "ID" : None
                                        }, 
                            hide_index=True, column_order=["DATE", "DESCRIPTION", "COST", "CATEGORY", "NOTES"]
                        )
                        # Άφοτου ο χρήστης διαγράψει ένα entry μέσω του UI (data_editor), επιστρέφεται στην 
                        # edited_df το καινούργιο dataframe χωρίς το row το οποίο διαγράφτηκε
                        # Οπότε για να εντοπίσω ποιό row(s) διαγράφτηκε ακολουθώ τα παρακάτω βήματα :
                        # 1) αρκέι να μεταρέψω τα ID του καινούργιου και του παλιού dataframe σε λίστες
                        # 2) μετατρέπω τις λίστες σε sets
                        # 3) Αποθηκεύω τα σβησμένα ids στην deleted_ids μέσω της αφαίρεσης των sets
                        # (η αφαίρεση επιστρέφει όλα τα ids τα οποία υπάρχουν στην dataframe_costs αλλά δεν υπάρχουν στην edited_df)
                        deleted_ids = set(dataframe_costs['ID'].to_list()) - set(edited_df['ID'].to_list())
                        if deleted_ids:
                            for id in deleted_ids:
                                database.delete_cost_entry(id)
                            st.rerun()    
            else:
                with c1:
                    # Εμφάνησε τον πίνακα losses
                    dataframe_losses = utils.get_losses_or_costs("losses")
                    if dataframe_losses.empty:
                        st.write("There are no data.")
                    else:
                        edited_df = st.data_editor(
                            dataframe_losses, 
                            num_rows="delete",
                            height=685,
                            disabled=list(dataframe_losses.columns.values),
                            column_config={
                                            "DATE" : st.column_config.DateColumn(format="DD/MM/YYYY"),
                                            "ID" : None
                                        }, 
                            hide_index=True, column_order=["DATE", "DESCRIPTION", "LOSS", "CATEGORY", "NOTES"]
                            
                        )
                        deleted_ids = set(dataframe_losses['ID'].to_list()) - set(edited_df['ID'].to_list())
                        if deleted_ids:
                            for id in deleted_ids:
                                database.delete_loss_entry(id)
                            st.rerun()
        # Export κουμπί
        with exportc:
            if st.session_state.show_costs:
                dataframe_costs = utils.get_losses_or_costs("costs")
                st.download_button(
                    "⬇️ Export",
                    dataframe_costs.to_csv(index=False),
                    file_name="costs.csv",
                    mime="text/csv",
                    key="export_costs"
                )
            else:
                dataframe_losses = utils.get_losses_or_costs("losses")
                st.download_button(
                    "⬇️ Export",
                    dataframe_losses.to_csv(index=False),
                    file_name="losses.csv",
                    mime="text/csv",
                    key="export_losses"
                )
        
        
        
            
    with c2:
       
        # Πρόσθεσε entries στους πίνακες costs και losses             
        subc1, subc2 = st.columns([0.8,0.8])
        
        with subc1:
            if st.button("➕ Add Cost", type="secondary"):
                open_add_cost_entry_form()
        with subc2:
            if st.button("➕ Add Loss", type="secondary"):
                open_add_loss_entry_form()
        # METRICS
        
        with st.container(border=True):
            st.metric("Total Costs & Losses", f"{database.get_total_losses_year() + database.get_total_costs_year():,.2f}€", delta=utils.calculate_percentage_difference_for_costs_and_losses(), format="percent", delta_description="vs. last years", delta_color="inverse")
        with st.container(border=True):
            st.metric("Total Costs", f"{database.get_total_costs_year():,.2f}€",  delta=utils.calculate_percentage_difference_for_costs(), format="percent", delta_description="vs. last years", delta_color="inverse")
        with st.container(border=True):
            st.metric("Total Losses", f"{database.get_total_losses_year():,.2f}€",   delta=utils.calculate_percentage_difference_for_losses(), format="percent", delta_description="vs. last years", delta_color="inverse")

       



    barcol1, barcol2 = st.columns(2)
    
    CONTAINER_HEIGHT = 700
    # Bar chart για Costs & Losses per year
    with barcol1:
        with st.container(border=True, height=CONTAINER_HEIGHT):
            data = database.get_cost_losses_2_columns()
            data = pd.DataFrame(data, columns=['YEAR', 'COST', 'LOSS']).set_index("YEAR")
            st.subheader("Costs & Losses Per Year")
            st.bar_chart(
                data,
                color=["#4F8CFF", "#10B981"],  
                height=600,
                width="stretch",
                horizontal=True, 
            )

    
                




# ================================================================

#                       EARNINGS PAGE

# ================================================================




# Χρησιμοποιώ την calc_res ώστε να παραμένει στο UI
# το αποτέλεσμα του calculator, χωρίς αυτήν την μεταβλητή
# κάθε φορά που ο χρήστης αλληλεπιδρά με το UI το πρόγραμμα κάνει
# rerun, οπότε όλα τα δεδομένα που αποθηκεύονται στον κώδικα του UI σβήνονται.
if "calc_res" not in st.session_state:
    st.session_state.calc_res = None
# Η παρακάτω if εφαρμόζεται όταν ο χρήστης έχει ήδη χρησιμοποιείσει το calculator,
# όταν αλλάζει σελίδα γίνεται True, οπότε όταν επιστρέψει ξανά στην σελίδα Earnings
# δεν θα εμφανίζεται το αποτέλεσμα της προηγούμενης πράξης.
elif st.session_state.page != "Earnings":
    st.session_state.calc_res = None


# Ίδια λογική με το calculator, αλλά με περισσότερα metrics
if "net_profit" not in st.session_state:
    st.session_state.net_profit = None
    st.session_state.roi = None
    st.session_state.annualized_roi = None
elif st.session_state.page != "Earnings":
    st.session_state.net_profit = None
    st.session_state.roi = None
    st.session_state.annualized_roi = None    

# Χρησιμοποιώ την παρακάτω μεταβλητή ώστε να κάνω reset το id_selection = st.selectbox,
# στην περίπτωση όπου το immediate_transfer = False, παρουσιάζεται ένα form
# το οποίο πρέπει να συμπληρώσει ο χρήστης ώστε να γίνει η μεταφορά των δεδομένων στον
# πίνακα earnings σε περίπτωση όπου ο χρήστης δεν κάνει submit το form η τιμή στο selectbox παραμένει
# με αποτέλεσμα εαν ο χρήστης χρησιμοποιείσει οποιοδήποτε στοιχείο του UI(earnings) το οποίο κάνει generate ένα
# st.dialog να εμφανίζεται error καθώς δεν μπορούν να τρέχουν ταυτόχρονα 2 st.dialog
if "multiselect_version" not in st.session_state:
    st.session_state.multiselect_version = 0

# Η παρακάτω function αλλάζει το key του widget id_selection = st.selectbox,
def increment_key_for_multiselect():
    st.session_state.multiselect_version += 1

# Χρησιμοιποιείτε ώστε να αλλάζει το interface
# του roi calculator ανάλογα με την επιλογή του
# χρήστη ως προς τον τρόπο υπολογισμού του.
if "dates" not in st.session_state:
    st.session_state.dates = True


def dates_or_lenght():
    st.session_state.dates = not st.session_state.dates



# Φόρμα καταχώρησης earning entry
# θέτωντας τις παραμέτρους ως None η function καλείτε
# με αλλά και χωρίς παραμέτρους εφόσον χρησιμοποιώ 2 φορες την συγκερκιμένη φόρμα
# διαφοροποιώ τις περιπτώσεις που χρησιμοποιώ την φορμά ανάλογα με τις παρμέτρους
# που έχουν ή οχι περαστεί στο κάλεσμα της.
@st.dialog("Add earning")
def open_add_earning_entry_form(id_selection=None, profit_p=None, description_p=None, roi_p=None, notes_p=None, date_p=None):
    with st.form("add earning"):
        # Ορίζοντας ως default τιμή των παραμέτρων το None, η function υποστηρίζει διπλή χρήση:
        # 1) Χωρίς παραμέτρους: Τα πεδία παραμένουν κενά/αρχικά για νέα χειροκίνητη καταχώρηση.
        # 2) Με παραμέτρους: Τα πεδία προ-συμπληρώνονται (pre-fill) με δεδομένα (π.χ. από pending entry)
        # επιτρέποντας στον χρήστη να τα ελέγξει ή να τα τροποποιήσει πριν την οριστική αποθήκευση.
        if not date_p:
            date_p = datetime.today()
        if not profit_p:
            profit_p = 0.0
        if not roi_p:
            roi_p = 0.0

        date = st.date_input("Date", value = date_p)
        category = st.selectbox(
            label = "Select Category", options=utils.get_categories(database.get_earnings_categories),index=0,
            accept_new_options = True, help="Select/Add Category"
        )         
        profit = st.number_input(label = "Net Profit (€)", min_value=0.0,  value = profit_p)
        description = st.text_input(label = "Description", value = description_p)
        roi = st.number_input(label = "ROI", value = roi_p)
        
        notes = st.text_input(label = "Notes", value = notes_p)
         
        submit = st.form_submit_button("Add")
            
        if submit:
            database.add_earning_entry(category, profit, description, roi, notes, date)
            # Στην περίπτωση όπου το form έγινε generated από την μεταφορά entry.
            
            if id_selection!=None:
                database.delete_pending_earning_entry(id_selection)
            st.rerun() 

# Φόρμα καταχώρησης pending earning entry
@st.dialog("Add pending earning")
def open_add_pending_earning_entry_form():
    st.markdown(
                """
                <style>
                    div[data-testid="stTextInput"] [data-testid="InputInstructions"] {
                        display: none;
                    }
                </style>
                """
    ,unsafe_allow_html=True)

    with st.form("add pending earning"):
        date = st.date_input("Date")
        category = st.selectbox(
            label = "Select Category", options=utils.get_categories(database.get_pending_earnings_categories),index=0,
            accept_new_options = True, help="Select/Add Category"
        )         
        profit = st.number_input("Net Profit (€)", min_value=0.0)
        description = st.text_input("Description")
        roi = st.number_input("ROI")
        immediate_transfer = st.toggle("Immediate Transfer", value=True, key="immediate_transfer_toggle")
        notes = st.text_input("Notes")
         
        submit = st.form_submit_button("Add")
            
        if submit:
            database.add_pending_earning_entry(category, profit, description, roi, notes, date, immediate_transfer)
            st.rerun()


def render_earnings():
    # Κάνω hide τα instruction τα οποία δίνει το streamlit στο text input (search query)
    st.markdown(
    """
    <style>
        div[data-testid="stTextInput"] [data-testid="InputInstructions"] {
            display: none;
        }
    </style>
    """
    ,unsafe_allow_html=True)
    
    st.title("Earnings")
    m1, m2, m3 = st.columns(3)   
    # METRICS
    with m1:
        
        with(st.container(border=True)):
            st.metric("Total Gross Profit", f"{database.get_total_gross_profit_year():,.2f}€", delta=utils.calculate_percentage_difference_for_gross_profit(), format="percent", delta_description="vs. all past years")
    with m2:
        
        with st.container(border=True):
            st.metric("Total Net Profit", f"{database.get_total_net_profit_of_a_year():,.2f}€", delta=utils.calculate_percentage_difference_for_net_profit(), format="percent", delta_description="vs. all past years")  
    st.divider()

    top_left_col, top_right_col = st.columns([5, 4], vertical_alignment="bottom")
    with top_left_col:
        
        search_col, btn_col1, btn_col2 = st.columns([6.5, 2.2, 1.6], vertical_alignment="bottom")
        with search_col:
            with st.form("form", border=False):
                
                fc1, fc2 = st.columns(2)
                with fc1:
                    search_query = st.text_input("Search entry", placeholder="Filter by description", label_visibility="collapsed")
                with fc2:
                    submit_button = st.form_submit_button("search")
            if submit_button and search_query.strip():
                render_search_query(search_query)
            
        with btn_col1:     
            if st.button("➕ Add Earnings", type="secondary"):
                open_add_earning_entry_form()
        with btn_col2:
            dataframe_earnings = utils.get_earnings()
            st.download_button(
                "⬇️ Export",
                dataframe_earnings.to_csv(index=False),
                file_name="earnings.csv",
                mime="text/csv",
                key="export_losses"
            )
    

         
                    
    body_left, body_right = st.columns([5, 4])

    with body_left:
        # Earnings table
        if dataframe_earnings.empty:
            st.write("There are no data.")
        else:
            edited_df = st.data_editor(
                dataframe_earnings, 
                num_rows="delete",
                height=650,
                disabled=list(dataframe_earnings.columns.values),
                column_config={
                                "DATE" : st.column_config.DateColumn(format="DD/MM/YYYY"),
                                "ID" : None,
                                "ROI": st.column_config.ProgressColumn(min_value=0, max_value=100)
                            }, 
                hide_index=True, column_order=['DATE', 'CATEGORY', 'PROFIT', 'DESCRIPTION', 'ROI', 'NOTES']
            )


            deleted_ids = set(dataframe_earnings['ID'].to_list()) - set(edited_df['ID'].to_list())
            if deleted_ids:
                for id in deleted_ids:
                    database.delete_earning_entry(id)
                st.rerun()

        # Area chart για Earnings vs. Costs & Losses 
        with body_right:
            
            with st.container(border=True):
                st.subheader("Earnings vs. Costs & Losses (Annual Comparison)")

                # Συνολικό gross profit για κάθε χρόνο 
                data_gross = database.get_gross_profit_each_year()
                # Συνολικό πόσο για costs & losses για κάθε χρόνο
                data_costs = database.get_cost_losses_each_year()

                # περιέχει μόνο το costs&losses ποσό
                data_costs_list = [element[1] for element in data_costs]
                if not data_costs_list:
                    st.write("please add cost losses")
                    st.stop()
                dataframe_earnigns_cost_losses = pd.DataFrame(data_gross, columns=['YEAR', 'EARNINGS'])
                
                dataframe_earnigns_cost_losses['COSTS_LOSSES'] = data_costs_list
                fig = go.Figure()
                # --- EARNINGS LINE ---
                fig.add_trace(
                    go.Scatter(
                        x=dataframe_earnigns_cost_losses["YEAR"],
                        y=dataframe_earnigns_cost_losses["EARNINGS"],
                        name="Earnings",
                        mode="lines+markers",
                        line=dict(color="#10B981", width=3.5, shape="spline"),
                        marker=dict(size=8, color="#10B981", symbol="circle"),
                        fill="tozeroy",
                        fillcolor="rgba(16, 185, 129, 0.08)",
                        hovertemplate="<b>Earnings</b><br>Year: %{x}<br>Amount: %{y:,.2f}€<extra></extra>",
                    )
                )
                # --- COSTS & LOSSES LINE ---
                fig.add_trace(
                    go.Scatter(
                        x=dataframe_earnigns_cost_losses["YEAR"],
                        y=dataframe_earnigns_cost_losses["COSTS_LOSSES"],
                        name="Costs & Losses",
                        mode="lines+markers",
                        line=dict(color="#FB7185", width=3.5, shape="spline"),
                        marker=dict(size=8, color="#FB7185", symbol="circle"),
                        fill="tozeroy",
                        fillcolor="rgba(251, 113, 133, 0.08)",
                        hovertemplate="<b>Costs & Losses</b><br>Year: %{x}<br>Amount: %{y:,.2f}€<extra></extra>",
                    )
                )
                # Customization του chart
                fig.update_layout(
                    height=557,
                    hovermode="x unified",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(
                        type="category",
                        tickangle=0,
                        tickfont=dict(size=14, color="#94A3B8"),
                        showgrid=False,
                        showline=True,
                        linecolor="#334155",
                    ),
                    yaxis=dict(
                        tickfont=dict(size=13, color="#94A3B8"),
                        showgrid=True,
                        gridcolor="#1E293B",
                        zeroline=True,
                        zerolinecolor="#334155",
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        font=dict(size=14, color="#E2E8F0"),
                    ),
                )

                # rendering chart
                st.plotly_chart(fig, use_container_width=True)
    
    
    with st.container(border=True):
        # Πίνακας PENDING_EARNINGS
        table_pending_earnings = database.get_pending_earnings()
        # Customize το "➕ Add pending earning" κουμπί 
        st.markdown("""
                    <style>
                        
                        div[class*="st-key-Add_pending_earning_button"] button {
                            border: none !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)
        # --- Empty State ---
        if  not table_pending_earnings:
            st.markdown(
                            """
                                <div style="
                                    display: flex;
                                    flex-direction: column;
                                    align-items: center;
                                    justify-content: center;
                                    margin: 20px 0;
                                    border-radius: 14px;
                                    text-align: center;
                                ">
                                    <div style="
                                        width: 64px;
                                        height: 64px;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        border-radius: 50%;
                                        background: rgba(41, 181, 232, 0.1);
                                        border: 1px solid rgba(41, 181, 232, 0.25);
                                        font-size: 28px;
                                        margin-bottom: 16px;
                                        margin-right:10px;
                                    ">
                                        📊
                                    </div>
                                    <h3 style="color: #f3f4f6; font-size: 18px; font-weight: 600; margin-left:20px;">
                                    No pending earnings found</h3>
                                    <p style="
                                        margin: 0;
                                        color: #9ca3af;
                                        font-size: 17px;
                                        max-width: 320px;
                                        line-height: 1.5;
                                    ">There are currently no records tracked in this table.</p>
                                </div>
                """,unsafe_allow_html=True,)
            
            btnc1, btc2 = st.columns([4,5.4],)
            with btc2:
                if st.button("➕ Add pending earning", key="Add_pending_earning_button"):
                    open_add_pending_earning_entry_form()
        else:
            
            dataframe_pending_entries = utils.get_pending_earnings()     
            total_profit = dataframe_pending_entries["PROFIT"].sum()
            
            st.markdown("""
                                <div style="
                                    display: flex;
                                    align-items: center;
                                    gap: 10px;
                                    margin: 16px 0 10px 0;
                                    border-left: 3px solid #f97316;
                                    padding-left: 10px;">
                                    <h3 id="pending_earnings" style="
                                        margin: 0;
                                        color: #f9fafb;
                                        font-size: 1.15rem;
                                        font-weight: 600;
                                        letter-spacing: -0.01em;">Pending Earnings</h3>
                                    <span style="
                                        font-size: 0.72rem;
                                        font-weight: 500;
                                        padding: 2px 7px;
                                        border-radius: 999px;
                                        background: rgba(249, 115, 22, 0.12);
                                        color: #fb923c;
                                        border: 1px solid rgba(249, 115, 22, 0.25);">Unsettled</span>
                                </div>
                            """,unsafe_allow_html=True,)
            
            st.caption("Entries not yet committed to the database.")
             
            col1, col2, col3, col4 = st.columns([3,4, 1.5, 1.5], vertical_alignment="bottom")
            # METRICS
            with col1:
                st.metric("Pending Profit", f"{total_profit:,.2f}€")
            with col2:
                st.metric("Awaiting Sales", value=dataframe_pending_entries.shape[0])
            with col3:
                if st.button("➕ Add pending earning", key="Add_pending_earning_button"):
                    open_add_pending_earning_entry_form()
            with col4:
                # Επιλογή μεταφοράς entry από τον πίνακα PENDGING_EARNINGS
                # στον EARNINGS    
                id_selection = st.selectbox(
                    label="➡️ Settle to Earnings",
                    options=dataframe_pending_entries["ID"].to_list(),
                    placeholder="Select entries to settle...",
                    index=None,
                    # παράμετρος με την οποία ρυθμίζεται η εμφάνιση των επιλογών
                    format_func=lambda id_val: f"{id_val} - {dataframe_pending_entries.loc[dataframe_pending_entries['ID'] == id_val, 'DESCRIPTION'].values[0]}",
                    help="Selected pending records will be committed to realized earnings.",
                    key=f"settle_select_{st.session_state.multiselect_version}"
                    )
                
                # Περίπτωση όπου ο χρήστης έχει επιλέξει το entry από το st.selectbox
                # το οποίο θέλει να μεταφέρει στον πίνακα earnings
                if id_selection != None:
                    # Στο row βρίσκεται η επιλογή του χρήστη
                    row = dataframe_pending_entries.loc[dataframe_pending_entries["ID"] == id_selection]
                    
                    # Αν η στήλη IMMEDIATE_TRANSFER == True, δεν χρειάζονται περαιτέρω επεξεργασία τα δεδομένα για την μεταφορά.
                    if row["IMMEDIATE_TRANSFER"].iloc[0] == True:
                        # το row["DATE"] είναι datetime object, η sql περνάει τα
                        # dates ως strings οπότε το μεταρέπω σε string πριν το περάσω στην βάση
                        # με την database.add_earning_entry το date() επιστρέφει μόνο την ημερομηνία
                        # και σβήνει το time
                        date = str(row["DATE"].iloc[0].date())
                        
                        database.add_earning_entry(
                            row["CATEGORY"].iloc[0],
                            row["PROFIT"].iloc[0],
                            row["DESCRIPTION"].iloc[0],
                            row["ROI"].iloc[0],
                            row["NOTES"].iloc[0],
                            date,
                        )

                        database.delete_pending_earning_entry(id_selection)
                        st.rerun()

                    # Το entry χρειάζεται περαιτέρω επεξεργασία οπότε
                    # ανοίγει το form για να συμπληρωθούν τα δεδομένα
                    else:
                        
                        open_add_earning_entry_form(id_selection, row["PROFIT"].iloc[0], row["DESCRIPTION"].iloc[0], row["ROI"].iloc[0], row["NOTES"].iloc[0], row["DATE"].iloc[0])
                        # Καθέ φορα όπου αλλάζει το key του widget γίνεται εκ νέου
                        # generate το st.selectbox οπότε δεν κρατάει την πάλια του τιμή
                        # άρα ξαναεπιστρέφει στον index = None, οπότε δεν συμπίτπτουν
                        # δύο st.dialog ταυτόχρονα.
                        increment_key_for_multiselect()
            # Πίνακα pendings_earnings
            edited_df = st.data_editor(
                dataframe_pending_entries,
                hide_index=True,
                num_rows="delete",
                column_order=["ID", "PROFIT", "DESCRIPTION", "ROI", "DATE", "NOTES"],
                column_config={
                    "PROFIT": st.column_config.Column(
                        "PROFIT EST."
                    ),
                    "ROI": st.column_config.ProgressColumn(
                        min_value=0,
                        max_value=100,
                        format="%.1f"
                    ),
                    "DATE": st.column_config.DateColumn("DATE OF SALE",format="DD/MM/YYYY",),
                    "CATEGORY": None,
                },
            )
            deleted_ids = set(dataframe_pending_entries['ID'].to_list()) - set(edited_df['ID'].to_list())
            if deleted_ids:
                for id in deleted_ids:
                    database.delete_pending_earning_entry(id)
                    st.rerun()


    # ROI Calculator και Calculator
    
    roi, calc = st.columns(2)
    with roi:
        with st.container(border=True):
            st.subheader("ROI Calculator")
            # Menu button από το οποίο επιλέγει ο χρήστης με ποιό τρόπο θα υπολογιστεί το annualized ROI
            time_mode = st.menu_button(
                "Investment time",
                options=["Use Dates", "Use Length"],
                icon="⏰", on_click=dates_or_lenght
            )
            # ROI calculator
            with st.form("roi_calculator_form", border=False, enter_to_submit=False):
                amount_invested = st.number_input("Amount Invested (€)", min_value=0.0, width=200)
                total_amount_received = st.number_input("Amount Returned (€)", min_value=0.0, width=200)

                # Aλλάζει δυναμικά με βάση την επιλογή του χρήστη
                if st.session_state.dates:
                    time_length = None
                    datecol1, datecol2 = st.columns([1,2])
                    with datecol1:
                        starting_date = st.date_input("From",width=180, value="2026-01-01")
                    with datecol2:
                        last_date = st.date_input("To",width=180, value="today")
                else:
                    last_date = 2
                    starting_date = 1
                    time_length = st.number_input("Investment Length (years)", value=1.0 ,min_value=0.0, step=0.5, width=200)
                submitted = st.form_submit_button("Calculate")
            # Workflow υπολογισμού ROI ανάλογα με την επιλογή του χρήστη
            if submitted and amount_invested != 0.0 and time_length != 0.0 and (last_date >= starting_date):
                if st.session_state.dates:
                    days = (last_date - starting_date).days
                    time_years = max(days / 365.25, 0.001)
                else:
                    time_years = max(float(time_length), 0.001)
                net_profit = total_amount_received - amount_invested
                roi = (net_profit / amount_invested) * 100
                annualized_roi = (((total_amount_received / amount_invested) ** (1 / time_years)) - 1) * 100
                st.session_state.net_profit = net_profit
                st.session_state.roi = roi
                st.session_state.annualized_roi = annualized_roi
            # Pop up μηνύματα σε περίπτωση όπου ο χρήστης δεν έχει εισχωρήσει σωστά τα δεδομένα 
            elif submitted and amount_invested == 0.0:
                st.toast(body=" Amount Invested must be greater than zero!", icon="⚠️", duration="infinite")
            elif submitted and time_length == 0.0:
                st.toast(body=" Investment Length must be greater or equal to 1.0", icon="⚠️", duration="infinite")
            elif submitted and (last_date < starting_date):
                st.toast(body=" The 'To' date cannot be before the 'From' date!", icon="⚠️", duration="infinite")

            # Αποτέλεσματα
            if st.session_state.net_profit != None: 
                net_profit = 0
                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.metric("Net Profit", f"{st.session_state.net_profit:,.2f}€", delta=f"{st.session_state.net_profit:,.2f}€", border=True)
                with col_res2:
                    st.metric("ROI (%)", f"{st.session_state.roi:.2f}%", delta=f"{st.session_state.roi:.2f}%", border=True)
                with col_res3:
                    st.metric("Annualized ROI (%)", f"{st.session_state.annualized_roi:.2f}%", delta=f"{st.session_state.annualized_roi:.2f}%", border=True)

    with calc:
        with st.form("calculator", border=True, enter_to_submit=False):
            st.subheader("Calculator")
            st.caption("Availiable functions: additon(+), substraction(-), multiplication(×)")
            first_number = st.number_input("",width=200, key="first_number")
            second_number = st.number_input("",width=200, key="second_number")
            option_map = { 
                "+" : "addition",
                "-": "substraction",
                "×": "multiplication",
                "÷": "division"
            }

            func_choice = st.pills("Select an operation", option_map, selection_mode="single")
            submitted = st.form_submit_button("Calculate")

            if submitted and func_choice != None:
                result = 0
                if option_map[func_choice] == "addition":
                    result = first_number + second_number
                elif option_map[func_choice] == "substraction":
                    result = first_number - second_number
                elif option_map[func_choice] == "multiplication":
                    result = first_number * second_number
                elif option_map[func_choice] == "division":
                    result = first_number / second_number
                st.session_state.calc_res = result
            
            if st.session_state.calc_res != None:
                st.metric(label="Result", value=f"{st.session_state.calc_res:,.2f}", border=True, width=200)
            if submitted and func_choice == None:
                st.toast(body="Select a calculation method...",  icon="⚠️", duration="infinite")
    

            
   

    barcol1, barcol2 = st.columns(2)    

    # Βar chart για Gross Profits per year

    with barcol1:
        with st.container(border=True):
            data = database.get_gross_profit_each_year()
            year = [element[0] for element in data]
            profits = [element[1] for element in data]
            profits = [f"{element:,.2f}" for element in profits]
            st.subheader("Gross Profits per year")
            figure = px.bar(
                x=year,y=profits,
                text=profits,
                color_discrete_sequence=["#3B82F6"],
                labels = {
                    "x": "Year",
                    "y": "Gross Profit"
                }
            )
            figure.update_yaxes(title_font_size=22, tickfont_size=17)
            figure.update_xaxes(title_font_size=22, tickfont_size=17)
            figure.update_traces(textposition="outside", textfont_size=15, marker_cornerradius=10)
            st.plotly_chart(figure)   

            

    # Βar chart για Net Profit per year

    with barcol2:
        with st.container(border=True):
            data = database.get_total_net_profit_of_each_year()
            year = [element[0] for element in data]
            profits = [element[1] for element in data]
            profits = [f"{element:,.2f}" for element in profits]
            st.subheader("Net Profit per year")
            figure = px.bar(
                x=year,y=profits,
                color_discrete_sequence=["#10B981"],
                text=profits,
                labels = {
                    "x": "Year",
                    "y": "Net Profit"
                }
            )
            figure.update_yaxes(title_font_size=22, tickfont_size=17)
            figure.update_xaxes(title_font_size=22, tickfont_size=17)
            #color = st.color_picker("Pick chart's color", "#B04141", key="colorpicker2")
            figure.update_traces(textposition="outside", textfont_size=15,marker_cornerradius=10)
            st.plotly_chart(figure)
        





# ================================================================

#                      INVESTMENTS PAGE

# ================================================================






# Form καταχώρησης investment entry
@st.dialog("Add investment")
def open_add_investment_entry_form():
    with st.form("add investment"):
        date = st.date_input("Date", value=datetime.today())   
        entry = st.number_input("Amount (€)", min_value=0.0)
        description = st.text_input("Description", )
        amount = st.number_input("Amount", min_value=0.0)
        currency = st.selectbox(
            label = "Select Currency", options=utils.get_categories(database.get_investments_currencies), 
            index=0, 
            accept_new_options = True,
            help="Enter/Add your preferred currency code (EUR, USD etc)"
            )
        # Μετατρέπω το currency σε κεφαλαία
        currency = currency.upper()

        account = st.text_input("Account", type="email")
        platform = st.text_input("Platform", placeholder="brokerage platform")
         
        submit = st.form_submit_button("Add")
            
        if submit:
            database.add_investment_entry(date, entry, description, amount, currency, account, platform)
            st.rerun()


def render_investments():
    
    
    st.title("Investments")
    # Κάνω hide τα instruction τα οποία δίνει το streamlit στο text input (search query)
    st.markdown(
    """
    <style>
        div[data-testid="stTextInput"] [data-testid="InputInstructions"] {
            display: none;
        }
    </style>
    """
    ,unsafe_allow_html=True)

    topcol1, topcol2, topcol3 = st.columns([0.8, 0.8, 3])
    # METRICS
    with topcol1:
        total_port_value = database.get_sum_investments()
        if isinstance(total_port_value, float):
                st.metric("Total amount invested", f"{database.get_sum_investments():,.2f}€", border=True)
        else:
            st.toast(f"{total_port_value}", icon="⚠️", duration="infinite")
    st.divider()

    # Line chart για Portofolio Value

    with st.container(border=True):
        st.subheader("Portofolio Value")
        dataframe_investments_for_chart = utils.get_investments_line_chart()

        
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dataframe_investments_for_chart["DATE"],
                y=dataframe_investments_for_chart["ENTRY"],
                mode="lines+markers",
                name="Entry Cost",
                # Solid border line
                line=dict(color="#00d2ff", width=3, shape="linear"),  # smooth curve
                # Faded area
                fill="tozeroy",
                fillgradient=dict(
                    type="vertical",
                    colorscale=[
                        [0.0, "rgba(0, 210, 255, 0.00)"],  # 0% opacity (fades away)
                        [0.5, "rgba(0, 210, 255, 0.15)"],  # Soft tint in the middle
                        [1.0, "rgba(0, 210, 255, 0.45)"],  # Stronger accent near the line
                    ],
                ),
                marker=dict(
                    size=7,
                    color="#00d2ff",
                    line=dict(width=2, color="#ffffff"),  # Clean white center/ring
                ),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Date: %{x|%d %b %Y}<br>"
                    "Entry: %{y:,.2f} %{customdata[1]}<br>"
                ),
                customdata=dataframe_investments_for_chart[["DESCRIPTION", "CURRENCY"]],
            )
        )

        
        fig.update_layout(
            autosize=False,   
            width=1500,        
            height=475,       
            title=dict(
                text="<b>Investments Over Time</b>",
                font=dict(size=18, color="#ffffff"),
                x=0.02,
            ),
            paper_bgcolor="rgba(14, 17, 23, 0)",
            plot_bgcolor="rgba(14, 17, 23, 0)",
            hovermode="x unified",
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255, 255, 255, 0.07)",
                color="#a0a0a0",
                tickformat="%b %Y",
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255, 255, 255, 0.07)",
                color="#a0a0a0",
                tickprefix="€",
                zeroline=False,
            ),
            margin=dict(l=40, r=40, t=50, b=40), # Increased left/right margins to prevent clipping
        )

        # Disable Streamlit's container width override
        st.plotly_chart(fig, use_container_width=False)    
            
    
         
         
    search_col, btn_col1, btn_col2 = st.columns([7,1.2,0.8], vertical_alignment="bottom")
    with search_col:
        
        with st.form("form", border=False):
            
            fc1, fc2 = st.columns(2)
            with fc1:
                search_query = st.text_input("Search entry", placeholder="Filter by description", label_visibility="collapsed")
            with fc2:
                submit_button = st.form_submit_button("search")
        if submit_button and search_query.strip():
            render_search_query(search_query)
        
    with btn_col1:     
        if st.button("➕ Add Investment", type="secondary"):
            open_add_investment_entry_form()
    with btn_col2:
        dataframe_investments = utils.get_investments()
        st.download_button(
            "⬇️ Export",
            dataframe_investments["ENTRY"].to_csv(index=False),
            file_name="investments.csv",
            mime="text/csv",
            key="export_losses"
        )     
                    
    

    # Πίνακας investments
    dataframe_investments = utils.get_investments()
    if dataframe_investments.empty:
        st.write("There are no data.")
    else:
        edited_df = st.data_editor(
            dataframe_investments, 
            num_rows="delete",
            height=650,
            disabled=list(dataframe_investments.columns.values),
            column_config={
                            "DATE" : st.column_config.DateColumn("DATE",format="DD-MM-YYYY"),
                            "ID" : None,
                            "PLATFORM": None,
                            "ACCOUNT": None
                        }, 
            hide_index=True,
        )
        deleted_ids = set(dataframe_investments['ID'].to_list()) - set(edited_df['ID'].to_list())
        if deleted_ids:
            for id in deleted_ids:
                database.delete_investment_entry(id)
            st.rerun()    
    




                
             

# Άναλογα με την σελίδα καλείτε η function
# η οποία αντιπροσωπεύει την κάθε μια
if st.session_state.page == "Dashboard":
    render_dashboard()
elif st.session_state.page == "Costs&Losses":
    render_costs_losses()
elif st.session_state.page == "Earnings":
    render_earnings()
elif st.session_state.page == "Investments":
    render_investments()
