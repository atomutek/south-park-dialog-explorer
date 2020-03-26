import pandas as pd
import streamlit as st

st.title('South Park Dialog explorer')

DATA_FILE = '../data/southpark-all-seasons.csv'

NOTHING = 'Nothing'
MOST_REPR = 'Most represented'
LEAST_REPR = 'Least represented'
SHOW_MY_FAV = 'Show my favorite character'

# Season,Episode,Character,Line
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_FILE, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


def find_brute_force(string, string_to_find):
    return all(keyword.lower() in string.lower() for keyword in string_to_find.lower().split())


def search(data, col, string_to_find):
    results = []
    for test_str in data[col]:
        res = find_brute_force(test_str, string_to_find)
        if res:
            results.append(test_str.replace('\n', ''))
    return results


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(100000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')


def main_body(data, char, what):

    if what == NOTHING:
        # TODO: Find a way to show the whole `line` column
        st.subheader('Raw data')
        st.dataframe(data.head())

        with pd.option_context('display.max_colwidth', None):
            html = data.head().to_html(index=False, escape=True)
            st.markdown(html, unsafe_allow_html=True)
    # Show the ten most represented characters
    elif what == MOST_REPR:
        st.subheader('Most represented characters')
        st.dataframe(data.groupby('character')[['line']].count().reset_index().sort_values(by='line', ascending=False).head(10))
    elif what == LEAST_REPR:
        st.subheader('Least represented characters')
        st.dataframe(data.groupby('character')[['line']].count().reset_index().sort_values(by='line', ascending=True).head(10))
    elif what == SHOW_MY_FAV:
        st.subheader('Favorite character')
        st.write('Your favorite character is: {}'.format(char))
        st.dataframe(data[data.character == char].line)

        string_to_find = st.text_input("What are you looking in the lines?", "They killed Kenny")

        results = search(data, 'line', string_to_find)

        if not results:
            st.write("Not found.")

        for result in results:
            st.write(result)


def sidebar(data):
    st.sidebar.markdown('# Which character?')

    char = st.sidebar.selectbox(
        'Which character do you like best?', data['character'].unique())

    st.sidebar.markdown('You selected: {}'.format(char))

    what = st.sidebar.radio(
        "What do you want to do?",
        (NOTHING,
         MOST_REPR,
         LEAST_REPR,
         SHOW_MY_FAV))

    return char, what


if __name__ == '__main__':
    char, what = sidebar(data)
    main_body(data, char, what)
