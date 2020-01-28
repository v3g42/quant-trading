import plotly.graph_objs as go
import plotly.offline as offline_py
offline_py.init_notebook_mode(connected=True)

color_scheme = {
    'index': '#B6B2CF',
    'etf': '#2D3ECF',
    'tracking_error': '#6F91DE',
    'df_header': 'silver',
    'df_value': 'white',
    'df_line': 'silver',
    'heatmap_colorscale': [(0, '#6F91DE'), (0.5, 'grey'), (1, 'red')],
    'background_label': '#9dbdd5',
    'low_value': '#B6B2CF',
    'high_value': '#2D3ECF',
    'y_axis_2_text_color': 'grey',
    'shadow': 'rgba(0, 0, 0, 0.75)',
    'major_line': '#2D3ECF',
    'minor_line': '#B6B2CF',
    'main_line': 'black'}

def generate_config():
    return {'showLink': False, 'displayModeBar': False, 'showAxisRangeEntryBoxes': True}

def _generate_stock_trace(prices):
    return go.Scatter(
        name='Index',
        x=prices.index,
        y=prices,
        line={'color': color_scheme['major_line']})


def _generate_traces(name_df_color_data):
    traces = []

    for name, df, color in name_df_color_data:
        traces.append(go.Scatter(
            name=name,
            x=df.index,
            y=df,
            mode='line',
            line={'color': color}))

    return traces


def plot_stock(prices, title):
    config = generate_config()
    layout = go.Layout(title=title)

    stock_trace = _generate_stock_trace(prices)

    offline_py.iplot({'data': [stock_trace], 'layout': layout}, config=config)


def print_dataframe(df, n_rows=10, n_columns=3):
    missing_val_str = '...'
    config = generate_config()

    formatted_df = df.iloc[:n_rows, :n_columns]
    formatted_df = formatted_df.applymap('{:.3f}'.format)

    if len(df.columns) > n_columns:
        formatted_df[missing_val_str] = [missing_val_str]*len(formatted_df.index)
    if len(df.index) > n_rows:
        formatted_df.loc[missing_val_str] = [missing_val_str]*len(formatted_df.columns)

    trace = go.Table(
        type='table',
        columnwidth=[1, 3],
        header={
            'values': [''] + list(formatted_df.columns.values),
            'line': {'color': color_scheme['df_line']},
            'fill': {'color': color_scheme['df_header']},
            'font': {'size': 13}},
        cells={
            'values': formatted_df.reset_index().values.T,
            'line': {'color': color_scheme['df_line']},
            'fill': {'color': [color_scheme['df_header'], color_scheme['df_value']]},
            'font': {'size': 13}})

    offline_py.iplot([trace], config=config)


def plot_resampled_prices(df_resampled, df, title):
    config = generate_config()
    layout = go.Layout(title=title)

    traces = _generate_traces([
        ('Monthly Close', df_resampled, color_scheme['major_line']),
        ('Close', df, color_scheme['minor_line'])])

    offline_py.iplot({'data': traces, 'layout': layout}, config=config)


def plot_returns(returns, title):
    config = generate_config()
    layout = go.Layout(title=title)

    traces = _generate_traces([
        ('Returns', returns, color_scheme['major_line'])])

    offline_py.iplot({'data': traces, 'layout': layout}, config=config)


def plot_shifted_returns(df_shited, df, title):
    config = generate_config()
    layout = go.Layout(title=title)

    traces = _generate_traces([
        ('Shifted Returns', df_shited, color_scheme['major_line']),
        ('Returns', df, color_scheme['minor_line'])])

    offline_py.iplot({'data': traces, 'layout': layout}, config=config)


def print_top(df, name, top_n=10):
    print('{} Most {}:'.format(top_n, name))
    print(', '.join(df.sum().sort_values(ascending=False).index[:top_n].values.tolist()))
