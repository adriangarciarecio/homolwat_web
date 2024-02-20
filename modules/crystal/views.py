#/usr/bin/env python3

import os
from django.shortcuts import render
from django.conf import settings

from bokeh.embed import server_session, server_document
from bokeh.client import pull_session

#################################################################
#
# This is my fantastic Bioinformatics Web Application
#
#################################################################
# sudoPass = 'compmod5'
# command = 'bokeh serve dimerbow/dimerbow_crystal.py dimerbow/dimerbow_simulation.py --allow-websocket-origin=alf06.uab.es --port 5006 --address alf06.uab.es &'
# os.system('echo %s | sudo -S %s' % (sudoPass, command))

def crystal(request):
    context = {}
    context['site_title'] = settings.SITE_TITLE

    return render(request, 'home/home.html', context)

def structure_crystal(request):
    context = {}

    return render(request, 'crystal/structure_crystal.html', context)

def graphic_crystal(request):
    context = {}

    context['dimerbow_crystal'] = server_document("./dimerbow_crystal")
    return render(request, 'crystal/graphic_crystal.html', context)

# @app.route('/structure_simulation.html')
# def structure_simulation():
#     return render_template("structure_simulation.html")

# @app.route('/graphic_crystal.html')

# @app.route('/graphic_simulation.html')
# def graphic_simulation():
#     script_2=server_document("http://alf06.uab.es:5006/dimerbow_simulation")
#     return render_template("graphic_simulation.html", dimerbow_simulation=script_2)