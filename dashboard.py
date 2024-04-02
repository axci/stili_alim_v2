import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from utils_contstants import *
from utils_plot import plot_vertical_bar_chart, plot_horizontal_bar_chart, plot_gauge, colors

#######################
# Page configuration
st.set_page_config(
    page_title = "Stili alimentari",
    page_icon='🥑',
    layout='wide',
    initial_sidebar_state='expanded'
)

alt.themes.enable('dark')

#######################
# Load Data
df = pd.read_csv('data/stili_al.csv')
df = (df
    .rename(columns={'area': 'regione', 's3': 'sesso', 'generation': 'generazione'})
    .replace('Nessuno di questi', 'Nessuno stile')
)

checkpoint_countries = []
checkpoint_regions = []

#######################
# Grouping function
def group_df_all(df, metric: str) -> pd.Series:
    # group for a bar chart
    s = (df
            .groupby(metric)
            .count()
        ).country.sort_values()
    return s    


def group_df(df, metric: str, compare_by: str) -> pd.Series:
    # group for a bar chart
    s = (df
            .groupby([compare_by, metric])
            .country
            .count()
            #.sort_values()
        )
    return s


def aggregate_dataframe(df, stile_col='stile', categories=['regione', 'gender', 'generazione']):
    """
    Aggregates a DataFrame by a 'stile' column and counts occurrences of specified categories.
    
    Parameters:
    - df: DataFrame to be processed.
    - stile_col: The name of the column to group by. Default is 'stile'.
    - categories: List of column names to count occurrences for. Default is ['regione', 'gender', 'generazione'].
    
    Returns:
    - A new DataFrame with the total count and counts for specified categories by 'stile'.
    """
    # Filter DataFrame to include only relevant columns (stile + categories)
    relevant_df = df[[stile_col] + categories]
    
    # Calculate the total counts for each 'stile'
    total_counts = relevant_df.groupby(stile_col).size().rename('Total')
    
    # Initialize a list to hold the data for each category
    category_data = []
    
    # Process each category
    for category in categories:
        # Create dummy variables for the current category
        dummies = pd.get_dummies(relevant_df[[stile_col, category]], columns=[category])
        # Aggregate dummies by 'stile'
        aggregated = dummies.groupby(stile_col).sum()
        # Rename columns to include category name
        aggregated.columns = [col.split("_")[-1] for col in aggregated.columns]
        # Append to the list
        category_data.append(aggregated)
    
    # Combine all the category data with the total counts
    summary_df = pd.concat([total_counts] + category_data, axis=1).fillna(0).astype(int)

    summary_df=summary_df.sort_values('Total', ascending=False)  # sort by total
    if 'Altro, non vuole indicare' in summary_df.columns:
        del summary_df['Altro, non vuole indicare']

    #summary_df['stile'] = pd.Categorical(summary_df['stile'], categories=order_stile, ordered=True)

    return summary_df


#######################
# Dashboard Main Panel
col = st.columns((2, 1), gap='medium')

############# Sidebar
with st.sidebar:
    st.title('🥑 Stili alimentari')
    countries = ['All'] + list(df.country.unique())
    selected_country = st.selectbox('Selezionare un paese', countries)

    if selected_country == 'All':
        df_filtered = df
    else:
        df_filtered = df.query('country == @selected_country')

        # compare with another country
        countries_compare = [country for country in list(df.country.unique()) if country != selected_country]
        checkpoint_countries = st.multiselect('Compare:', countries_compare)
        if checkpoint_countries: # if there are selected countries to compare
            selected_countries = [selected_country] + checkpoint_countries
            df_filtered = df.query('country in @selected_countries')
            
        # region
        if selected_country == "Italia":
            regions = ['All'] + list(df_filtered.query("country == 'Italia'").regione.unique())
            selected_region = st.selectbox('Selezionare una regione', regions)
            if selected_region != 'All':
                df_filtered = df_filtered.query('regione == @selected_region')

                # compare with another country
                regions_compare = [region for region in list(df.query("country == 'Italia'").regione.unique()) if region != selected_region]
                checkpoint_regions = st.multiselect('Compare:', regions_compare)
                if checkpoint_regions: # if there are selected regions to compare
                    selected_regions = [selected_region] + checkpoint_regions
                    df_filtered = df.query('regione in @selected_regions')

    # gender
    genders = ['All'] + list(df.sesso.unique())
    selected_gender = st.selectbox('Selezionare un sesso', genders)
    if selected_gender != 'All':
        df_filtered = df_filtered.query('sesso == @selected_gender')

    # age group
    ages = ['All'] + list(  np.sort(df.generazione.unique() ))
    selected_age = st.selectbox('Selezionare una generazione', ages)
    if selected_age != 'All':
        df_filtered = df_filtered.query('generazione == @selected_age')
    
    # s5
    s5_list = ['All'] + list(df.res_acq.unique())
    selected_s5 = st.selectbox('Selezionare responsabili acquisti', s5_list)
    if selected_s5 != 'All':
        df_filtered = df_filtered.query('res_acq == @selected_s5')

    # Color theme
    st.markdown("""<br><hr>""", unsafe_allow_html=True) # a gap br and a line (hr)
    color_theme_list = ['blue', 'cyan', 'green', 'red', 'yellow', 'olive', 'purple', 'gold']
    selected_color_theme = st.selectbox('🎨 Select a color theme', color_theme_list)
    color_map = {
        'blue': BLUE,
        'cyan': CYAN,
        'green': GREEN,
        'yellow': YELLOW,
        'red': RED,
        'olive': OLIVE,
        'purple': PURPLE,
        'gold': GOLD
    }
    selected_color = color_map[selected_color_theme]
    if selected_color in colors:
        colors.remove(selected_color)  # Remove the selected_color from its current position
        colors.insert(0, selected_color) 



with col[0]:

    ####################### COLUMN 1
    st.markdown('#### Stili Alimentari')
    
    # The Bar Chart
    if selected_country == "All":
        metric_series = group_df_all(df_filtered, "stile")
        #st.dataframe(metric_series)
        #fig = make_bars_plotly_all(selected_color_theme, metric_series, fixed_order_flag_freq=False)
        fig = plot_horizontal_bar_chart([metric_series], order=order_stile, title='Stili alimentari', 
                                        show_legend=False, show_title=False, figsize=(10, 5))
    else:
        if checkpoint_regions:
            metric_series = group_df(df_filtered, "stile", 'regione')
            series_list = []
            for area, group in metric_series.groupby(level=0):
                series = group.reset_index(level=0, drop=True)
                series.name = area  # Set the series name to the country
                series_list.append(series)
        else:
            metric_series = group_df(df_filtered, "stile", 'country')
            # Create a list of Series
            series_list = []
            for country, group in metric_series.groupby(level=0):
                series = group.reset_index(level=0, drop=True)
                series.name = country  # Set the series name to the country
                series_list.append(series)

        #st.dataframe(metric_series)
        #fig = make_bars_plotly(selected_color_theme, metric_series)
        fig = plot_horizontal_bar_chart(series_list, order=order_stile, title='Stili alimentari', show_title=False,
                                        labels=[ser.name for ser in series_list], figsize=(10, 5))
    #st.plotly_chart(fig)
    st.pyplot(fig)

    # ##### TABLE
    selected_categories = st.multiselect('', ['regione', 'sesso', 'generazione'], placeholder="Choose a category")
    af = aggregate_dataframe(df_filtered, categories=['regione', 'sesso', 'generazione'])
    if selected_categories:
        af = aggregate_dataframe(df_filtered, categories=selected_categories)
  
    st.dataframe(af,
                 column_config={
                     "Total": st.column_config.ProgressColumn(
                         "Total",
                         format="%f",
                         min_value=0,
                         max_value=max(af.Total)
                     )
                 }
                 )






################################# COLUMN 2
with col[1]:
    st.markdown('#### Prodotti')
    selected_food = st.multiselect('', food.keys(), placeholder="Selezionare un prodotto")
    if not selected_food:
        selected_food = ['🧁 pasticceria']

    df_prodotti = df_filtered[[ food[prodotto][0] for prodotto in selected_food ] + [ food[prodotto][1] for prodotto in selected_food ]]
    #st.text(df_prodotti)

    #subcol = st.columns((1, 1), gap='medium')
    #with subcol[0]:
    temp_df = df_filtered[[food[prodotto][0] for prodotto in selected_food ]]
    series_list = []
    for col in temp_df.columns:
        series_list.append(temp_df[col].value_counts())
    order = order_frequenza
    #st.dataframe(series_list[0])
    fig = plot_horizontal_bar_chart(series_list, order, title="Frequenza", labels=selected_food, figsize=(6, 3))
    st.pyplot(fig)

    ##### Gauge Chart
    df_prodotti = df_filtered[[ food[prodotto][2] for prodotto in selected_food ]]
    freq_dict = {selected_food[i]: round(df_prodotti[col].mean(), 1) for i, col in enumerate(df_prodotti) }
    
    col_maker = [1 for item in selected_food]
    subcol = st.columns(col_maker)

    for i, prodotto in enumerate(selected_food):
        with subcol[i]:
            fig = plot_gauge(freq_dict[selected_food[i]], colors[i])
            st.plotly_chart(fig)




    #with subcol[1]:
    temp_df = df_filtered[[food[prodotto][1] for prodotto in selected_food ]]
    series_list = []
    for col in temp_df.columns:
        series_list.append(temp_df[col].value_counts())
    order = order_cambiamento
    fig = plot_horizontal_bar_chart(series_list, order, title="Cambiamento", labels=selected_food, figsize=(6,3))
    st.pyplot(fig)
    #st.image('images/cioccolato.png')

    ##### Gauge Chart: Cambiamento
    df_prodotti = df_filtered[[ food[prodotto][3] for prodotto in selected_food ]]
    freq_dict = {selected_food[i]: 
                 ((df_prodotti.loc[df[col]==1][col].sum() / -df_prodotti.loc[df[col]==-1][col].sum() ) - 1 )*100
                 for i, col in enumerate(df_prodotti) }
    
    col_maker = [1 for item in selected_food]
    subcol = st.columns(col_maker)

    for i, prodotto in enumerate(selected_food):
        with subcol[i]:
            fig = plot_gauge(freq_dict[selected_food[i]], colors[i], 
                             title="Growth Rate", limit_down=-100, limit_up=100, perc=True)
            st.plotly_chart(fig)



    
