import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Cargar el conjunto de datos
csv_file_path = 'AirQualityUCI.csv'  # Reemplaza con la ruta a tu archivo CSV

data = pd.read_csv(csv_file_path, delimiter=';')

# Limpiar datos reemplazando -200 con NaN
data.replace(-200, pd.NA, inplace=True)

# Convertir la columna 'Date' a datetime
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir el layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard de Calidad del Aire", className="text-center"),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='sensor-dropdown',
                options=[
                    {'label': 'CO(GT)', 'value': 'CO(GT)'},
                    {'label': 'NMHC(GT)', 'value': 'NMHC(GT)'},
                    {'label': 'C6H6(GT)', 'value': 'C6H6(GT)'},
                    {'label': 'NOx(GT)', 'value': 'NOx(GT)'},
                    {'label': 'NO2(GT)', 'value': 'NO2(GT)'},
                    {'label': 'PT08.S1(CO)', 'value': 'PT08.S1(CO)'},
                    {'label': 'PT08.S2(NMHC)', 'value': 'PT08.S2(NMHC)'},
                    {'label': 'PT08.S3(NOx)', 'value': 'PT08.S3(NOx)'},
                    {'label': 'PT08.S4(NO2)', 'value': 'PT08.S4(NO2)'},
                    {'label': 'PT08.S5(O3)', 'value': 'PT08.S5(O3)'},
                    {'label': 'T', 'value': 'T'},
                    {'label': 'RH', 'value': 'RH'},
                    {'label': 'AH', 'value': 'AH'}
                ],
                value='CO(GT)',
                clearable=False,
                className='mb-3'
            ),
            dcc.Graph(id='time-series-graph'),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='histogram-graph')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='box-plot-graph')
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter-graph')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id='year-slider',
                min=2004,
                max=2005,
                marks={i: str(i) for i in range(2004, 2006)},
                value=2004,
                step=1
            ),
        ], width=12)
    ]),
], fluid=True)

# Callback para actualizar las gráficas en función del sensor seleccionado y el año
@app.callback(
    [Output('time-series-graph', 'figure'),
     Output('histogram-graph', 'figure'),
     Output('box-plot-graph', 'figure'),
     Output('scatter-graph', 'figure')],
    [Input('sensor-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graphs(selected_sensor, selected_year):
    # Filtrar datos por año
    filtered_data = data[data['Date'].dt.year == selected_year]

    # Crear gráfica de series de tiempo
    fig_time_series = px.line(filtered_data, x='Date', y=selected_sensor, title=f'Series de Tiempo para {selected_sensor} en {selected_year}')

    # Crear histograma
    fig_histogram = px.histogram(filtered_data, x=selected_sensor, title=f'Histograma de {selected_sensor} en {selected_year}')

    # Crear box plot
    fig_box_plot = px.box(filtered_data, y=selected_sensor, title=f'Box Plot de {selected_sensor} en {selected_year}')

    # Crear gráfico de dispersión (scatter plot) para mostrar la relación entre dos variables
    fig_scatter = px.scatter(filtered_data, x=selected_sensor, y='T', title=f'Scatter Plot de {selected_sensor} vs T en {selected_year}')

    return fig_time_series, fig_histogram, fig_box_plot, fig_scatter

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
