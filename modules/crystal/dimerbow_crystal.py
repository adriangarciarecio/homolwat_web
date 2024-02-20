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
    Button,
)
from bokeh.models.glyphs import ImageURL
from bokeh.io import curdoc, show

# data = pd.read_csv(f'dimer_general_crystal.csv')
machine = 'http://alf06.uab.es/dimerbow'
engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://adrian:D1m3rB0w!@localhost:3306/lmcdb")
data = pd.read_sql(
    "select dimerbow.*, uniprot, iuphar_sub from dimerbow, pdb, gpcr_cls where (dimerbow.pdbid = pdb.pdbid) and (pdb.uniprot = gpcr_cls.entry) and (dimerbow.SIMULATION = 'X') and (dimerbow.DISPLAY = 'YES') order by dimerbow.DIMER asc;",
    engine,
)
palette = {"HH": "blue", "HT": "orange"}
alias = {"HH": "Head-to-head", "HT": "Head-to-tail"}
data["TYPE_b"] = [alias[x] for x in data["TYPE"]]
data["dimer_colors"] = [palette[x] for x in data["TYPE"]]
data = data.fillna("-")

source = ColumnDataSource(
    data=dict(
        ind=data.ID,
        dimer=data.DIMER,
        recep=data.RECEPTOR,
        reference=data.REFERENCE,
        x=data.X,
        y=data.Y,
        fus=data.FUSION_PROTEIN,
        typ=data.TYPE_b,
        ori=data.COUNT_1,
        lz=data.COUNT_2,
        coords=data.COORDS,
        uniprot=data.uniprot,
        iuphar=data.iuphar_sub,
        color=data.dimer_colors,
        pdbid=data.pdbid,
    )
)

TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save,tap"

tooltips = [
    ("Dimer", "@dimer"),
    ("Type", "@typ"),
    ("Uniprot", "@uniprot"),
    ("References", "@reference"),
    ("Fusion protein", "@fus"),
    ("Interactions PDB", "@ori"),
    ("Interactions with fusion protein", "@lz"),
]

p = figure(
    tools=TOOLS,
    toolbar_location="above",
    plot_width=800,
    plot_height=800,
    title="%d dimers selected" % len(data),
    tooltips=tooltips,
    x_range=[-60, 60],
    y_range=[-60, 60],
)
p.toolbar.logo = "grey"
p.axis.visible = False
p.grid.visible = False
p.grid.grid_line_color = "white"
p.image_url(
    url=[machine + "/static/img/bokeh_reference.png"],
    x=2,
    y=2,
    w=70,
    h=90,
    anchor="center",
)

renderer = p.circle(
    x="x",
    y="y",
    size=16,
    source=source,
    legend="typ",
    color="color",
    line_color="black",
    fill_alpha=0.8,
)

selected_circle = Circle(fill_alpha=1, fill_color="color", line_color="black")
nonselected_circle = Circle(fill_alpha=0.2, fill_color="color", line_color="black")

renderer.selection_glyph = selected_circle
renderer.nonselection_glyph = nonselected_circle

labels = LabelSet(
    x="x",
    y="y",
    text="pdbid",
    y_offset=8,
    text_font_size="12pt",
    text_color="black",
    source=source,
    text_align="center",
)
p.add_layout(labels)

taptool = p.select(type=TapTool)
taptool.callback = CustomJS(
    args=dict(source=source),
    code="""
        var data = source.data;
        var d = cb_data.source.selected['1d'].indices;
        var dimer = data["dimer"][d];
        var coords = data["coords"][d];
        sessionStorage.setItem("dimer", dimer);
        sessionStorage.setItem("coords", coords);
        parent.frame2_cry.location.reload();
        """,
    )

# Lists
l_recep = list(data.RECEPTOR.unique())
l_recep.append("All")

l_fus = list(data.FUSION_PROTEIN.unique())
for n, i in enumerate(l_fus):
    if i == None:
        l_fus[n] = "-"
l_fus.append("All")

l_iuphar = list(data.iuphar_sub.unique())
l_iuphar.append("All")

# Filterers
type_dimer = Select(
    title="Type:", value="All", options=["All", "Head-to-head", "Head-to-tail"]
)
refer = TextInput(value="--Press Enter after code insertion--", title="Reference:")
recep = MultiSelect(title="Receptor:", value=["All"], options=sorted(l_recep))
iuphar_clas = MultiSelect(
    title="IUPHAR clasification:", value=["All"], options=sorted(l_iuphar)
)
fus_prot = MultiSelect(title="Fusion Protein:", value=["All"], options=sorted(l_fus))
ori_inter = Slider(title="Interactions PDB", start=0, end=70, value=0, step=1)
lz_inter = Slider(
    title="Interactions with fusion protein", start=0, end=70, value=0, step=1
)
reset = Button(label="Reset", button_type="success")

# Reset
reset.js_on_click(
    CustomJS(
        args=dict(source=source),
        code="""
    parent.frame1_cry.location.reload();
""",
    )
)

# Update
def update_data(attrname, old, new):
    type_val = type_dimer.value
    recep_val = recep.value
    refer_val = refer.value
    iuphar_val = iuphar_clas.value
    fus_prot_val = fus_prot.value
    selected_count = data[
        (data.COUNT_1 >= ori_inter.value) & (data.COUNT_2 >= lz_inter.value)
    ]
    selected = selected_count[
        selected_count.REFERENCE.str.contains(refer_val.upper()) == True
    ]
    if selected.empty == True:
        selected = selected_count[
            selected_count.DIMER.str.contains(refer_val.upper()) == True
        ]
        if selected.empty == True:
            CustomJS(
                args=dict(source=source),
                code="""
                    alert ('Check the PDB code!');
                """,
            )
    if refer_val == "--Press Enter after code insertion--":
        selected = selected_count
    if type_val != "All":
        selected = selected[selected.TYPE_b.str.contains(type_val) == True]
    if recep_val != ["All"]:
        selected = selected[selected["RECEPTOR"].isin(recep_val)]
    if iuphar_val != ["All"]:
        selected = selected[selected["iuphar_sub"].isin(iuphar_val)]
    if fus_prot_val != ["All"]:
        selected = selected[selected["FUSION_PROTEIN"].isin(fus_prot_val)]

    p.title.text = "%d dimers selected" % len(selected.ID)
    source.data = dict(
        ind=selected["ID"],
        dimer=selected["DIMER"],
        receptor=selected["RECEPTOR"],
        reference=selected["REFERENCE"],
        x=selected["X"],
        y=selected["Y"],
        fus=selected["FUSION_PROTEIN"],
        typ=selected["TYPE_b"],
        ori=selected["COUNT_1"],
        lz=selected["COUNT_2"],
        coords=selected["COORDS"],
        uniprot=selected["uniprot"],
        iuphar=selected["iuphar_sub"],
        color=selected["dimer_colors"],
        pdbid=selected["pdbid"],
    )


controls = [type_dimer, refer, recep, iuphar_clas, fus_prot, ori_inter, lz_inter]
for control in controls:
    control.on_change("value", update_data)
inputs = widgetbox(controls)

curdoc().add_root(row(reset, width=100))
curdoc().add_root(row(inputs, p, width=700))

