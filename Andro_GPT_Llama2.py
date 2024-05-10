import streamlit as st
from datetime import datetime, date
import pandas as pd
import time

def calculate_working_days(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    total_working_days = len(date_range)
    return total_working_days

def calculate_worked_days(start_date, today_date):
    date_range = pd.date_range(start=start_date, end=today_date, freq='B')
    worked_days = len(date_range)
    return worked_days

def days_to_months(days):
    return round(days / 30.44, 2)

def days_to_hours(days):
    return days * 8

def countdown_timer(remaining_days):
    remaining_seconds = remaining_days * 24 * 60 * 60
    while remaining_seconds > 0:
        days = remaining_seconds // (24 * 60 * 60)
        hours = (remaining_seconds % (24 * 60 * 60)) // (60 * 60)
        minutes = (remaining_seconds % (60 * 60)) // 60
        seconds = remaining_seconds % 60

        timer_str = f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;
                        background-color: #1E88E5; padding: 10px; border-radius: 5px;">
                <h2 style="color: white; margin: 0;">{timer_str}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(1)
        remaining_seconds -= 1

# Streamlit app
st.set_page_config(page_title="Calculadora de Dias de Trabalho", layout="wide")

# Sidebar
st.sidebar.title("Dados do Contrato")
start_date = st.sidebar.date_input("Data de Início", value=date(2023, 1, 1))
end_date = st.sidebar.date_input("Data de Término", value=date(2023, 12, 31))
today_date = date.today()

# Main content
st.title("Calculadora de Dias de Trabalho")

total_working_days = calculate_working_days(start_date, end_date)
total_working_months = days_to_months(total_working_days)
total_working_hours = days_to_hours(total_working_days)

worked_days = calculate_worked_days(start_date, today_date)
worked_hours = days_to_hours(worked_days)

remaining_days = total_working_days - worked_days
remaining_months = days_to_months(remaining_days)
remaining_hours = days_to_hours(remaining_days)

# Use HTML format for headers
st.markdown("<h2>Resultados</h2>", unsafe_allow_html=True)

# Use a table for the results
data = {
    'Metrics': ['Total de Dias de Trabalho', 'Dias Trabalhados', 'Dias Restantes'],
    'Dias': [total_working_days, worked_days, remaining_days],
    'Meses': [total_working_months, '', remaining_months],
    'Horas': [total_working_hours, worked_hours, remaining_hours],
}

st.table(pd.DataFrame(data))

# Interactive digital tic-tock
st.markdown("<h2>Contador Regressivo</h2>", unsafe_allow_html=True)
countdown_timer(remaining_days)
