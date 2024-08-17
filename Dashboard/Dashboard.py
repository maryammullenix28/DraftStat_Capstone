import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from shiny import App, Inputs, Outputs, Session, reactive, ui, render

final_qb_data = pd.read_csv("final_qb_data.csv")
final_rb_data = pd.read_csv("final_rb_data.csv")
final_wr_data = pd.read_csv("final_wr_data.csv")
final_te_data = pd.read_csv("final_te_data.csv")

qb_num_vars = {'G':'Games Played', 'Pass Com':'Passes Completed', 'Pass Att':'Passes Attempted',
               'Pass Yds':'Passing Yards', 'Pass TD':'Passing Touchdowns', 'Int':'Interceptions',
               'Pass_Yds/Att':'Passing Yards per Attempt', 'Pass_Com/G':'Passes Completed per Game',
               'Pass_Yds/G':'Passing Yards per Game', 'Pass_TD/G':'Passing Touchdowns per Game', 'Int/G':'Interceptions per Game'}
rb_num_vars = {'G':'Games Played', 'Rush':'Rush Attempts', 'Rush Yds':'Rushing Yards', 'Rush TD':'Rushing Touchdowns',
               'Rush Yds/Att':'Rushing Yards per Attempt', 'Rush Yds/G':'Rushing Yard per Game', 'Rush TD/G':'Rushing Touchdowns per Game'}
wr_num_vars = {'G':'Games Played', 'Rec':'Receptions', 'Rec Yds':'Recieving Yards', 'Rec TD':'Recieving Touchdowns',
               'Rec Yds/Rec':'Recieving Yards per Reception', 'Rec Yds/G':'Recieving Yards per Game', 'Rec TD/G':'Recieving Touchdowns per Game'}
te_num_vars = {'G':'Games Played', 'Rec':'Receptions', 'Rec Yds':'Recieving Yards', 'Rec TD':'Recieving Touchdowns',
               'Rec Yds/Rec':'Recieving Yards per Reception', 'Rec Yds/G':'Recieving Yards per Game', 'Rec TD/G':'Recieving Touchdowns per Game'}

fbs_confs = ['Any','AAC', 'ACC', 'Big 12', 'Big Ten', 'CUSA', 'FBS Independent','Independent', 'MAC', 'Mountain West', 'Pac-12', 'SEC', 'Sun Belt']
fcs_confs = ['Any','ASUN', 'Big Sky', 'Big South', 'CAA', 'FCS Independent', 'Ivy League','MEAC', 'MVFC', 'NEC', 'OVC', 'Patriot', 'Pioneer', 'SWAC', 'SoCon','Southland', 'WAC']
all_confs = fbs_confs + fcs_confs 

app_ui = ui.page_fixed(  
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.output_image("logo", inline = True, width = "100%"),
            ui.input_select("pos", "Position:", ['Quarterback','Running Back','Wide Reciever','Tight End'], selected='Quarterback'),
            ui.input_select("div", "Division:", ['Any','FBS','FCS'], selected='Any'),
            ui.input_select("conf", "Conference:", all_confs, selected='Any'),
            ui.input_select("var_filter", "Filter Variable:", {'G':'Games Played'}, selected=None),
            ui.input_slider("filter", "", min=0, max=61, value=[0,61]),
            style="color:white; background:#294BA1 !important;",bg = '#294BA1',
        ),
        ui.panel_main(
            ui.input_select("var_y", "Y Variable:", {'G':'Games Played'}, selected=None),
            ui.input_select("var_x", "X Variable:", {'G':'Games Played'}, selected=None),
            ui.output_plot("scatter_plot"),
            ui.input_select("var_box", "Variable for Comparison:", {'G':'Games Played'}, selected=None),
            ui.output_plot("box_plot"),
        bg = 'black'),
    ),
)

def server(input, output, session):
    @render.image  
    def logo():
        img = {"src": "logo.png"}  
        return img
    
    @reactive.effect
    def conf_update():
        x = "Any"
        x = input.div()
        choice_vars = []

        # Can use [] to remove all choices
        if x == 'Any':
            choice_vars = all_confs
        elif x == 'FBS':
            choice_vars = fbs_confs
        elif x == 'FCS':
            choice_vars = fcs_confs

        ui.update_select(
            "conf",
            label="Conference:",
            choices=choice_vars,
            selected= "Any")
    
    @reactive.effect
    def var_y_update():
        x = "Quarterback"
        x = input.pos()
        choice_vars = []

        # Can use [] to remove all choices
        if x == 'Quarterback':
            choice_vars = qb_num_vars
        elif x == 'Running Back':
            choice_vars = rb_num_vars
        elif x == 'Wide Reciever':
            choice_vars = wr_num_vars
        elif x == 'Tight End':
            choice_vars = te_num_vars

        ui.update_select(
            "var_y",
            label="Y Variable:",
            choices=choice_vars,
            selected= None)
        
    @reactive.effect
    def var_x_update():
        x = "Quarterback"
        x = input.pos()
        choice_vars = []

        # Can use [] to remove all choices
        if x == 'Quarterback':
            choice_vars = qb_num_vars
        elif x == 'Running Back':
            choice_vars = rb_num_vars
        elif x == 'Wide Reciever':
            choice_vars = wr_num_vars
        elif x == 'Tight End':
            choice_vars = te_num_vars

        ui.update_select(
            "var_x",
            label="X Variable:",
            choices=choice_vars,
            selected= None)
    
    @reactive.effect
    def var_filter_update():
        x = "Quarterback"
        x = input.pos()
        choice_vars = []

        # Can use [] to remove all choices
        if x == 'Quarterback':
            choice_vars = qb_num_vars
        elif x == 'Running Back':
            choice_vars = rb_num_vars
        elif x == 'Wide Reciever':
            choice_vars = wr_num_vars
        elif x == 'Tight End':
            choice_vars = te_num_vars

        ui.update_select(
            "var_filter",
            label="Filter Variable:",
            choices=choice_vars,
            selected= None)
        
    @reactive.effect
    def filter_update():
        pos = "Quarterback"
        pos = input.pos()
        div = input.div()
        conf = input.conf()
        df = pd.DataFrame()

        # Can use [] to remove all choices
        if pos == 'Quarterback':
            df = final_qb_data
        elif pos == 'Running Back':
            df = final_rb_data
        elif pos == 'Wide Reciever':
            df = final_wr_data
        elif pos == 'Tight End':
            df = final_te_data
        
        if div == 'Any':
            df = df
        elif div != 'Any':
            df = df[df.Division == div]
        
        if conf == 'Any':
            df = df
        elif conf != 'Any':
            df = df[df.Conference == conf]
            
        var = df[input.var_filter()]  
        var_rng = [min(var),max(var)]
        
        ui.update_slider(
            "filter",
            label="",
            min=var_rng[0], max=var_rng[1], value=var_rng)
    
    @reactive.effect
    def var_box_update():
        x = "Quarterback"
        x = input.pos()
        choice_vars = []

        # Can use [] to remove all choices
        if x == 'Quarterback':
            choice_vars = qb_num_vars
        elif x == 'Running Back':
            choice_vars = rb_num_vars
        elif x == 'Wide Reciever':
            choice_vars = wr_num_vars
        elif x == 'Tight End':
            choice_vars = te_num_vars

        ui.update_select(
            "var_box",
            label="Variable for Comparison:",
            choices=choice_vars,
            selected= None)
    
    @render.plot(alt="Scatter Plot")  
    def scatter_plot():
        pos = "Quarterback"
        pos = input.pos()
        div = input.div()
        conf = input.conf()
        fltr = input.filter()
        df = pd.DataFrame()

        # Can use [] to remove all choices
        if pos == 'Quarterback':
            df = final_qb_data
        elif pos == 'Running Back':
            df = final_rb_data
        elif pos == 'Wide Reciever':
            df = final_wr_data
        elif pos == 'Tight End':
            df = final_te_data
        
        if div == 'Any':
            df = df
        elif div != 'Any':
            df = df[df.Division == div]
        
        if conf == 'Any':
            df = df
        elif conf != 'Any':
            df = df[df.Conference == conf]
        
        df = df[df[input.var_filter()].between(fltr[0],fltr[1])]
        
        y_Y = df[input.var_y()][df['Drafted?']=='Y']
        x_Y = df[input.var_x()][df['Drafted?']=='Y']
        y_N = df[input.var_y()][df['Drafted?']=='N']
        x_N = df[input.var_x()][df['Drafted?']=='N']
        
        if len(x_Y)>0 and len(x_N)>0:
        
            a_Y, b_Y = np.polyfit(x_Y, y_Y, 1)
            a_N, b_N = np.polyfit(x_N, y_N, 1)

            fig, ax = plt.subplots()
            ax.scatter(x_Y, y_Y, c='lightgreen',label = 'Drafted', alpha = 0.75)
            ax.plot(x_Y, a_Y*x_Y+b_Y, c='g')
            ax.scatter(x_N, y_N, c='pink',label = 'Undrafted', alpha = 0.75)
            ax.plot(x_N, a_N*x_N+b_N, c='r')
            ax.set_title("{} - {} vs {}".format(input.pos(),input.var_y(),input.var_x()))
            ax.set_xlabel(input.var_x())
            ax.set_ylabel(input.var_y())
            ax.legend()

            return fig  
        
        elif len(x_Y)>0:
        
            a_Y, b_Y = np.polyfit(x_Y, y_Y, 1)

            fig, ax = plt.subplots()
            ax.scatter(x_Y, y_Y, c='lightgreen',label = 'Drafted', alpha = 0.75)
            ax.plot(x_Y, a_Y*x_Y+b_Y, c='g')
            ax.set_title("{} - {} vs {}".format(input.pos(),input.var_y(),input.var_x()))
            ax.set_xlabel(input.var_x())
            ax.set_ylabel(input.var_y())
            ax.legend()

            return fig 
        
        elif len(x_N)>0:
        
            a_N, b_N = np.polyfit(x_N, y_N, 1)

            fig, ax = plt.subplots()
            ax.scatter(x_N, y_N, c='pink',label = 'Undrafted', alpha = 0.75)
            ax.plot(x_N, a_N*x_N+b_N, c='r')
            ax.set_title("{} - {} vs {}".format(input.pos(),input.var_y(),input.var_x()))
            ax.set_xlabel(input.var_x())
            ax.set_ylabel(input.var_y())
            ax.legend()

            return fig   
    
    @render.plot(alt="Box Plot")  
    def box_plot():
        pos = "Quarterback"
        pos = input.pos()
        div = input.div()
        conf = input.conf()
        fltr = input.filter()
        df = pd.DataFrame()

        # Can use [] to remove all choices
        if pos == 'Quarterback':
            df = final_qb_data
        elif pos == 'Running Back':
            df = final_rb_data
        elif pos == 'Wide Reciever':
            df = final_wr_data
        elif pos == 'Tight End':
            df = final_te_data
        
        if div == 'Any':
            df = df
        elif div != 'Any':
            df = df[df.Division == div]
        
        if conf == 'Any':
            df = df
        elif conf != 'Any':
            df = df[df.Conference == conf]
        
        df = df[df[input.var_filter()].between(fltr[0],fltr[1])]
        
        y_Y = df[input.var_box()][df['Drafted?']=='Y']
        y_N = df[input.var_box()][df['Drafted?']=='N']
         
        if len(y_Y)>0 and len(y_N)>0:
        
            fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
            ax1.boxplot(y_Y, vert = True, patch_artist=True, boxprops=dict(facecolor="lightgreen", color="g"))
            ax2.boxplot(y_N, vert = True, patch_artist=True, boxprops=dict(facecolor="pink", color="r"))
            ax1.set_title("Drafted {}s - {}".format(input.pos(),input.var_box()))
            ax1.set_ylabel(input.var_box())
            ax1.yaxis.grid(True)
            ax2.set_title("Undrafted {}s - {}".format(input.pos(),input.var_box()))
            ax2.set_ylabel(input.var_box())
            ax2.yaxis.grid(True)

            return fig 
        
        elif len(y_Y)>0:
        
            fig, (ax1) = plt.subplots(nrows=1, ncols=1)
            ax1.boxplot(y_Y, vert = True, patch_artist=True, boxprops=dict(facecolor="lightgreen", color="g"))
            ax1.set_title("Drafted {}s - {}".format(input.pos(),input.var_box()))
            ax1.set_ylabel(input.var_box())
            ax1.yaxis.grid(True)

            return fig 
        
        elif len(y_N)>0:
        
            fig, (ax2) = plt.subplots(nrows=1, ncols=1)
            ax2.boxplot(y_N, vert = True, patch_artist=True, boxprops=dict(facecolor="pink", color="r"))
            ax2.set_title("Undrafted {}s - {}".format(input.pos(),input.var_box()))
            ax2.set_ylabel(input.var_box())
            ax2.yaxis.grid(True)

            return fig 
        
app = App(app_ui, server, debug=False)
