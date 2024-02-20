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

def home(request):
    context = {}
    context['site_title'] = settings.SITE_TITLE

    return render(request, 'home/home.html', context)

def manual(request):
    context = {}
    context['site_title'] = settings.SITE_TITLE

    return render(request, 'home/manual.html', context)

def contact(request):
    context = {}
    context['site_title'] = settings.SITE_TITLE

    return render(request, 'home/contact.html', context)

# @app.route('/about.html')
# def about():
#     return render_template('about.html')

# @app.route('/structure_crystal.html')
# def structure_crystal():
#     return render_template("structure_crystal.html")

# @app.route('/structure_simulation.html')
# def structure_simulation():
#     return render_template("structure_simulation.html")

# @app.route('/graphic_crystal.html')
# def graphic_crystal():
#     script_1=server_document("http://alf06.uab.es:5006/dimerbow_crystal")
#     return render_template("graphic_crystal.html", dimerbow_crystal=script_1)

# @app.route('/graphic_simulation.html')
# def graphic_simulation():
#     script_2=server_document("http://alf06.uab.es:5006/dimerbow_simulation")
#     return render_template("graphic_simulation.html", dimerbow_simulation=script_2)