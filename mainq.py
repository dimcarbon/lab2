from spyre import server
import pandas as pd

class MyApp(server.App):
    title = "tables"

    inputs = [{     "type":'dropdown',
                    "label": 'Index',
                    "options" : [ {"label": "VCI", "value":"VCI"},
                                  {"label": "TCI", "value":"TCI"},
                                  {"label": "VHI", "value":"VHI"}],
                    "key": 'index',
                    "action_id": "update_data"},

              {     "input_type":'dropdown',
                    "label": 'Area',
                    "options" : [ {"label": "Cherkasy", "value":"01"},
                                    {"label": "Chernihiv", "value":"02"} ,
                                    {"label": "Chernivtsi", "value":"03"} ,
                                    {"label": "Crimea", "value":"4"} ,
                                    {"label": "Dnipropetrovs'k", "value":"05"},
                                    {"label": "Donets'k", "value":"06"},
                                    {"label": "Ivano-Frankivs'k", "value":"07"},
                                    {"label": "Kharkiv", "value":"08"},
                                    {"label": "Kherson", "value":"09"},
                                    {"label": "Khmel'nits'kyy", "value":"10"} ,
                                    {"label": "Kiev", "value":"11"},
                                    {"label": "KievCity", "value":"12"},
                                    {"label": "Kirovohrad", "value":"13"},
                                    {"label": "Luhans'k", "value":"14"},
                                    {"label": "L'viv", "value":"15"},
                                    {"label": "Mykolayiv", "value":"16"},
                                    {"label": "Odessa", "value":"17"},
                                    {"label": "Poltava", "value":"18"},
                                    {"label": "Rivne", "value":"19"},
                                    {"label": "Sevastopol'", "value":"20"},
                                    {"label": "Sumy", "value":"21"},
                                    {"label": "Ternopil'", "value":"22"} ,
                                    {"label": "Zacarpathia", "value":"23"},
                                    {"label": "Vinnytsya", "value":"24"},
                                    {"label": "Volyn", "value":"25"},
                                    {"label": "Zaporizhzhya", "value":"26"},
                                    {"label": "Zhytomyr", "value":"27"}
                                 ],
                    "key": 'area',
                    "action_id": "update_data"
                    },
              {
                    "type":'slider',
                    "label":'Year',
                    "value":'2000',
                    "max":'2016',
                    "min":'1981',
                    "key":'year',
                    "action_id": "update_data"
              },
              {
                    "input_type":'slider',
                    "label":'Weeks: from (min value is the default)',
                    "value":'1',
                    "max":'52',
                    "min":'1',
                    "key":'week1',
                    "action_id": "update_data"
              },
              {
                    "input_type":'slider',
                    "label":'to (max value is the default)',
                    "value":'52',
                    "max":'52',
                    "min":'1',
                    "key":'week2',
                    "action_id": "update_data"
              }
              ]

    controls = [{   "type" : "hidden",
                    "id" : "update_data"
                }]

    tabs = ["Plot", "Table"]

    outputs = [
                { "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]

    def getData(self, params):
        city = int(params['area'])
        url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1=1981&year2=2017&type=Mean".format(city)
        data = pd.read_csv(url,index_col=False, header=1, skipfooter=1, engine='python',
                     names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'], delimiter='\,\s+|\s+|\,')
        df = data[data.year == int(params['year'])][data.week >= int(params['week1'])][data.week <= int(params['week2'])][["year", "week", params['index']]]
        return df

    def getPlot(self, params):
        df = self.getData(params).set_index('week').drop(['year'],axis=1)
        plt_obj = df.plot()
        plt_obj.set_ylabel(params['index'])
        fig = plt_obj.get_figure()
        return fig

app = MyApp()
app.launch(port=9022)