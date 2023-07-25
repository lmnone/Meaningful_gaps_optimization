import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio


def plot_gantt_chart(df_, annotation_column='comment', save_path=None):
    fig = px.timeline(df_, x_start='start_o', x_end='end_o', y='room_id', opacity=0.5)
    fig.update_yaxes(title_text='room_id')

    # Add annotations for the room column
    for i, row in df_.iterrows():
        fig.add_annotation(x=row['start'], y=row['room_id'], text=str(row[annotation_column]), showarrow=False,
                           font=dict(color='red', size=14))

    fig.show()
    if save_path is not None:
        pio.write_image(fig, save_path)


def plot_gantt_chart_ticks(df_, tick_start_col='start15', tick_end_col='end15'):
    fig, ax = plt.subplots()

    ax.barh(df_['task'], df_[tick_end_col] - df_[tick_start_col], left=df_[tick_start_col])
    ax.set_xlabel('Time')
    ax.set_ylabel('Room')
    ax.set_title('Gantt Chart')

    plt.show()


def plot_bar_h(data):
    x = np.arange(len(data))
    plt.bar(x, data)
    plt.show()


def plot_position(array1, array2, array3):
    x = np.arange(len(array1))

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=array1, name='position', marker=dict(opacity=0.5)))
    fig.add_trace(go.Bar(x=x, y=array2, name='open(at start)', marker=dict(opacity=0.5)))
    fig.add_trace(go.Bar(x=x, y=array3, name='close(at end)', marker=dict(opacity=0.5)))

    fig.update_layout(barmode='group')
    fig.show()
