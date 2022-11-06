from dash import Dash, html, dcc
from dash import Dash, dcc, html, Output, Input, State, ALL
import dash_bootstrap_components as dbc
from fight_lib import *
from fight_modifiers import *
from wound_modifiers import *
from rolloff_modifiers import *

class FightTab:

    LABEL   = "Fight"
    ID      = "fight-tab"
    DATA_ID = "fight-tab-data"



    def build_tab(self):
        tabcard = dbc.Card(
            dbc.CardBody(
                html.Div(id=self.DATA_ID,
                style={'display': 'inline-block', 'width': '95%'},
                children=self.tab_contents())
            )
        )
        return tabcard


    def register_callbacks(self, app):
        self.build_tab()


        @app.callback(Output("win-fight-container", "children"), 
                        Output("damage-graph", "figure"),
                        Input("calculate-button", "n_clicks"),
                        State({"input":"atk_input", "name":ALL}, 'value'), 
                        State({"input":"def_input", "name":ALL}, 'value'),
                        State({"type":"modifier", "name":ALL}, 'value'))
        def calculate(n_clicks, atk_stats, def_stats, modifiers):
            print(def_stats)
            f = FightRoller(atk_stats, def_stats, modifiers)
            wounds_hist = f.wounds()
            return f.GetWinRate(), wounds_hist







    def tab_contents(self):
        
        input_col = dbc.Col([
                        html.H2("Input Options"), 
                        html.Hr(),


                        dbc.Row([

                            dbc.Col([
                                html.H4("Attacker Profile"),
                                html.Br(),
                                html.H5("Fight Value"),
                                dcc.Input(id={"name":"atk-fv-input",
                                              "input":"atk_input"},
                                    type="number",
                                    min=1,
                                    value=1),
                                html.Br(),

                                html.Br(), 
                                html.H5("Strength"),
                                dcc.Input(id={"name":"atk-strength-input",
                                              "input":"atk_input"},
                                    type="number",
                                    min=1,
                                    value=1),
                                html.Br(),


                                html.Br(), 
                                html.H5("Attacks"),
                                dcc.Input(id={"name":"atk-attacks-input",
                                              "input":"atk_input"},
                                    type="number",
                                    min=1,
                                    value=1),
                                html.Br()
                            ]),

                            dbc.Col([
                                html.H4("Defender Profile"),
                                html.Br(),
                                html.H5("Fight Value"),
                                dcc.Input(id={"name":"def-fv-input",
                                              "input":"def_input"},
                                    type="number",
                                    min=1,
                                    value=1),
                                html.Br(),

                                html.Br(), 
                                html.H5("Defence"),
                                dcc.Input(id={"name":"def-defence-input",
                                              "input":"def_input"},
                                    type="number",
                                    min=1,
                                    value=1),
                                html.Br(),


                                html.Br(), 
                                html.H5("Attacks"),
                                dcc.Input(id={"name":"def-attacks-input",
                                              "input":"def_input"},
                                type="number",
                                    min=1,
                                    value=1),
                                html.Br()
                            ])                        

                        ]), 

                        # Modifiers
                        html.Br(),
                        html.H4("Duel Roll Modifiers"),
                        html.Hr(),
                        dbc.Row([

                            dbc.Col([
                                html.H5("Attacker Modifiers"),
                                dcc.Checklist(list(duel_roll_modifiers_dict().keys()), id={"name":"atk-duel-roll-modifiers-checklist", "type":"modifier"}),
                                html.Br(),
                                html.H5("Roll Off Modifiers"),
                                dcc.Checklist(list(atk_rolloff_modifiers_dict().keys()), id={"name":"atk-rolloff-modifiers-checklist", "type":"modifier"}),
                                html.Br(),
                                html.H5("Wound Modifiers"),
                                dcc.Checklist(list(wound_modifiers_dict().keys()), id={"name":"wound-modifiers-checklist", "type":"modifier"})
                            ]),


                            dbc.Col([
                                html.H5("Defender Modifiers"),
                                dcc.Checklist(list(duel_roll_modifiers_dict().keys()), id={"name":"def-duel-roll-modifiers-checklist", "type":"modifier"}),
                                html.Br(),
                                html.H5("Roll Off Modifiers"),
                                dcc.Checklist(list(def_rolloff_modifiers_dict().keys()), id={"name":"def-rolloff-modifiers-checklist", "type":"modifier"}),
                                html.Br()

                            ]),

                        ]), 
                        html.Br(), 
                        html.Button("Calculate", id="calculate-button")

                    ])
        
        
        
        
        
        
        output_col = dbc.Col([
                        html.H2("Odds"), 
                        html.Hr(),
                        html.H5("Win the Fight"),
                        html.Div(id="win-fight-container"),
                        html.Hr(),
                        html.H5("Potential Damage"), 
                        dcc.Graph(id="damage-graph")
                    ])
        
        
        return [
            dbc.Row(
                [input_col, 
                output_col]
            )]