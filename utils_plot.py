import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils_contstants import *

colors = [ BLUE, CYAN, GREEN, RED, YELLOW, OLIVE, PURPLE, GOLD]

def plot_vertical_bar_chart(series_list, order, title, labels=None, xlabel_rotation=90):
    """
    Plots multiple pd.Series on the same vertical bar chart.

    :param series_list: List of pd.Series to plot.
    :param labels: Optional list of labels for the series. If None, Series names will be used.
    """
    n = len(series_list)  # Number of series
    if labels is None:
        labels = [f"Series {i+1}" for i in range(n)]  # Default labels if none provided

    reordered_series_list = [series.reindex(order) for series in series_list]
    total_values = [sum(series.values) for series in reordered_series_list]  # Total values for each series

    # Settings
    bar_width = 0.8 / n  # Adjust bar width based on number of series
    index = np.arange(len(order))  # Use the provided order for the x-axis

    # Plotting
    fig, ax = plt.subplots()
    for i, (series, label) in enumerate(zip(reordered_series_list, labels)):
        position = index - 0.4 + bar_width*(i + 0.5)
        bars = ax.bar(position, series, bar_width, label=label, color=colors[i])

        # Add percentages above bars
        for bar, value in zip(bars, series):
            percentage = f"{value / total_values[i] * 100:.1f}%"  # Calculate percentage
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), percentage, 
                    ha='center', va='bottom')

    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Labeling
    ax.set(xticks=index, xticklabels=order, xlim=[-0.5, len(order)-0.5])
    ax.set_title(title, fontsize=20)
    ax.legend()

    plt.xticks(rotation=xlabel_rotation)

    return fig

def plot_horizontal_bar_chart(series_list, order, title, figsize=(6, 6), perc_fontsize=10,
                              labels=None, show_legend=True, show_title=True):
    """
    Plots multiple pd.Series on the same horizontal bar chart.

    :param series_list: List of pd.Series to plot.
    :param order: The order of the bars on the y-axis.
    :param title: The title of the plot.
    :param labels: Optional list of labels for the series. If None, Series names will be used.
    """
    n = len(series_list)  # Number of series
    # control fontsize of the percentage on bars:
    if n == 2:
        perc_fontsize = 5
    if n== 3:
        perc_fontsize = 3
    if n > 3:
        perc_fontsize = 1
    if labels is None:
        labels = [f"Series {i+1}" for i in range(n)]  # Default labels if none provided

    reordered_series_list = [series.reindex(order) for series in series_list]
    total_values = [sum(series.values) for series in reordered_series_list]  # Total values for each series

    # Settings
    bar_height = 0.8 / n  # Adjust bar height based on number of series
    index = np.arange(len(order))  # Use the provided order for the y-axis

    # Plotting
    fig, ax = plt.subplots(figsize=figsize)
    for i, (series, label) in enumerate(zip(reordered_series_list, labels)):
        position = index - 0.4 + bar_height * (i + 0.5)
        bars = ax.barh(position, series, bar_height, label=label, color=colors[i])
       
        # Add percentages beside bars
        for bar, value in zip(bars, series):
            percentage = f"{value / total_values[i] * 100:.1f}%"
            # Place text inside the bar if the bar is wide enough, otherwise place it outside
            text_position = bar.get_width() - 5 if bar.get_width() > 90 else bar.get_width() + 5
            ha = 'right' if bar.get_width() > 90 else 'left'
            
            ax.text(text_position, bar.get_y() + bar.get_height() / 2, percentage, 
                    ha=ha, va='center', color='white' if bar.get_width() > 90 else 'black', fontsize=perc_fontsize)

    # Remove spines
    ax.spines[['top','right','bottom']].set_visible(False)
    ax.spines['left'].set_linewidth(1.1)
    ax.grid(which="major", axis='x', color='#758D99', alpha=0.6, zorder=1)

    # Reformat x-axis tick labels
    ax.xaxis.set_tick_params(labeltop=True,      # Put x-axis labels on top
                            labelbottom=False,  # Set no x-axis labels on bottom
                            bottom=False,       # Set no ticks on bottom
                            labelsize=11,       # Set tick label size
                            pad=-1)             # Lower tick labels a bit
    ax.yaxis.set_tick_params(pad=5,            # Pad tick labels so they don't go over y-axis
                         labelsize=9,       # Set label size
                         bottom=False)       # Set no ticks on bottom/left

    # Labeling
    ax.set(yticks=index, yticklabels=order)
    
    if show_title:
        ax.set_title(title, fontsize=20)
    
    if show_legend:
        ax.legend()

    return fig



########## GAUGE
def plot_gauge(value, color, limit_down=0, limit_up=10, perc=False, title="Volte al mese"):
    if perc:
        suffix="%"
    else:
        suffix=""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number={'suffix': suffix},     
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
            gauge = {'axis': {'range': [limit_down, limit_up]},
                            'bar': {'color': color},  # Change the bar color
                    }  
    ))
    fig.update_layout(width=150, height=170)  # Adjust these values according to your needs
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.update_layout(title_font=dict(size=10))



    return fig


################## PLOTLY
def make_bars_plotly_all(input_color, s: pd.Series, 
                         fixed_order_flag_freq=False, fixed_order_flag_camb=False,
                         horizontale=True,
                         width=800, height=600):
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
    chart_color = color_map.get(input_color, 'blue')  # Default to blue if color not found
    # Fixed order for the bars
    if fixed_order_flag_freq:
        fixed_order = [
        'Tutti i giorni o quasi', '2-3 volte a settimana', '1 volta a settimana', 
        '2-3 volte al mese', '1 volta al mese', "4-5 volte all’anno", 
        'Più raramente', 'Mai'
        ][::-1]
        s = s.reindex(fixed_order)

    if fixed_order_flag_camb:
        fixed_order = [
            "Molto aumentato", "Un po’ aumentato", "Uguale",
            "Un po’ diminuito", "Molto diminuito"
        ][::-1]
        s = s.reindex(fixed_order)

    # Calculate percentages
    total = s.sum()
    percentages = (s / total * 100).round(1).astype(str) + '%'

    if horizontale:
        fig = go.Figure(go.Bar(
            x=s.values,
            y=s.index,
            orientation='h',
            marker=dict(color=chart_color),
            text=percentages,
            textposition='auto',
        ))
    else:
        fig = go.Figure(go.Bar(
            x=s.index,
            y=s.values,
            orientation='v',
            marker=dict(color=chart_color),
            text=percentages,
            textposition='auto',
        ))

    # Update layout for a cleaner look
    fig.update_layout(
        #title=title,
        xaxis=dict(
            showticklabels=True,
            showgrid=True,
            tickangle=0,
            titlefont=dict(size=12),
            title_standoff=25
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            linecolor='black'
        ),
        plot_bgcolor='white',
        showlegend=False,
        autosize=True,  # Enable autosizing
        #width=width,
        #height=height,
    )

    fig.update_yaxes(tickfont=dict(size=12), tickmode='array', tickvals=list(s.index))
    fig.update_xaxes(tickfont=dict(size=12))

    return fig

def make_bars_plotly(input_color, s: pd.Series, width=800, height=600):
    if len(s.index.levels[0]) == 2:
        height *= 1.1
    if len(s.index.levels[0]) == 3:
        height *= 1.3
    if len(s.index.levels[0]) > 3:
        height *= 1.5

    # sorting bars
    if s.index.levels[1].name in [f'q5__{i}' for i in range(4, 11)]:
        fixed_order = [
            "Molto aumentato", "Un po’ aumentato", "Uguale",
            "Un po’ diminuito", "Molto diminuito"
        ][::-1]
        new_categories = pd.Categorical(s.index.get_level_values(1), categories=fixed_order, ordered=True)

        # Rebuild the MultiIndex with the new categorical order for the second level
        s.index = pd.MultiIndex.from_arrays([s.index.get_level_values(0), new_categories], names=s.index.names)

        # Sort the Series based on the new index
        s = s.sort_index(level=1)
 
    if s.index.levels[1].name in [f'q4__{i}' for i in range(4, 11)]:
        fixed_order = [
        'Tutti i giorni o quasi', '2-3 volte a settimana', '1 volta a settimana', 
        '2-3 volte al mese', '1 volta al mese', "4-5 volte all’anno", 
        'Più raramente', 'Mai'
        ][::-1]

        new_categories = pd.Categorical(s.index.get_level_values(1), categories=fixed_order, ordered=True)

        # Rebuild the MultiIndex with the new categorical order for the second level
        s.index = pd.MultiIndex.from_arrays([s.index.get_level_values(0), new_categories], names=s.index.names)

        # Sort the Series based on the new index
        s = s.sort_index(level=1)

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
    chart_color = color_map.get(input_color, 'blue')  # Default to blue if color not found
    country_colors = {'Italia': OLIVE, 'Germania': YELLOW, 'Francia': BLUE, 'USA': RED }

    # colors
    colors = chart_color

    fig = go.Figure()

    for i, country in enumerate(s.index.levels[0]):
        country_data = s[country]
        country_total = country_data.sum()
        country_percentages = (country_data / country_total * 100).round(1)
        if s.index.levels[0].name == 'country':
            colors = country_colors[country]
        elif s.index.levels[0].name == 'regione':
            colors = list(color_map.values())[i]
        fig.add_trace(go.Bar(
            x=country_percentages.values,
            y=country_data.index,
            orientation='h',
            marker=dict(color=colors),
            text=country_percentages.apply(lambda x: f'{x}%'),
            textposition='auto',
            name=country  # If you want a legend indicating each country
        ))

    # Update layout for a cleaner look
    fig.update_layout(
        #title=title,
        xaxis=dict(
            showticklabels=True,
            showgrid=True,
            tickangle=0,
            titlefont=dict(size=12),
            title_standoff=25
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            linecolor='black'
        ),
        plot_bgcolor='white',
        showlegend=True,
        autosize=True,
        #width=width,
        #height=height,
    )

    return fig
