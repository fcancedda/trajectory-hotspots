import json
import plotly as py
import plotly.graph_objs as go


def grab_map_points(geoJSON):
    pts = []  # list of points defining boundaries of polygons
    for feature in geoJSON['features']:  # for each region in china
        if feature['geometry']['type'] == 'Polygon':
            pts.extend(feature['geometry']['coordinates'][0])
            pts.append([None, None])  # mark the end of a polygon
    x, y = zip(*pts)
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='China')
    return trace


def retrieve_map_trace():
    with open("app/data/map/geojson-map-china-master/china.json") as json_file:
        jdata = json_file.read()
        geoJSON = json.loads(jdata)

    trace_of_china = grab_map_points(geoJSON)
    return trace_of_china


def retrieve_user_trace(user_uid):
    user_data_points = []
    with open('app/data/parsed/output_' + user_uid + '.txt') as f:
        for line in f:
            lat, lng, date, time = line.strip('\n').split(',')[0:5]
            user_data_points.append((lat, lng))

        Y, X = zip(*user_data_points)
        # Create a trace
        user_trace = go.Scatter(
            x=X,
            y=Y,
            mode='markers',
            name=user_uid
        )
        return user_trace


data = []

china_traces = retrieve_map_trace()

data.append(china_traces)

for i in range(182):  # change to accommodate number of users
    user_str = '%03d' % i
    print(user_str + 'Start')
    user_trace = retrieve_user_trace(user_str)
    print(user_str + 'Done')
    data.append(user_trace)

py.offline.plot({
    "data": data,
    "layout": go.Layout(title="user data")
}, auto_open=True)

