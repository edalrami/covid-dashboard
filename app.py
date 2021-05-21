import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_daq as daq

#Custom python file made for data plot object generation functions
from plots import *
import pandas as pd


#Prepare State Data-----------------------------------------------------------------------------------------------------------
state_data = pd.read_excel("Covid-19 Vaccinations Data US/Covid-19 Vaccinations Data US/us_state_vaccinations.xlsx", engine='openpyxl')
state_data = state_data[["date", "location", "people_fully_vaccinated_per_hundred", "people_vaccinated_per_hundred", "daily_vaccinations"]]
state_data = state_data[state_data.location != "United States"].sort_values(by="date")

#Prepare totals data----------------------------------------------------------------------------------------------------------
totals_data = pd.read_excel("Covid-19 Vaccinations Data US/Covid-19 Vaccinations Data US/Total COVID-19 Vaccinations in the United States .xlsx", engine='openpyxl')

#drop null rows
totals_data = totals_data[totals_data["Doses Administered per 100k by State where Administered"].notna()]

#comparing with the CDC data, doses administered per 100k should be signified in the thousands
totals_data["Doses Administered per 100k by State where Administered"] = totals_data["Doses Administered per 100k by State where Administered"].apply(lambda x: x*1000)
totals_data = totals_data[["State/Territory/Federal Entity","Doses Administered per 100k by State where Administered", "Total Doses Administered by State where Administered"]]

#Create dictionary of state codes. The codes are needed to generate a Choropleth map object.
location_code = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa':'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    "Federated States of Micronesia" : 'FSM',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    "Indian Health Svc" : "IHS",
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Marshall Islands':'RMI',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    "New York City": "NYC",
    'New York State': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Republic of Palau': 'PW',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

#Create a reverse dictionary to be able convert state codes back into their original names. 
#This will be used to convert the location codes in the death/case count data.
reverse_location_code = dict(map(reversed, location_code.items()))
totals_data["location_code"] = totals_data["State/Territory/Federal Entity"].apply(lambda x: location_code[x])


#Prepare daily cases/death count data
cases_deaths = pd.read_csv("Covid-19 Vaccinations Data US/Covid-19 Vaccinations Data US/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv")
cases_deaths.submission_date = pd.to_datetime(cases_deaths.submission_date)
cases_deaths.sort_values(by="submission_date", inplace=True)
cases_deaths = cases_deaths[["submission_date", "state", "new_case", "new_death", "conf_cases", "conf_death"]].reset_index(drop=True)
cases_deaths.columns = ["submission_date", "state", "New Cases", "New Deaths", "Total Confirmed Cases", "Total Confirmed Deaths"]
cases_deaths["state"] = cases_deaths.state.apply(lambda x: reverse_location_code[x])

#Prepare Vaccine Distribution Allocations Data
pfizer = pd.read_csv("Covid-19 Vaccinations Data US/Covid-19 Vaccinations Data US/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_Pfizer.csv")
moderna = pd.read_csv("Covid-19 Vaccinations Data US/Covid-19 Vaccinations Data US/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_Moderna.csv")
johnson = pd.read_csv("Covid-19 Vaccinations Data US/Covid-19 Vaccinations Data US/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_Janssen.csv")

pfizer["type"] = "pfizer"
moderna["type"] = "moderna"
johnson["type"] = "johnson"

vaccines = pd.concat([pfizer,moderna,johnson], axis = 0)




def get_state_dropdown():
    dict_list= []
    for i in location_code.keys():
        dict_list.append({'label': i, 'value': i})
    return dict_list


def get_state_names():
    return list(location_code.keys())

dropdown_values = get_state_dropdown()

#---------------------------------DASH LAYOUT---------------------------------------------------------
#Create dash instance to initialize app
app = dash.Dash(__name__)
server = app.server 
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.title = "Honey Report"
app.layout = html.Div(children=[
        html.H1(children=['COVID19 Vaccination Effects on Rate of Death/Cases']),
        html.H2(children = 'Created by Edwin A. Ramirez'),

        #paragraph div
        #Alternative method to make this cleaner would be to be write 
        #paragraphs in text file then read it and load it

        #Div Containing first two figures
        html.Div(
            id = 'main-div1',
            className = 'twelve columns mini_container',
            children = [
                html.Div(
                    id="map-container",
                    className = "six columns",
                    children = [
                        html.Div([dcc.Graph(id="map-fig", figure=generate_map_object(totals_data))])
                    ]
                ),

                html.Div(
                    id = "bar-container",
                    className = "six columns",
                    children = [
                        html.Div([dcc.Graph(id="bar-fig", figure=generate_bar_plot(totals_data))])
                    ]

                ),

            ]
        ),


        html.Div(
            id = "main-div2",
            className = "twelve columns mini_container",
            children = [
                html.Div(
                    id="text-container",
                    className="six columns",
                    children = [
                        html.P("Select Location From Dropdown"),
                        html.Div(
            
                            id = "dropdown-container",
                            className = "four columns",
                            children = [
                                dcc.Dropdown(
                                    id = 'dropdown',
                                    className = "",
                                    options=dropdown_values,
                                    value='Maine'
                                ),        
                            ]
                        )
                    ], style={'align-items':'center'}
                )
                
            
            ], 

        ),



        #Div Containing first two figures
        html.Div(
            id = 'main-div3',
            className = 'twelve columns mini_container',
            children = [
                html.Div(
                    id = "donut-container",
                    className = "four columns",
                    children = [
                        
                        html.Div([dcc.Graph(id='donut-fig')])
                    ]


                ),

                html.Div(
                    id = "multiline-container",
                    className = "four columns",
                    children = [

                         html.Div([dcc.Graph(id="line-fig")])
                    ]
                ),

                html.Div(
                    id = "spark-container",
                    className = "four columns",
                    children = [

                         html.Div([dcc.Graph(id="spark-fig", config={'displayModeBar': False})])
                    ]
                ),
            ]        
        ),
])

#-------------------------CALLBACKS to udpate figures-------------------------------------------

#Create callback for us choropleth map
#The map is reactive to two inputs, which are the slider and dropdown
#Thus they are placed in a list to indicate that there are multiple inputs
#for the figure with id 'us-map'

@app.callback(
    dash.dependencies.Output('donut-fig', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_donut(dropdown):
    fig = generate_donut_chart(vaccines, dropdown)
    return fig


@app.callback(
    dash.dependencies.Output('line-fig', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_multiline(dropdown):
    fig = generate_line_plot(state_data, dropdown)
    return fig

@app.callback(
    dash.dependencies.Output('spark-fig', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_sparkline(dropdown):
    fig = create_spark_lines(cases_deaths, dropdown)
    return fig




#---------------------launch app----------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)