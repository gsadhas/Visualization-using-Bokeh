import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import Label
from bokeh.models import WheelZoomTool

global COLORS_DEF

COLORS_DEF = ['#5D8AA8', '#E32636', '#FFBF00', '#A4C639', '#FBCEB1', '#4B5320', '#3B444B', '#E9D66B',
              '#B2BEB5', '#6D351A', '#007FFF', '#F4C2C2', '#98777B', '#BF94E4', '#964B00', '#98817B', '#FBCCE7',
              '#8C92AC', '#FF3800', '#FBEC5D', '#9400D3', '#614051', '#AEC6CF', '#CB99C9', '#808000', '#85BB65',
              '#E1A95F', '#50C878', '#FFDF00', '#B2EC5D', '#138808', '#FF5C5C', '#E3A857', '#3EB489', '#D2691E',
              '#E4D00A', '#002E63', '#FF7F50', '#B31B1B']


def generate_legend(dpg):
    """
    Function to create custom legend for the given values
    :param dpg: List of legend values
    :return: bokeh plot components
    """
    plotWidth = (len(dpg) + 1) * 60

    p = figure(plot_height=120, plot_width=plotWidth, tools="save,pan,reset")
    p.toolbar_location = 'above'
    p.axis.visible = None
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.outline_line_alpha = 0
    lab = Label(x=0.25, y=1.5, text="Down Group", text_font_size="10pt")
    p.add_layout(lab)

    for i, dp in enumerate(dpg):
        p.circle(x=0.5 + i, y=1, size=10, fill_color=COLORS_DEF[i], line_color=None)
        lab = Label(x=0.5 + i + 0.2, y=0.75, text=str(dp), text_font_size="10pt")
        p.add_layout(lab)
    script, div = components(p, CDN)
    return script, div


def generate_plot(df, type):
    """
    Generate bokeh plot for the respective view
    :param df: Pandas dataframe
    :param type: plot type if it is for single view or multi view
    :return: bokeh plot components
    """
    x_title = 'Value'
    y_title = 'Rate'

    # Creating uval as string to render
    dfT = pd.DataFrame()
    dfT['suval'] = df['uval'].apply(lambda x: str(x))
    dfT['str'] = df['tr'].apply(lambda x: str(x))

    dfT['myir'] = df['yir'].apply(lambda x: x + 5 if x != 0 else 5)
    df = pd.concat([df, dfT], axis=1)

    hover = HoverTool(
        point_policy=None,
        attachment='vertical',
        tooltips="""
        <div style="position:relative;border-bottom:1px solid #C0C0C0;">
        <span style="font-size:12px; font-weight:bold;"> Value: </span>
        <span style="font-size:12px;">@suval</span> <br/>
        <span style="font-size:12px; font-weight:bold;">Rate: </span><span style="font-size:12px;">@str</span><br/>
        <span style="font-size:12px; font-weight:bold;">Down Group:</span><span style="font-size:12px;">@dpg</span><br/>
        <span style="font-size:12px; font-weight:bold;">Int rate:</span><span style="font-size:12px;">@yir</span><br/>
        </div>
        """)

    if type == 'single':
        height = 500
        width = 600
    else:
        height = 300
        width = 400

    p = figure(plot_height=height, plot_width=width,
               tools=[hover, "reset,box_select,pan,save,redo,undo,wheel_zoom,tap"])
    p.toolbar.active_scroll = p.select(type=WheelZoomTool)[0]
    p.toolbar.active_tap = None

    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if type == 'single':
        dpg = df['dpg'].unique()
        for i, dp in enumerate(dpg):
            dfP = df[df['dpg'] == dp]
            data_dict = {
                'suval': dfP['suval'],
                'str': dfP['str'],
                'yir': dfP['yir'],
                'dpg': dfP['dpg']
            }
            source = ColumnDataSource(data=data_dict)
            p.circle(x=dfP['uval'], y=dfP['tr'], radius=dfP['myir'], source=source, fill_color=None,
                     line_color=COLORS_DEF[i],
                     alpha=0.6, hover_alpha=0.2, line_width=2, legend='DPG: ' + str(dp))
    else:
        dpg = df['dpg'].unique()
        for i, dp in enumerate(dpg):
            dfP = df[df['dpg'] == dp]
            data_dict = {
                'suval': dfP['suval'],
                'str': dfP['str'],
                'yir': dfP['yir'],
                'dpg': dfP['dpg']
            }
            source = ColumnDataSource(data=data_dict)
            p.circle(x=dfP['uval'], y=dfP['tr'], radius=dfP['myir'], source=source, fill_color=None,
                     line_color=COLORS_DEF[i],
                     alpha=0.6, hover_alpha=0.2, line_width=2)

    script, div = components(p, CDN)

    return div, script
