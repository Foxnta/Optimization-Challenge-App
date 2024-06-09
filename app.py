import os
import dash
from dash import Dash, dash_table, html, Input, Output, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()


# defino la app
app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )

server = app.server

# importo las tablas y las guardo como dataframes
# tabla1 = pd.read_csv("Tabla1.csv")
# tabla2 = pd.read_csv("Tabla2.csv")
# tabla3 = pd.read_csv("Tabla3.csv")
# tabla4 = pd.read_csv("Tabla4.csv")

current_directory = os.path.dirname(__file__)

try:
    tabla1 = pd.read_csv(os.path.join(current_directory, "Tabla1.csv"))
except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar el archivo 'Tabla1.csv'. Detalles: {e}")

try:
    tabla2 = pd.read_csv(os.path.join(current_directory, "Tabla2.csv"))
except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar el archivo 'Tabla2.csv'. Detalles: {e}")

try:
    tabla3 = pd.read_csv(os.path.join(current_directory, "Tabla3.csv"))
except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar el archivo 'Tabla3.csv'. Detalles: {e}")

try:
    tabla4 = pd.read_csv(os.path.join(current_directory, "Tabla4.csv"))
except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar el archivo 'Tabla4.csv'. Detalles: {e}")


# estructuro el html de la pagina con algunos estilos
app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Asignación De Horas',
                     className="app-header--title")
        ]
    ),
    html.Div(
        className="app-problema",
        children=[
            html.Div([
                html.P('El proceso de fabricación de cierto equipo industrial incluye una etapa de ensamble, la cual se realiza de forma manual por un equipo de operarios, los cuales operan a velocidades diferentes (i.e. eficiencia), dependiendo de su nivel de experiencia y habilidad. El proceso de ensamble es el cuello de botella del sistema, y debido a esto la Dirección de Operaciones de la empresa espera que el proceso opere con altos niveles de productividad. La Tabla 1 presenta los tiempos estándar de las 8 referencias que actualmente se ensamblan, y la cantidad de unidades que se requiere fabricar en un día determinado. La Tabla 2 presenta las eficiencias de los 12 operarios asignados al proceso.')
            ])
        ]
    ),

    html.Div([
        html.H2('Tabla 1: Tiempos estándar [min] y requerimiento',
                style={
                    'textAlign': 'center',
                    'color': 'rgb(243, 245, 244)',
                    'fontSize': '2rem'
                }),

        dash_table.DataTable(
            data=tabla1.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in tabla1.columns],
            style_table={
                'maxWidth': '500px',
                'margin': '1rem auto',
                'overflowX': 'auto'
            },
            style_data={
                'backgroundColor': 'rgb(17, 17, 17)',
                'color': 'white',
                'fontSize': '2rem',
                'textAlign': 'center',
                'size': '0.5rem'
            },
            style_header={
                'backgroundColor': 'rgb(0, 0, 0)',
                'color': 'white',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '2rem'
            },

            style_data_conditional=[
                {
                    'if': {'state': 'active'},
                    'backgroundColor': 'rgb(0, 135, 135)',
                    'border': '1px solid white'
                }]
        )
    ], style={'margin': '5rem 0'}),

    html.Div([
        html.H2('Tabla 2: Eficiencias',
                style={
                    'textAlign': 'center',
                    'color': 'rgb(243, 245, 244)',
                    'fontSize': '2rem'
                }),

        dash_table.DataTable(
            data=tabla2.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in tabla2.columns],
            style_table={
                'maxWidth': '900px',
                'margin': '1rem auto',
                'overflowX': 'auto'

            },
            style_data={
                'backgroundColor': 'rgb(17, 17, 17)',
                'color': 'white',
                'fontSize': '2rem',
                'textAlign': 'center',
                'size': '0.5rem'
            },
            style_header={
                'backgroundColor': 'rgb(0, 0, 0)',
                'color': 'white',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '2rem'
            },
            style_data_conditional=[
                {
                    'if': {'state': 'active'},
                    'backgroundColor': 'rgb(0, 135, 135)',
                    'border': '1px solid white'
                }]
        )
    ], style={'margin': '5rem 0'}),

    html.Div(
        className="app-preguntas",
        children=[
            html.Ol(
                className="app-preguntas--ol",
                children=[
                    html.Li(
                        '¿Qué producto(s) se debe(n) asignar a cada operario y en qué cantidad, con el fin de terminar el plan de producción en el menor tiempo posible?'),
                    html.Li('De la solución al punto anterior se desprende que no es posible ejecutar la totalidad del plan de producción en un turno de 8 horas. Suponga que usted debe comprometerse con un porcentaje de adherencia al plan (porcentaje de cumplimiento). ¿Con qué valor se puede comprometer si se entiende que este porcentaje se debe cumplir para todas las referencias?'),
                    html.Li('Suponga que la empresa trabaja un turno de 8 horas al día. ¿Cuántas horas extra sería necesario programar para cumplir con el plan de producción si el máximo número de horas que se pueden asignar a un operario es de tres por día?')
                ]
            )
        ]
    ),

    html.Div([
        html.H2('Tabla 3: Asignación',
                style={
                    'textAlign': 'center',
                    'color': 'rgb(243, 245, 244)',
                    'fontSize': '2rem',
                    'margin': '0'
                }),
        html.A('Celdas con un tono mas claro son modificables',
               style={
                   'textAlign': 'center',
                   'color': 'rgb(243, 245, 244)',
                   'fontSize': '2rem',
                   'display': 'block',
                   'margin': '1rem'
               }),
        dash_table.DataTable(
            data=tabla3.to_dict('records'),
            id='tabla-asignacion',
            columns=[
                {'name': 'Referencia', 'id': 'Referencia', 'editable': False},
                {'name': 'Tiempo_estándar', 'id': 'Tiempo_estándar', 'editable': False},
                {'name': 'Requerimiento', 'id': 'Requerimiento', 'editable': False},
                {'name': 'A', 'id': 'A', 'editable': True, 'type': 'numeric'},
                {'name': 'B', 'id': 'B', 'editable': True, 'type': 'numeric'},
                {'name': 'C', 'id': 'C', 'editable': True, 'type': 'numeric'},
                {'name': 'D', 'id': 'D', 'editable': True, 'type': 'numeric'},
                {'name': 'E', 'id': 'E', 'editable': True, 'type': 'numeric'},
                {'name': 'F', 'id': 'F', 'editable': True, 'type': 'numeric'},
                {'name': 'G', 'id': 'G', 'editable': True, 'type': 'numeric'},
                {'name': 'H', 'id': 'H', 'editable': True, 'type': 'numeric'},
                {'name': 'I', 'id': 'I', 'editable': True, 'type': 'numeric'},
                {'name': 'J', 'id': 'J', 'editable': True, 'type': 'numeric'},
                {'name': 'K', 'id': 'K', 'editable': True, 'type': 'numeric'},
                {'name': 'L', 'id': 'L', 'editable': True, 'type': 'numeric'},
                {'name': 'Total', 'id': 'Total', 'editable': False}
            ],
            editable=True,
            style_table={
                'maxWidth': '1200px',
                'margin': '1rem auto',
                'overflowX': 'auto'
            },
            style_data={
                'backgroundColor': 'rgb(17, 17, 17)',
                'color': 'white',
                'fontSize': '2rem',
                'textAlign': 'center',
                'size': '0.5rem'
            },
            style_header={
                'backgroundColor': 'rgb(0, 0, 0)',
                'color': 'white',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '2rem'
            },
            style_cell={
                'minWidth': '50px'
            },
            style_data_conditional=[

                {
                    'if': {'state': 'active'},
                    'color': 'white',
                    'backgroundColor': 'rgb(0, 135, 135)',
                    'border': '1px solid white'
                },
                {
                    'if': {'column_id': 'Total'},
                    'backgroundColor': 'rgb(17, 17, 17)',
                }
            ],
            css=[{"selector": "input", "rule": "color:rgb(255,255,255)"}],
        ),
    ],
        style={'margin': '5rem 0'}
    ),

    html.Div([
        html.H2('Tabla 4: Tiempos Resultantes',
                style={
                    'textAlign': 'center',
                    'color': 'rgb(243, 245, 244)',
                    'fontSize': '2rem'
                }),

        dash_table.DataTable(
            id='tabla-resultados',
            data=tabla4.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in tabla4.columns],
            style_table={
                'maxWidth': '1200px',
                'margin': '1rem auto',
                'overflowX': 'auto'
            },
            style_data={
                'backgroundColor': 'rgb(17, 17, 17)',
                'color': 'white',
                'fontSize': '2rem',
                'textAlign': 'center',
                'size': '0.5rem'
            },
            style_header={
                'backgroundColor': 'rgb(0, 0, 0)',
                'color': 'white',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '2rem'
            },
            style_cell={
                'minWidth': '50px'
            },
            style_data_conditional=[
                {
                    'if': {'state': 'active'},
                    'backgroundColor': 'rgb(0, 135, 135)',
                    'border': '1px solid white'
                }]
        )
    ], style={'margin': '5rem 0'}),



    html.Div([
        html.Div([
            html.H2('Makespan: ',
                    style={
                        'textAlign': 'center',
                        'color': 'rgb(243, 245, 244)',
                        'fontSize': '2rem'
                    }),

            html.B(id='valor-makespan',
                   style={
                       'textAlign': 'center',
                       'color': 'rgb(9, 205, 205)',
                       'fontSize': '3rem',
                       'display': 'block',
                       'margin': '1rem'
                   }),
        ]),
        html.Div([
            html.Label('Numero del Equipo: ',
                       style={
                           'textAlign': 'center',
                           'color': 'rgb(243, 245, 244)',
                           'fontSize': '2rem',
                           'marginRight': '10px',
                           'fontWeight': 'bold',
                           'fontSize': '2rem'
                       }),

            dcc.Input(id='Nroequipo', type='number', min=1, max=30, value=1,
                      style={
                          'backgroundColor': 'rgb(17, 17, 17)',
                          'color': 'rgb(243, 245, 244)',
                          'fontSize': '2rem',
                          'width': '55px'
                      })
        ],
            style={'paddingBottom': '15px'
                   }),

        html.Br(),

        html.Div([
            html.Label('Participantes: ',
                       style={
                           'color': 'rgb(243, 245, 244)',
                           'fontSize': '2rem',
                           'paddingBottom': '50px',
                           'fontWeight': 'bold',
                           'fontSize': '2rem',
                       }),
            html.Br(),
            dcc.Textarea(
                id='Participantes',
                style={
                    'width': '95%',
                    'maxWidth': '400px',
                   'height': '100px',
                   'backgroundColor': 'rgb(17, 17, 17)',
                   'color': 'rgb(243, 245, 244)',
                   'outline': 'none',
                   'fontSize': '2rem',
                },
            ),
        ]),

        html.Button('Enviar', id='boton-guardar', n_clicks=0,
                    style={
                        'marginTop': '20px',
                        'color': 'rgb(243, 245, 244)',
                        'backgroundColor': 'rgb(17, 17, 17)',
                        'padding': '8px',
                        'borderRadius': '5px'
                    }),

        html.Div(id='mensaje-guardado',
                    style={
                        'marginTop': '20px',
                        'fontSize': '1.6rem',
                        'color': 'rgb(243, 245, 244)',
                    })
    ],
        style={
        'backgroundColor': 'rgb(36, 36, 36)',
        'textAlign': 'center',
        'margin': 'auto',
        'maxWidth': '450px',
        'paddingTop': '20px',
        'paddingBottom': '20px',
        'borderRadius': '20px',
        'marginBottom': '50px', }),

    html.Div([
             html.H2('🏆    Podio     🏆 ',
                     style={
                         'textAlign': 'center',
                         'color': 'rgb(243, 245, 244)',
                         'fontSize': '2rem'
                     }),


             html.Div(id='datos-mongodb',
                      style={'text-align': 'center',
                             'color': 'rgb(243, 245, 244)',
                             'fontSize': '2rem',
                             'paddingBottom': '5px',
                             }),
             html.Button('Actualizar', id='actualizar-button',
                         style={
                                          'color': 'rgb(243, 245, 244)',
                                          'backgroundColor': 'rgb(17, 17, 17)',
                                          'padding': '8px',
                                          'borderRadius': '5px',
                                          'display': 'block',
                                          'margin': 'auto'
                         }),

             ],
             style={
             'backgroundColor': 'rgb(36, 36, 36)',
             'textAlign': 'center',
             'margin': 'auto',
             'maxWidth': '450px',
             'paddingTop': '20px',
             'paddingBottom': '20px',
             'borderRadius': '20px',
             'marginBottom': '50px'}),

])

# Definir el callback para actualizar la tabla de asignaciones


@app.callback(
    dash.dependencies.Output('tabla-asignacion', 'data'),
    dash.dependencies.Output('tabla-asignacion', 'style_data_conditional'),
    [dash.dependencies.Input('tabla-asignacion', 'data_timestamp')],
    [dash.dependencies.State('tabla-asignacion', 'data')]
)
def actualizar_tabla_asignacion(timestamp, data):
    tabla3 = pd.DataFrame(data)
    tabla3['Total'] = tabla3[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                              'J', 'K', 'L']].apply(pd.to_numeric, errors='coerce').sum(axis=1)
    total = tabla3['Total'].tolist()
    requerimiento = tabla3['Requerimiento'].tolist()
    if(total == requerimiento):
        style_data_conditional = [
            {
                'if': {'state': 'active'},
                'color': 'white',
                'backgroundColor': 'rgb(0, 135, 135)',
                'border': '1px solid white'
            },
            {
                'if': {'column_id': 'Total'},
                'backgroundColor': 'rgb(17, 17, 17)',
            }
        ]
    else:
        style_data_conditional = [
            {
                'if': {'state': 'active'},
                'color': 'white',
                'backgroundColor': 'rgb(0, 135, 135)',
                'border': '1px solid white'
            },
            {
                'if': {'column_id': 'Total'},
                'backgroundColor': 'rgb(147, 6, 6)',
            }
        ]
    return tabla3.to_dict('records'), style_data_conditional

# Definir el callback para actualizar la tabla resultados


@app.callback(
    dash.dependencies.Output('tabla-resultados', 'data'),
    dash.dependencies.Output('valor-makespan', 'children'),
    [dash.dependencies.Input('tabla-asignacion', 'data_timestamp')],
    [dash.dependencies.State('tabla-asignacion', 'data')]
)
def actualizar_tabla_resultados(timestamp, data):
    tabla3 = pd.DataFrame(data)
    columnas = tabla2.columns.tolist()
    columnas.pop(0)
    listadeTE = tabla3['Tiempo_estándar'].values.tolist()
    listasolucion = []

    for operario in columnas:
        columnaoperario = tabla3[operario].values.tolist()
        suma_producto = sum(
            [x * y for x, y in zip(columnaoperario, listadeTE)])
        porcentaje_str = tabla2[operario][0]
        porcentaje_num = float(porcentaje_str[:-1])/100.0
        listasolucion.append(round(suma_producto/porcentaje_num, 2))

    index = 0
    for operario in columnas:
        tabla4.loc[0, operario] = listasolucion[index]
        index += 1
    return tabla4.to_dict('records'), max(listasolucion)

# Guardar los datos en mongoDB


@app.callback(
    dash.dependencies.Output('mensaje-guardado', 'children'),
    dash.dependencies.Input('boton-guardar', 'n_clicks'),
    [dash.dependencies.Input('tabla-asignacion', 'data_timestamp')],
    dash.dependencies.State('valor-makespan', 'children'),
    dash.dependencies.State('Nroequipo', 'value'),
    dash.dependencies.State('Participantes', 'value'),
    dash.dependencies.State('tabla-asignacion', 'data')
)
def guardar_en_mongo(n_clicks, data_timestamp, makespan, nroequipo, participantes, data):
    tabla3 = pd.DataFrame(data)
    tabla3['Total'] = tabla3[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                              'J', 'K', 'L']].apply(pd.to_numeric, errors='coerce').sum(axis=1)
    total = tabla3['Total'].tolist()
    requerimiento = tabla3['Requerimiento'].tolist()
    if(total == requerimiento) and (n_clicks and participantes != None):
        # data = {
        #     'Makespan': makespan,
        #     'Equipo': equipo.upper(),
        #     'Participantes': participantes.upper()
        # }
        # collection.insert_one(data)

        # Inserta los datos en MongoDB
        documento = {'Equipo': nroequipo}
        nuevos_valores = {
            '$set': {'Makespan': makespan,
                     'Participantes': participantes.upper()
                     }
        }

        collection.update_one(documento, nuevos_valores, upsert=True)

        return html.Div('Datos guardados')

    return html.Div('Datos no registrados')

# Traer los datos desde mongoDB


@app.callback(
    Output('datos-mongodb', 'children'),
    Input('actualizar-button', 'n_clicks'),
    State('datos-mongodb', 'children')
)
def actualizar_datos(n_clicks, current_data):
    if n_clicks:
        # todos los documentos de la colección
        datos = sorted(collection.find({}), key=lambda x: x["Makespan"])

        # Crea una lista de HTML para mostrar los datos
        datos_html = []

        for documento in datos:
            datos_html.append(
                html.P(f'Equipo {documento["Equipo"]} - Makespan: {documento["Makespan"]}'))

        return datos_html
    else:
        return current_data

MONGODB_URI = os.getenv('MONGODB_URI')  # Obtén la URL de conexión desde las variables de entorno
client = MongoClient(MONGODB_URI)
db = client['ControlDeLaProduccion']  # nombre de la base de datos
collection = db['Reto']  # nombre de la colección

if __name__ == '__main__':

    app.run_server(debug=True)
