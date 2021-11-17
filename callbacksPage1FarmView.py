from dash.dependencies import Input, Output, State
import page1FarmView
from app import app
import farmView.Farm_View as FV
from pandas import read_hdf
import turbineView.Analysis_Tools as AT
import Tab1DbManager
import TrendMonitoring

@app.callback(
    Output('farm-view', "children"),
    [Input("overview-card-tabs", "active_tab")],
)
def generate_overview_tabs(at):
    if at == "farm-view":
        return page1FarmView.farm_view_tabs
    elif at == "turbine-view":
        return page1FarmView.turbine_view_content
    elif at == "db-manager":
        return Tab1DbManager.generate_main_tabs()
    elif at == "trend-monitoring":
        return TrendMonitoring.content


@app.callback(
    Output('tabs-farm-view-div', "children"),
    [Input("farm-view-tabs", "active_tab")],
)
def generate_farmview_tabs(at):
    if at == "tab-live-data":
        return page1FarmView.generate_liveData_farm()


@app.callback(
    [Output('farm-speed-card', "children"),
     Output('farm-generation-card', "children"),
     Output('farm-freq-card', "children"),
     Output('farm-temperature-card', "children")],
    [Input("select-farm", 'value')]
)
def generate_farmview_cards(farm):
    live_data_output = FV.live_data_cards(farm)
    farm_speed = live_data_output[0]
    farm_power = live_data_output[1]
    farm_freq = live_data_output[2]
    farm_temp = live_data_output[3]
    return farm_speed, farm_power, farm_freq, farm_temp


@app.callback(
    [Output('checklist-WT-selection', 'options'),
     Output('checklist-WT-selection', 'value')],
    [Input("select-farm", "value")]
)
def gen_checklist(farm_name):
    #Based On File
    # df = read_hdf("./farmView/{}/livedataTable".format(farm_name))
    # options = [{'label': i, 'value': i} for i in df['Name']]
    # value = df['Name']
    #Static
    ops = ['WTG 01','WTG 02','WTG 03','WTG 04','WTG 05','WTG 06','WTG 07','WTG 08','WTG 09',
           'WTG 10','WTG 11','WTG 12','WTG 13','WTG 14','WTG 15','WTG 16','WTG 17','WTG 18','WTG 19','WTG 20','WTG 21','WTG 22']
    options = [{'label': i, 'value': i} for i in ops]
    value = ops

    return options, value


@app.callback(
    Output('table-container-live-data', "children"),
    [Input("select-farm", "value"),
     Input("checklist-WT-selection", "value")],
)
def generate_livedata_table(farm_name, checklist_value):
    return AT.generate_live_data_table(farm_name,checklist_value)


