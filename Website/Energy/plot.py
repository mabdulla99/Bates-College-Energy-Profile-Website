import plotly.graph_objects as go

def plotter(dataset):

    """

    :param dataset: <dict> with keys being buildings and values being corresponding
    time and energy levels contained in a list.
    :return: Plotly visualization of data w/ range slider in HTML format.
    """

    fig = go.Figure()

    for key, value in dataset.items():

        sortedEnergy = [x for _, x in sorted(zip(value[0], value[1]))]  # sorting energy levels according to time
        fig.add_trace(go.Scatter(x=list(sorted(value[0])), y=sortedEnergy, name=key))

    fig.update_layout(showlegend=True, legend_title_text='Building', font_family="Georgia",
                      font_color="black", font_size=14, title_text="Energy (kW/h) vs. Time",
                      plot_bgcolor = "light gray", paper_bgcolor = "#e8e8e8")

    fig.update_yaxes(title="Energy (kW/h)")
    fig.update_xaxes(title="Time")

    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True, autorange=True), type="date"))

    final_plot = fig.to_html(full_html=False, default_height=700, default_width = 1500)

    return final_plot



