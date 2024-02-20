#!/usr/bin/python3

###############################################################################
# PATHS AND DICTIONARIES
###############################################################################
import os

path = os.path.dirname(os.path.abspath("__file__"))
from os.path import *
import pandas as pd
import __main__

__main__.pymol_argv = [
    "pymol",
    "-A3",
]  # https://pymolwiki.org/index.php/Command_Line_Options
from os.path import dirname, join
import numpy as np
import sqlalchemy
import re

from bokeh import events
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout, widgetbox, row
from bokeh.embed import components
from bokeh.models import (
    CustomJS,
    Div,
    ColumnDataSource,
    LabelSet,
    HoverTool,
    FactorRange,
    Plot,
    LinearAxis,
    Grid,
    Range1d,
    OpenURL,
    TapTool,
    Circle,
)
from bokeh.models.widgets import (
    Slider,
    Select,
    TextInput,
    Div,
    MultiSelect,
    RadioGroup,
    Dropdown,
    Button,
)
from bokeh.models.glyphs import ImageURL
from bokeh.io import curdoc, show

# data = pd.read_csv(f"dimer_general_simulation.csv")
machine = "http://alf06.uab.es/dimerbow"
engine = sqlalchemy.create_engine(
    f"mysql+mysqlconnector://adrian:D1m3rB0w!@localhost:3306/lmcdb"
)
data = pd.read_sql(
    "select dimerbow.*, uniprot, iuphar_sub from dimerbow, pdb, gpcr_cls where (dimerbow.pdbid = pdb.pdbid) and (pdb.uniprot = gpcr_cls.entry) and (dimerbow.DISPLAY = 'YES') order by dimerbow.DIMER asc;",
    engine,
)
palette = {
    "X": "green",
    "1": "grey",
    "2": "grey",
    "3": "grey",
    "4": "grey",
    "5": "grey",
}
data["dimer_colors"] = [palette[x] for x in data["SIMULATION"]]
data = data.fillna("-")
print(data)
source_1 = ColumnDataSource(
    data=dict(
        ind=[],
        sim=[],
        dimer=[],
        recep=[],
        typ=[],
        reference=[],
        x=[],
        y=[],
        ini=[],
        end=[],
        color=[],
        coords=[],
        uniprot=[],
    )
)

source = ColumnDataSource(
    data=dict(
        ind=[],
        sim=[],
        dimer=[],
        recep=[],
        typ=[],
        x=[],
        y=[],
        ini=[],
        end=[],
        color=[],
        coords=[],
        uniprot=[],
    )
)

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

tooltips_crystal = [
    ("Id", "@ind"),
    ("Dimer", "@dimer"),
    ("Uniprot", "@uniprot"),
    ("References", "@reference"),
    ("Type", "@typ"),
]

tooltips_simulation = [
    ("Id", "@ind"),
    ("Dimer", "@dimer"),
    ("Uniprot", "@uniprot"),
    ("Type", "@typ"),
    ("Start", "@ini"),
    ("End", "@end"),
]

hover_crystal = HoverTool(tooltips=tooltips_crystal, names=["crystal"])
hover_simulation = HoverTool(tooltips=tooltips_simulation, names=["simulations"])


callback = CustomJS(
    args=dict(source=source),
    code="""
                var data = source.data;
                var id = cb_data.source.selected['1d'].indices;
                var dimer = data["dimer"][id];
                var coords = data["coords"][id];
                var sim = data["sim"][id];
                sessionStorage.setItem("sim", sim);
                sessionStorage.setItem("dimer", dimer);
                sessionStorage.setItem("coords", coords);
                parent.frame2_sim.location.reload();
                """,
)

taptool = TapTool(names=["simulations"], callback=callback)

p = figure(
    tools=TOOLS,
    toolbar_location="above",
    plot_width=800,
    plot_height=800,
    title="",
    x_range=[-50, 50],
    y_range=[-50, 50],
)
p.toolbar.logo = "grey"
p.axis.visible = False
p.grid.visible = False
p.grid.grid_line_color = "white"
p.image_url(
    url=[machine + "/static/img/bokeh_reference.png"],
    x=1,
    y=2,
    w=70,
    h=90,
    anchor="center",
)

p.circle(
    x="x",
    y="y",
    size=16,
    source=source_1,
    color="color",
    line_color="black",
    fill_alpha=0.8,
    name="crystal",
)

renderer = p.circle(
    x="x",
    y="y",
    size=16,
    source=source,
    color="color",
    line_color="black",
    fill_alpha=0.8,
    name="simulations",
)

selected_circle = Circle(fill_alpha=1, fill_color="color", line_color="black")
nonselected_circle = Circle(fill_alpha=0.2, fill_color="white", line_color="black")

renderer.selection_glyph = selected_circle
renderer.nonselection_glyph = nonselected_circle

p.add_tools(hover_crystal)
p.add_tools(hover_simulation)
p.add_tools(taptool)

# Lists
l_recep = list(data.RECEPTOR.unique())
l_recep.append("-- Select receptor --")

l_dimer = list(data.DIMER.unique())
l_dimer.append("-- Select dimer --")


# Filterers
dimer = Select(title="Dimer:", value="-- Select dimer --", options=sorted(l_dimer))
refer = TextInput(value="--Press Enter after code insertion--", title="Reference:")
ori_inter = Slider(
    title="Interactions when simulation start", start=0, end=70, value=0, step=1
)
lz_inter = Slider(
    title="Interactions when simulation ends", start=0, end=70, value=0, step=1
)
recep = Select(
    title="Receptor:", value="-- Select receptor --", options=sorted(l_recep)
)
reset = Button(label="Reset", button_type="success")

# Reset
reset.js_on_click(
    CustomJS(
        args=dict(source=source_1),
        code="""
    parent.frame1_sim.location.reload();
""",
    )
)

reset.js_on_click(
    CustomJS(
        args=dict(source=source),
        code="""
    parent.frame1_sim.location.reload();
""",
    )
)

# Dimer change
def update_data(attrname, old, new):
    print(dimer.value)
    recep_val = recep.value
    dimer_val = dimer.value
    selected = data[data.RECEPTOR.str.contains(recep_val) == True]
    selected = data[data.DIMER.str.contains(dimer_val) == True]
    selected = selected[
        (selected.COUNT_1 >= ori_inter.value) & (selected.COUNT_2 >= lz_inter.value)
    ]
    selected_1 = selected[selected.SIMULATION.str.contains("X")]
    selected_2 = selected[~selected.SIMULATION.str.contains("X")]
    source_1.data = dict(
        ind=selected_1["ID"],
        sim=selected_1["SIMULATION"],
        dimer=selected_1["DIMER"],
        reference=selected_1["REFERENCE"],
        typ=selected_1["TYPE"],
        recep=selected_1["RECEPTOR"],
        x=selected_1["X"],
        y=selected_1["Y"],
        ini=selected_1["COUNT_1"],
        end=selected_1["COUNT_2"],
        color=selected_1["dimer_colors"],
        coords=selected_1["COORDS"],
        uniprot=selected_1["uniprot"],
    )
    source.data = dict(
        ind=selected_2["ID"],
        sim=selected_2["SIMULATION"],
        dimer=selected_2["DIMER"],
        typ=selected_2["TYPE"],
        recep=selected_2["RECEPTOR"],
        x=selected_2["X"],
        y=selected_2["Y"],
        ini=selected_2["COUNT_1"],
        end=selected_2["COUNT_2"],
        color=selected_2["dimer_colors"],
        coords=selected_2["COORDS"],
        uniprot=selected_2["uniprot"],
    )
    dimer_change = CustomJS(
        args=dict(p=p, dimer_val=dimer_val),
        code="""
    sessionStorage.setItem("dimer", "blank");
    sessionStorage.setItem("sim", -1);
    parent.frame2_sim.location.reload();
    p.reset.emit();
    """,
    )
    dimer.callback = dimer_change
    try:
        y_start = int(selected_2["X"].min())
        y_end = int(selected_2["X"].max())
        x_start = int(selected_2["Y"].min())
        x_end = int(selected_2["Y"].max())
        coords = [abs(y_start), abs(y_end), abs(x_start), abs(x_end)]
        p.x_range.start = max(coords) * -1 - 5
        p.x_range.end = max(coords) + 5
        p.y_range.start = max(coords) * -1 - 5
        p.y_range.end = max(coords) + 5
    except:
        p.x_range.start = -100
        p.x_range.end = 100
        p.y_range.start = -100
        p.y_range.end = 100


controls = [dimer, ori_inter, lz_inter]
for control in controls:
    control.on_change("value", update_data)


inputs = widgetbox(controls)

curdoc().add_root(row(reset, width=100))
curdoc().add_root(row(inputs, p, width=700))

