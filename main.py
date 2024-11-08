'''
Streamlit App for Feedback Analysis
'''
import streamlit as st
import pandas as pd
import util

# URL of the data
URL = "https://nevarisbuild.blob.core.windows.net/exceptiontracker/feedback.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load data from a CSV file."""
    data = pd.read_csv(URL)
    return data


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="User Feedbacks", layout="wide")
    st.title('Feedback Analyse')
    st.subheader('Daten')

    with st.spinner('Loading data...'):
        # Load data
        df = load_data()

    # Daten aufbereiten
    df = prepare_data(df.copy())

    # Display the data
    display_data(df)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    '''Prepare the data'''
    # Emojis for the column "Begeistert" else "☹️"
    df["Begeistert"] = df["IsHappy"].apply(
        lambda x: "😊" if x == 1 else "")
    df["Datum"] = pd.to_datetime(df.Datum).dt.strftime('%d.%m.%Y')
    df["Message"] = df.Message.astype(str)
    # Remove leading and trailing whitespaces
    df["Message"] = df["Message"].str.strip()
    # Remove rows with Message length less than 3 and 
    # text contains only digits or special characters
    df["Kunden-Feedback"] = df["Message"].apply(
        lambda x: x if len(x) > 2 and any(char.isalpha() for char in x) else None)
    # Versionen ermitteln für eine bessere Lesbarkeit
    df["Version"] = df["AppVersion"].apply(util.get_version)
    # Remove rows with missing values in the column "Kunden-Feedback"
    df.dropna(subset=["Kunden-Feedback", "Version"], inplace=True)
    # Daten bereinigen für Produkt
    df["Produkt"] = df["AppName"].str.replace("NEVARIS ", "")
    return df


def display_data(df: pd.DataFrame) -> None:
    '''Display the most important data'''
    st.dataframe(df[["Datum", "Produkt", "Version", "Begeistert", "Kunden-Feedback"]],
                 column_config={
        # Adjust the width for "Datum"
        "Datum": st.column_config.TextColumn(help="Datum des Feedback"),
        # Adjust the width for "AppName"
        "Produkt": st.column_config.TextColumn(help="NEVARIS Anwendungen"),
        # Adjust the width for "AppVersion"
        "Version": st.column_config.TextColumn(help="Offiziell ausgelieferte Versionen"),
        # Adjust the width for "Begeistert"
        "Begeistert": st.column_config.TextColumn(help="😊 = Begeistert; ☹️ = Leer"),
        # Adjust the width for "Kunden-Feedback"
        "Kunden-Feedback": st.column_config.TextColumn(width=700, disabled=True)
    },
        use_container_width=True,
        hide_index=True,
        height=600,
        selection_mode="multi-column",
        key="dataframe")


if __name__ == '__main__':
    main()
