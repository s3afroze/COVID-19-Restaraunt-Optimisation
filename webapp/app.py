import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

# Dictionary of important osmow's stores
list_of_locations = {'1 Kennedy Rd S': {'lon': -79.25569611653174, 'lat': 43.702583795662534},
 '10635 Bramalea Rd #3': {'lon': -79.72340999999994, 'lat': 43.72135000000003},
 '120 Clementine Dr #5': {'lon': -79.22881500934116, 'lat': 43.7755457634258},
 '126 Wellington Street West, unit 108': {'lon': -79.3833030256713, 'lat': 43.64664282548623},
 '1380 Lasalle Boulevard Unit # E2': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '140 Hwy 8 Unit 10A': {'lon': -79.50692534332316, 'lat': 43.601552272638266},
 '1447 Water Street, Unit 2&3': {'lon': -79.29663975, 'lat': 43.680028500000006},
 '1472 Innisfil Beach Road': {'lon': -79.53046374709079, 'lat': 44.22640447090783},
 '1500 Elgin Mills Road East Unit 1': {'lon': -79.34704744953514, 'lat': 43.75522623980035},
 '170 Sandalwood Pkwy E': {'lon': -79.35708443140246, 'lat': 43.74318331890051},
 '1746 Victoria Park Ave': {'lon': -79.30745138206483, 'lat': 43.73616768523925},
 '190 Bell Blvd, Unit 10A': {'lon': -79.53647087527986, 'lat': 43.72448067743742},
 '1900 Simcoe St N, Unit 103': {'lon': -79.69523033755091, 'lat': 44.39007245404853},
 '2 Douglas Rd - Unit A30': {'lon': -79.36764085830119, 'lat': 43.69059041799863},
 '200 Green Lane E, Building E11, Unit #3': {'lon': -79.41100591968375, 'lat': 43.72910785294566},
 '2021 Green Road - Unit 107': {'lon': -79.36288090437705, 'lat': 43.7399296661112},
 '2040 Algonquin rd, Unit 13A': {'lon': -79.35762348803861, 'lat': 43.6276403267663},
 '210 King Street North': {'lon': -79.50688809714923, 'lat': 43.70807410687276},
 '22 Fairview Dr, Unit 16': {'lon': -79.35602615251885, 'lat': 43.67512017236992},
 '2215 Steeles Ave W': {'lon': -79.4768730777022, 'lat': 43.78564985648354},
 '2406 Bloor St W': {'lon': -79.48319831585773, 'lat': 43.649635074124184},
 '2435 Appleby Line': {'lon': -79.54983032503472, 'lat': 43.653772950208335},
 '2439 Yonge St': {'lon': -79.39917553424914, 'lat': 43.71078981349182},
 '25 Brisdale Dr #3': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '251 Queen St S #1': {'lon': -79.50622387440136, 'lat': 43.707262925875845},
 '2583 St. Clair Ave West, Unit 2': {'lon': -79.48943165700267, 'lat': 43.66759256718332},
 '2620 Rutherford Rd': {'lon': -79.49625254936934, 'lat': 43.690444610392966},
 '3-25 Stonebridge Blvd': {'lon': -79.32282043003077, 'lat': 43.800540851520516},
 '30 Diana Dr, Building 4,Unit 1': {'lon': -79.48709647905241, 'lat': 43.740887300046055},
 '3221 Derry Rd W #8': {'lon': -79.61951331619214, 'lat': 43.718726766357605},
 '347 Dalhousie street': {'lon': -79.37619299747095, 'lat': 43.655807806619976},
 '351 College St': {'lon': -79.40346351941838, 'lat': 43.65731682373493},
 '355 Hespeler Rd': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '400 Scott Street': {'lon': -79.47274375926933, 'lat': 43.690622097105724},
 '4188 Living Arts Dr #4': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '4205 Keele St #6': {'lon': -79.49341386623664, 'lat': 43.773445654192294},
 '459 Holland Street West, Unit 6': {'lon': -79.41327306950357, 'lat': 43.67676803089047},
 '470 Chrysler Dr #21': {'lon': -79.30669825336496, 'lat': 43.744624406760465},
 '4850 Dundas Street West': {'lon': -79.5271344131512, 'lat': 43.65060080933688},
 '494 Big Bay Point Rd': {'lon': -79.49460880586429, 'lat': 43.6568248254777},
 '5 Mountainview Rd N': {'lon': -79.46105724680088, 'lat': 43.65469544568467},
 '500 Rexdale Blvd, Unit M017': {'lon': -79.59693325212817, 'lat': 43.71773918252375},
 '5083 Dixie Rd': {'lon': -79.56035727190087, 'lat': 43.591013894336555},
 '5261 Highway 7 - Unit B102': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '547 Cundles Rd E': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '555 Essa Road, Unit A9': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '5777 Main Street - #103': {'lon': -79.3015730947625, 'lat': 43.68742047758703},
 '5934 Victoria Ave': {'lon': -79.50881924999999, 'lat': 43.697448},
 '5945 Latimer Dr, Unit 9': {'lon': -79.41653278858449, 'lat': 43.70509575654498},
 '600 Lakeshore Rd E': {'lon': -79.34702671730138, 'lat': 43.65120392495528},
 '605 Rogers Rd': {'lon': -79.47450596710719, 'lat': 43.681830539529265},
 '611 Queen St W': {'lon': -79.40242487301637, 'lat': 43.647483783772984},
 '628 King St N': {'lon': -79.29922324543719, 'lat': 43.67873898581877},
 '655 Fairway Rd. S,Unit B7': {'lon': -79.52866875, 'lat': 43.654707},
 '6640 Finch Ave W': {'lon': -79.60587044892955, 'lat': 43.73376948268776},
 '6795 Airport Road, Unit A3': {'lon': -79.39597303368889, 'lat': 43.632057620788906},
 '7 Rossland Rd E, Unit 103, Building B': {'lon': -79.54473833172906, 'lat': 43.59986589696982},
 '750 Richmond St.': {'lon': -79.40871356148645, 'lat': 43.645467183478424},
 '790 Military Trail': {'lon': -79.19566148845881, 'lat': 43.78973898366869},
 '80 Courtneypark Dr E': {'lon': -79.38543999999996, 'lat': 43.648690000000045},
 '820 Kingston Rd': {'lon': -79.29235012101101, 'lat': 43.68016847100232},
 '8630 Woodbine Ave, Markham': {'lon': -79.35895670025916, 'lat': 43.852998899401555},
 '8750 Bayview Ave': {'lon': -79.35552481813586, 'lat': 43.65988194471682},
 '95 The Pond Road Building C2, unit 40': {'lon': -79.50122401636143, 'lat': 43.770200086409545},
 '96 First Street, Unit 1B': {'lon': -79.35451745680703, 'lat': 43.63315865191743},
 '9750 Markham Rd': {'lon': -79.24349063017577, 'lat': 43.80948291372859}}

 
weekdays_numbers = {0:'Monday', 1: 'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}

df = pd.read_csv("data/full_data.csv", index_col=[0])
df["Date/Time"] = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M")
df.index = df["Date/Time"]
df.drop("Date/Time", 1, inplace=True)

demand_data = pd.read_csv("data/demand_data_week.csv", index_col=[0])
demand_data["Date/Time"] = pd.to_datetime(demand_data.index, format="%Y-%m-%d %H:%M")
demand_data.index = demand_data["Date/Time"]
demand_data.drop("Date/Time", 1, inplace=True)

totalList = []
for month in demand_data.groupby(demand_data.index.month):
    dailyList = []
    for day in month[1].groupby(month[1].index.day):
        dailyList.append(day[1])
    totalList.append(dailyList)
totalList = np.array(totalList)

# print(totalList)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("COVID-19 Restaurant Solution"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different time frames on the histogram."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2020, 3, 30),
                                    max_date_allowed=dt(2021, 3, 30),
                                    initial_visible_month=dt(2020, 1, 1),
                                    date=dt(2020, 3, 30).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            value='120 Clementine Dr #5',
                                            placeholder="Select a location",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": str(n) + ":00",
                                                    "value": str(n),
                                                }
                                                for n in range(24)
                                            ],
                                            multi=True,
                                            placeholder="Select certain hours",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        # html.P(id="total-rides"),
                        # html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Select any of the bars on the histogram to section data by time."
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

# Gets the amount of days in the specified month
# Index represents month (0 is April, 1 is May, ... etc.)
daysInMonth = [30, 31, 30, 31, 31, 30]

# Get index for the specified month in the dataframe
monthIndex = pd.Index(["Apr", "May", "June", "July", "Aug", "Sept"])

# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(month, day, selection, name_of_day):
    print(f'month {month}')
    print(f'day {day}')
    xVal = []
    yVal = []
    xSelected = []
    colorVal = [
        "#F4EC15",
        "#DAF017",
        "#BBEC19",
        "#9DE81B",
        "#80E41D",
        "#66E01F",
        "#4CDC20",
        "#34D822",
        "#24D249",
        "#25D042",
        "#26CC58",
        "#28C86D",
        "#29C481",
        "#2AC093",
        "#2BBCA4",
        "#2BB5B8",
        "#2C99B4",
        "#2D7EB0",
        "#2D65AC",
        "#2E4EA4",
        "#2E38A4",
        "#3B2FA0",
        "#4E2F9C",
        "#603099",
    ]
    loc_data = demand_data[demand_data["Addr"] == selection]

    # Put selected times into a list of numbers xSelected
    # xSelected.extend([int(x) for x in selection])
    xVal = [i for i in range(24)]
    yVal = list(loc_data[name_of_day][:24])

    return [np.array(xVal), np.array(yVal), np.array(colorVal)]


# Selected Data in the Histogram updates the Values in the DatePicker
@app.callback(
    Output("bar-selector", "value"),
    [Input("histogram", "selectedData"), Input("histogram", "clickData")],
)
def update_bar_selector(value, clickData):
    holder = []
    if clickData:
        holder.append(str(int(clickData["points"][0]["x"])))
    if value:
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    print(clickData)
    if clickData:
        return {"points": []}


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input("date-picker", "date"), Input("location-dropdown", "value")],
)
def update_histogram(datePicked, selection):
    print(selection)
    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month - 4
    dayPicked = date_picked.day - 1
    
    name_of_day = weekdays_numbers[date_picked.weekday()]


    [xVal, yVal, colorVal] = get_selection(monthPicked, dayPicked, selection, name_of_day)

    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode="group",
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        dragmode="select",
        font=dict(color="white"),
        xaxis=dict(
            range=[-0.5, 23.5],
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=":00",
        ),
        yaxis=dict(
            range=[0, max(yVal) + max(yVal) / 4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode="nonnegative",
            zeroline=False,
        ),
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font=dict(color="white"),
            )
            for xi, yi in zip(xVal, yVal)
        ],
    )

    return go.Figure(
        data=[
            go.Bar(x=xVal, y=yVal, marker=dict(color=colorVal), hoverinfo="x"),
            go.Scatter(
                opacity=0,
                x=xVal,
                y=yVal / 2,
                hoverinfo="none",
                mode="markers",
                marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
                visible=True,
            ),
        ],
        layout=layout,
    )


# Get the Coordinates of the chosen months, dates and times
def getLatLonColor(selectedData, month, day):
    listCoords = totalList[month][day]

    # No times selected, output all times for chosen month and date
    if selectedData is None or len(selectedData) is 0:
        return listCoords
    listStr = "listCoords["
    for time in selectedData:
        if selectedData.index(time) is not len(selectedData) - 1:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ") | "
        else:
            listStr += "(totalList[month][day].index.hour==" + str(int(time)) + ")]"
    return eval(listStr)



# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "date"),
        Input("bar-selector", "value"),
        Input("location-dropdown", "value"),
    ],
)


def update_graph(datePicked, selectedData, selectedLocation):
    print(selectedData)
    zoom = 12.0
    latInitial = 43.773694
    lonInitial = -79.501911
    bearing = 0

    if selectedLocation:
        zoom = 15.0
        latInitial = list_of_locations[selectedLocation]["lat"]
        lonInitial = list_of_locations[selectedLocation]["lon"]

    date_picked = dt.strptime(datePicked, "%Y-%m-%d")
    monthPicked = date_picked.month - 4
    dayPicked = date_picked.day - 1
    listCoords = getLatLonColor(selectedData, monthPicked, dayPicked)

    return go.Figure(
        data=[
            # Data for all rides based on date and time
            Scattermapbox(
                lat=listCoords["Lat"],
                lon=listCoords["Lon"],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=listCoords.index.hour,
                marker=dict(
                    showscale=True,
                    color=np.append(np.insert(listCoords.index.hour, 0, 0), 23),
                    opacity=0.5,
                    size=5,
                    colorscale=[
                        [0, "#F4EC15"],
                        [0.04167, "#DAF017"],
                        [0.0833, "#BBEC19"],
                        [0.125, "#9DE81B"],
                        [0.1667, "#80E41D"],
                        [0.2083, "#66E01F"],
                        [0.25, "#4CDC20"],
                        [0.292, "#34D822"],
                        [0.333, "#24D249"],
                        [0.375, "#25D042"],
                        [0.4167, "#26CC58"],
                        [0.4583, "#28C86D"],
                        [0.50, "#29C481"],
                        [0.54167, "#2AC093"],
                        [0.5833, "#2BBCA4"],
                        [1.0, "#613099"],
                    ],
                    colorbar=dict(
                        title="Time of<br>Day",
                        x=0.93,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(color="#d8d8d8"),
                        titlefont=dict(color="#d8d8d8"),
                        thicknessmode="pixels",
                    ),
                ),
            ),
            # Plot of important locations on the map
            Scattermapbox(
                lat=[list_of_locations[i]["lat"] for i in list_of_locations],
                lon=[list_of_locations[i]["lon"] for i in list_of_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in list_of_locations],
                marker=dict(size=8, color="#ffa0a0"),
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "-79.501911",
                                        "mapbox.center.lat": "43.773694",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )


if __name__ == "__main__":
    app.run_server(debug=False)
