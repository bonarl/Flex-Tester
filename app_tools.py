# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:29:01 2017

@author: bonar
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import time


def defaults(app, net_select):
    #funcion for use in app to check if data such as tape id etc have been entered to avoid 
    #saving lots of data with default names into database
    tape_ID_entry = app.builder.get_object("tape_ID_entry")
    net_ID_entry = app.builder.get_object("net_ID_entry") 
    user_ID_entry = app.builder.get_object("user_ID_entry")
    connectors_entry = app.builder.get_object("connectors_entry")
    pins_entry = app.builder.get_object("pins_entry")
    net_select_ID = net_select
    
    #get all info about network to save into database
    tape_ID = Gtk.Entry.get_text(tape_ID_entry)
    net_ID = Gtk.Entry.get_text(net_ID_entry)
    user_ID = Gtk.Entry.get_text(user_ID_entry)
    connectors = Gtk.Entry.get_text(connectors_entry)
    pins = Gtk.Entry.get_text(pins_entry)  
    log_errors = []
    learn_errors = []
    learn_ok = 1
    log_ok = 1
    if user_ID == 'Enter Your Name' or net_ID == 'Enter New Network ID' or connectors == 'Connectors' or pins == 'Pins' or tape_ID == 'Enter Flex Tape ID' or net_select_ID == 'Select Tape Network ID':
        if user_ID == 'Enter Your Name':
            log_errors.append('Please enter your name to save results ')
            learn_errors.append('Please enter your name to save results ')
            learn_ok = 0
            log_ok = 0
        if net_ID == 'Enter New Network ID':
            learn_errors.append('Please enter a name for new network to save as ')
            learn_ok = 0
        if connectors == 'Connectors':
            learn_errors.append('Please enter number of connectors ')
            learn_ok = 0
        if pins == 'Pins':
            learn_errors.append('Please enter number of pins per connector ')
            learn_ok = 0
        if tape_ID == 'Enter Flex Tape ID':
            log_errors.append('Please enter flex tape id to save test results ')
            log_ok = 0
        if net_select_ID == 'Select Tape Network ID':
            log_errors.append('Please select a network from database to test against, or add new network to database ')
            log_ok = 0
        return(learn_errors, log_errors, learn_ok, log_ok)
    else: 
        return(1, 1, 1, 1)
    
def display(app, *args):
    for arg in args:
        app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(),  "\n" + str(arg))
    app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(), "\n")
        
def displayl(app, *args):
    for arg in args:
        for i in range(len(arg)):
            app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(),  "\n" + str(arg[i]))
    app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(), "\n")

                
      

    

