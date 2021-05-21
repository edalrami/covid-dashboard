import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

#choropleth map function figure 1
def generate_map_object(input_):
    '''
    Returns a plotly chloropleth graph object
    input: 
        input_: A dataframe of containing total doses data
        
    returns:
        fig: A chloropleth graph object of US and doses administered per 100k by State
    ''' 
    
    df = input_.copy()
    z_ = df["Doses Administered per 100k by State where Administered"].round()
    
    df['text'] = '<br><b>State: <b>' + df['State/Territory/Federal Entity'] + '<br>' + '<b>Total Doses: <b>' + df["Total Doses Administered by State where Administered"].astype(str) + '<br>'
    
    
    fig = go.Figure(data=go.Choropleth(
       
        locations=df.location_code,
        z=z_,
        zmin = int(np.round(z_.min(),2)),
        zmax = int(np.round(z_.max(),2)),
        locationmode='USA-states',
        colorscale='RdPu',
        autocolorscale=False,
        text=df["text"],
        marker_line_color='white', # line markers between states
        name = "",
        colorbar_title="Doses per 100k",
        hovertemplate = '%{text}' +
                        '<b>Doses Per 100k</b>: <b>%{z}</b>'
        
     
    ))

    fig.update_layout(
        
        height=500,
        width=700,
        title_text= 'Doses Aministered per 100k Persons Of The Total Population',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
    )
    
    return fig

#Bar chart figure 2
def generate_bar_plot(input_):
    '''
    Returns a plotly chloropleth graph object
    input: 
        input_: A dataframe of containing total state doses data
        
    returns:
        fig: A Bar Chart with the top 10 and bottom 10 ranked states/territories in doses administered per 100k.
    ''' 

    top10 = input_[["Doses Administered per 100k by State where Administered", "State/Territory/Federal Entity"]].sort_values(by="Doses Administered per 100k by State where Administered", ascending =False).reset_index(drop=True)
    bottom10 = top10.tail(10)
    top10 = top10.head(10)

    fig = make_subplots(rows=1, cols=2, horizontal_spacing = 0.4)

    fig.add_trace(go.Bar(orientation = "h",
                          y=top10["State/Territory/Federal Entity"],
                          x=top10["Doses Administered per 100k by State where Administered"],
                          text=top10["Doses Administered per 100k by State where Administered"].round().astype(int),
                          textposition = "auto",
                          name="Top 10"), row = 1, col = 1)
    fig.add_trace(go.Bar(orientation = "h",
                          y=bottom10["State/Territory/Federal Entity"],
                          x=bottom10["Doses Administered per 100k by State where Administered"],
                          text=bottom10["Doses Administered per 100k by State where Administered"].round().astype(int),
                          textposition = "auto",
                          name="Bottom 10"), row = 1, col = 2)


    fig.update_layout(height=500, width=700, title_text="Top and Bottom Rankings of Doses <br>Administered per 100k in US States/Territories")
    fig.update_yaxes(autorange = "reversed", row = 1, col = 1)
    fig.update_yaxes(autorange = "reversed", row = 1, col = 2)
    fig.update_xaxes(range = [0,120000], row = 1, col = 1)
    fig.update_xaxes(range = [0,120000], row = 1, col = 2)
    return fig


#line plot figure 3
def generate_line_plot(input_, state_):
    '''
    Returns a multiline graph object of vaccine data for a specfic US state.
    
    input parameters:
        input_: DataFrame containing data
        state_: String containing name of US State
    
    output:
        fig: A line plot figure object
    '''
    vaccine_data = ["people_fully_vaccinated_per_hundred", "people_vaccinated_per_hundred"]
    names_ = {"people_fully_vaccinated_per_hundred": "Fully Vaccinated", "people_vaccinated_per_hundred": "Received At Least 1 Dose"}
    fig = go.Figure()
    annotations = []
    colors = ['lime', "green"]
    color_ix = 0
    for i in vaccine_data:
        
        x_=list(input_[input_.location == state_].sort_values(by="date", ascending=True).date)
        y_=list(input_[input_.location == state_][i])

        line_size = 4
        mode_size = 12
        color_ = colors[color_ix]

        fig.add_trace(go.Scatter(x=x_, y=y_, mode='lines',
            name=names_[i],
            line=dict(color=color_, width=line_size),
            connectgaps=True,
            showlegend=True
        ))

        # endpoints
        max_val = max(y_)
        max_ix = x_[-1]
        fig.add_trace(go.Scatter(
            x=[max_ix],
            y=[max_val],
            name=names_[i],
            mode='markers+text',
            marker=dict(color=color_, size=mode_size),
            showlegend = False,
            text = '{}%'.format(round(max_val,2)),
            textposition = 'middle right'
        ))
        
        color_ix = color_ix + 1
        
    
    fig.update_layout(
        width = 520,
        height = 500,
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text='Vaccinations Per 100 People: ' + state_,
                                  font=dict(family='Arial',
                                            size=16,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Source: United States Center For Disease Control and Prevention',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))
    
    
    fig.update_layout(annotations=annotations, showlegend=True, legend_orientation='h', legend=dict(x=0, y=1.04))
    
    return fig


#Spark lines plot figure 3
def create_spark_lines(input_, location_):
    df = input_.copy()
    df = input_[input_.state == location_].sort_values(by="submission_date").reset_index(drop=True)
    df = df.fillna(method='ffill')
    df = df.drop(["state"], axis=1)
    df = df.set_index("submission_date")
    df = df.rename_axis(index="submission_date", columns = "Daily Totals")
    
    spark_lines = px.line(df, facet_row="Daily Totals", facet_row_spacing=0.01, height=500, width=400)

    # hide and lock down axes
    spark_lines.update_xaxes(visible=False, fixedrange=True)
    spark_lines.update_yaxes(visible=False, fixedrange=True, matches=None)
    spark_lines.add_vline(x="2020-12-14", 
                          line_width=2, 
                          line_dash="dash", 
                          line_color = "black",
                          #line_color='rgb(150,150,150)',
                          row="all", col = 1)
    # remove facet/subplot labels
    spark_lines.update_layout(annotations=[], overwrite=True)

    # strip down the rest of the plot
    spark_lines.update_layout(
        title=location_ + " COVID19 Totals <br> After First Vaccine Availability In US",
        title_font_size = 16,
        showlegend=True,
        legend = dict(x=1, y = 0),
        plot_bgcolor="white",
        margin=dict(t=35,l=10,b=10,r=10)
    )
    
    spark_lines.add_vline(x="2020-12-14", 
                          line_width=2, 
                          line_dash="dash", 
                          line_color = "black",
                          #line_color='rgb(150,150,150)',
                          row="all", col = 1)
    
    return spark_lines


def generate_donut_chart(input_, location_):
    
    df = input_[input_.Jurisdiction == location_]
    df = df.drop(["Jurisdiction", "Week of Allocations", "2nd Dose Allocations"], axis = 1)
    vaccine_totals = df.groupby(["type"]).sum()
    vaccine_totals.sort_values(by="type", inplace=True)
    vaccine_totals["Percentage"] = round((vaccine_totals["1st Dose Allocations"]/vaccine_totals["1st Dose Allocations"].sum())*100, 2)
    labels_ = ["Johnson & Johnson", "Moderna", "Pfizer"]
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels_, values=vaccine_totals["Percentage"].values, hole=.3)])
    fig.update_layout(height=500, 
                      width=500, 
                      title_font_size = 16,
                      title={
                             'text': "Distribution Allocations :" + location_,
                             'y':0.85,
                             'x':0.5,
                             'xanchor': 'center',
                             'yanchor': 'top'})
    return fig