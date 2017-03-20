# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:29:01 2017

@author: bonar
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import time
import re


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
    test_ok = 1
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
            test_ok = 0
        if pins == 'Pins':
            learn_errors.append('Please enter number of pins per connector ')
            learn_ok = 0
            test_ok =0
        if tape_ID == 'Enter Flex Tape ID':
            log_errors.append('Please enter flex tape id to save test results ')
            log_ok = 0
        if net_select_ID == 'Select Tape Network ID':
            log_errors.append('Please select a network from database to test against, or add new network to database ')
            log_ok = 0
        return(learn_errors, log_errors, learn_ok, log_ok, test_ok)
    else: 
        return(1, 1, 1, 1)
    
def display(app, *args):
    for arg in args:
        app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(),  "\n" + str(arg))

        
def displayl(app, *args):
    for arg in args:
        for i in range(len(arg)):
            app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(),  "\n" + str(arg[i]))

scan = ['', '', 'PORT 0 PIN 1 -> PORT 0 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 1 PIN 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 3 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 5 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 7 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 9 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 11 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 13 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 15 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 17 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 19 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 21 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 23 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 25 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 27 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 29 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 31 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 33 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 35 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 37 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 39 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 41 PIN 1 2 3 4 5 6 7 8', 'PORT 1 PIN 1 -> PORT 43 PIN 1 2 3 4 5 6 7 8', 'PORT 2 PIN 1 -> PORT 2 PIN 1 2 3 4 5 6 7 8', 'PORT 4 PIN 1 -> PORT 4 PIN 1 2 3 4 5 6 7 8', 'PORT 6 PIN 1 -> PORT 6 PIN 1 2 3 4 5 6 7 8', 'PORT 8 PIN 1 -> PORT 8 PIN 1 2 3 4 5 6 7 8', 'PORT 10 PIN 1 -> PORT 10 PIN 1 2 3 4 5 6 7 8', 'PORT 12 PIN 1 -> PORT 12 PIN 1 2 3 4 5 6 7 8', 'PORT 14 PIN 1 -> PORT 14 PIN 1 2 3 4 5 6 7 8', 'PORT 16 PIN 1 -> PORT 16 PIN 1 2 3 4 5 6 7 8', 'PORT 18 PIN 1 -> PORT 18 PIN 1 2 3 4 5 6 7 8', 'PORT 20 PIN 1 -> PORT 20 PIN 1 2 3 4 5 6 7 8', 'PORT 22 PIN 1 -> PORT 22 PIN 1 2 3 4 5 6 7 8', 'PORT 24 PIN 1 -> PORT 24 PIN 1 2 3 4 5 6 7 8', 'PORT 26 PIN 1 -> PORT 26 PIN 1 2 3 4 5 6 7 8', 'PORT 28 PIN 1 -> PORT 28 PIN 1 2 3 4 5 6 7 8', 'PORT 30 PIN 1 -> PORT 30 PIN 1 2 3 4 5 6 7 8', 'PORT 32 PIN 1 -> PORT 32 PIN 1 2 3 4 5 6 7 8', 'PORT 34 PIN 1 -> PORT 34 PIN 1 2 3 4 5 6 7 8', 'PORT 36 PIN 1 -> PORT 36 PIN 1 2 3 4 5 6 7 8', 'PORT 38 PIN 1 -> PORT 38 PIN 1 2 3 4 5 6 7 8', 'PORT 40 PIN 1 -> PORT 40 PIN 1 2 3 4 5 6 7 8', 'PORT 42 PIN 1 -> PORT 42 PIN 1 2 3 4 5 6 7 8', 'PORT 44 PIN 1 -> PORT 44 PIN 1 2 3 4 5 6 7 8']

saved = ['', '', 'PORT 0 PIN 1 -> PORT 0 PIN 2 3 4 5', 'PORT 0 PIN 1 -> PORT 4 PIN 4 5 6 7 8', 'PORT 0 PIN 1 -> PORT 26 PIN 2 3 4 5 6', 'PORT 0 PIN 1 -> PORT 28 PIN 3 4 5 6 7', 'PORT 0 PIN 6 -> PORT 5 PIN 6', 'PORT 0 PIN 6 -> PORT 10 PIN 6', 'PORT 0 PIN 6 -> PORT 15 PIN 6', 'PORT 0 PIN 6 -> PORT 20 PIN 6', 'PORT 0 PIN 6 -> PORT 25 PIN 6', 'PORT 0 PIN 6 -> PORT 30 PIN 3', 'PORT 0 PIN 6 -> PORT 37 PIN 1', 'PORT 0 PIN 6 -> PORT 42 PIN 3', 'PORT 0 PIN 7 -> PORT 5 PIN 7', 'PORT 0 PIN 7 -> PORT 10 PIN 7', 'PORT 0 PIN 7 -> PORT 15 PIN 7', 'PORT 0 PIN 7 -> PORT 20 PIN 7', 'PORT 0 PIN 7 -> PORT 25 PIN 7', 'PORT 0 PIN 7 -> PORT 30 PIN 4', 'PORT 0 PIN 7 -> PORT 37 PIN 2', 'PORT 0 PIN 7 -> PORT 42 PIN 4', 'PORT 0 PIN 8 -> PORT 39 PIN 1', 'PORT 1 PIN 1 -> PORT 39 PIN 2', 'PORT 1 PIN 2 -> PORT 1 PIN 3 4 5 6', 'PORT 1 PIN 2 -> PORT 3 PIN 3 4 5 6 7', 'PORT 1 PIN 2 -> PORT 5 PIN 1 2 3 4 5', 'PORT 1 PIN 2 -> PORT 9 PIN 4 5 6 7 8', 'PORT 1 PIN 7 -> PORT 3 PIN 2', 'PORT 1 PIN 7 -> PORT 6 PIN 7', 'PORT 1 PIN 7 -> PORT 8 PIN 2', 'PORT 1 PIN 7 -> PORT 11 PIN 7', 'PORT 1 PIN 7 -> PORT 13 PIN 2', 'PORT 1 PIN 7 -> PORT 16 PIN 7', 'PORT 1 PIN 7 -> PORT 18 PIN 2', 'PORT 1 PIN 7 -> PORT 21 PIN 7', 'PORT 1 PIN 7 -> PORT 23 PIN 2', 'PORT 1 PIN 7 -> PORT 26 PIN 7', 'PORT 1 PIN 7 -> PORT 28 PIN 2', 'PORT 1 PIN 7 -> PORT 31 PIN 4', 'PORT 1 PIN 7 -> PORT 33 PIN 5', 'PORT 1 PIN 8 -> PORT 3 PIN 1', 'PORT 1 PIN 8 -> PORT 6 PIN 8', 'PORT 1 PIN 8 -> PORT 8 PIN 1', 'PORT 1 PIN 8 -> PORT 11 PIN 8', 'PORT 1 PIN 8 -> PORT 13 PIN 1', 'PORT 1 PIN 8 -> PORT 16 PIN 8', 'PORT 1 PIN 8 -> PORT 18 PIN 1', 'PORT 1 PIN 8 -> PORT 21 PIN 8', 'PORT 1 PIN 8 -> PORT 23 PIN 1', 'PORT 1 PIN 8 -> PORT 26 PIN 8', 'PORT 1 PIN 8 -> PORT 28 PIN 1', 'PORT 1 PIN 8 -> PORT 31 PIN 5', 'PORT 1 PIN 8 -> PORT 33 PIN 4', 'PORT 2 PIN 4 -> PORT 2 PIN 5', 'PORT 2 PIN 4 -> PORT 7 PIN 4 5', 'PORT 2 PIN 4 -> PORT 12 PIN 4 5', 'PORT 2 PIN 4 -> PORT 17 PIN 4 5', 'PORT 2 PIN 4 -> PORT 22 PIN 4 5', 'PORT 2 PIN 4 -> PORT 27 PIN 4 5', 'PORT 2 PIN 4 -> PORT 32 PIN 4 5', 'PORT 3 PIN 8 -> PORT 38 PIN 8', 'PORT 4 PIN 1 -> PORT 38 PIN 7', 'PORT 4 PIN 2 -> PORT 9 PIN 2', 'PORT 4 PIN 2 -> PORT 14 PIN 2', 'PORT 4 PIN 2 -> PORT 19 PIN 2', 'PORT 4 PIN 2 -> PORT 24 PIN 2', 'PORT 4 PIN 2 -> PORT 29 PIN 2', 'PORT 4 PIN 2 -> PORT 30 PIN 2', 'PORT 4 PIN 2 -> PORT 35 PIN 4', 'PORT 4 PIN 2 -> PORT 42 PIN 2', 'PORT 4 PIN 3 -> PORT 9 PIN 3', 'PORT 4 PIN 3 -> PORT 14 PIN 3', 'PORT 4 PIN 3 -> PORT 19 PIN 3', 'PORT 4 PIN 3 -> PORT 24 PIN 3', 'PORT 4 PIN 3 -> PORT 29 PIN 3', 'PORT 4 PIN 3 -> PORT 30 PIN 1', 'PORT 4 PIN 3 -> PORT 35 PIN 3', 'PORT 4 PIN 3 -> PORT 42 PIN 1', 'PORT 5 PIN 8 -> PORT 39 PIN 5', 'PORT 6 PIN 1 -> PORT 39 PIN 6', 'PORT 6 PIN 2 -> PORT 6 PIN 3 4 5 6', 'PORT 6 PIN 2 -> PORT 8 PIN 3 4 5 6 7', 'PORT 6 PIN 2 -> PORT 10 PIN 1 2 3 4 5', 'PORT 6 PIN 2 -> PORT 14 PIN 4 5 6 7 8', 'PORT 8 PIN 8 -> PORT 39 PIN 4', 'PORT 9 PIN 1 -> PORT 39 PIN 3', 'PORT 10 PIN 8 -> PORT 35 PIN 1', 'PORT 11 PIN 1 -> PORT 35 PIN 2', 'PORT 11 PIN 2 -> PORT 11 PIN 3 4 5 6', 'PORT 11 PIN 2 -> PORT 13 PIN 3 4 5 6 7', 'PORT 11 PIN 2 -> PORT 15 PIN 1 2 3 4 5', 'PORT 11 PIN 2 -> PORT 19 PIN 4 5 6 7 8', 'PORT 13 PIN 8 -> PORT 39 PIN 8', 'PORT 14 PIN 1 -> PORT 39 PIN 7', 'PORT 15 PIN 8 -> PORT 37 PIN 5', 'PORT 16 PIN 1 -> PORT 37 PIN 6', 'PORT 16 PIN 2 -> PORT 16 PIN 3 4 5 6', 'PORT 16 PIN 2 -> PORT 18 PIN 3 4 5 6 7', 'PORT 16 PIN 2 -> PORT 40 PIN 1 2 3 4 5', 'PORT 16 PIN 2 -> PORT 44 PIN 4 5 6 7 8', 'PORT 18 PIN 8 -> PORT 37 PIN 4', 'PORT 19 PIN 1 -> PORT 37 PIN 3', 'PORT 20 PIN 1 -> PORT 20 PIN 2 3 4 5', 'PORT 20 PIN 1 -> PORT 24 PIN 4 5 6 7 8', 'PORT 20 PIN 1 -> PORT 40 PIN 6 7 8', 'PORT 20 PIN 1 -> PORT 41 PIN 1 2', 'PORT 20 PIN 1 -> PORT 43 PIN 7 8', 'PORT 20 PIN 1 -> PORT 44 PIN 1 2 3', 'PORT 20 PIN 8 -> PORT 38 PIN 1', 'PORT 21 PIN 1 -> PORT 38 PIN 2', 'PORT 21 PIN 2 -> PORT 21 PIN 3 4 5 6', 'PORT 21 PIN 2 -> PORT 23 PIN 3 4 5 6 7', 'PORT 21 PIN 2 -> PORT 25 PIN 1 2 3 4 5', 'PORT 21 PIN 2 -> PORT 29 PIN 4 5 6 7 8', 'PORT 23 PIN 8 -> PORT 37 PIN 8', 'PORT 24 PIN 1 -> PORT 37 PIN 7', 'PORT 25 PIN 8 -> PORT 38 PIN 5', 'PORT 26 PIN 1 -> PORT 38 PIN 6', 'PORT 28 PIN 8 -> PORT 38 PIN 4', 'PORT 29 PIN 1 -> PORT 38 PIN 3', 'PORT 34 PIN 7 -> PORT 34 PIN 8', 'PORT 34 PIN 7 -> PORT 35 PIN 5 6 7 8', 'PORT 34 PIN 7 -> PORT 36 PIN 1 2 3 4 5 6 7 8', 'PORT 34 PIN 7 -> PORT 42 PIN 5 6']

                
def check(scan, saved):
    scan_ints = []
    saved_ints = []
    errors = []
    scan_ports = []
    save_ports = []
    for i in range(len(scan)):
        scan_list = []
        for entry in scan[i].split():
            try:
                scan_list.append(int(entry))
            except:
                pass 
        if len(scan_list) > 2:
            scan_ints.append(scan_list)
    for i in range(len(saved)):
        save_list = []
        for entry in saved[i].split():
            try:
                save_list.append(int(entry))
            except: 
                pass
        if len(save_list) > 2:
            saved_ints.append(save_list)  
    
    for i in range(len(scan_ints)):
        for j in range(len(saved_ints)):
            scan_send_port = scan_ints[i][0]
            scan_send_pin = scan_ints[i][1]
            save_send_port = saved_ints[j][0]
            save_send_pin = saved_ints[j][1]
            scan_list = scan_ints[i]
            save_list = saved_ints[j]
            scan_ports.append(scan_send_port)
            save_ports.append(save_send_port)
            if scan_send_port == save_send_port and scan_send_pin == save_send_pin and scan_list != save_list:
                scan_receive_port = scan_list[2]
                
                save_receive_port = save_list[2]
                scan_list1 = []
                save_list1 = []
                for x in range(3,len(save_list)):
                    save_list1.append(save_list[x])
                for y in range(3,len(scan_list)):
                    scan_list1.append(scan_list[y])
                for pin in save_list1:
                    if pin not in scan_list1:
                        errors.append('PORT %s PIN %s does not connect to PORT %s PIN %s' % (scan_send_port, scan_send_pin, scan_receive_port, pin))
                for pin in scan_list1:
                    if pin not in save_list1:
                        errors.append('PORT %s PIN %s connects to PORT %s PIN %s' % (scan_send_port, scan_send_pin, scan_receive_port, pin))
    save_set = set(save_ports)
    scan_set = set(scan_ports)
    for port in save_set:
        if port not in scan_set:
            errors.append('No connections found for port %s' %(port))
    for port in scan_set:
        if port not in save_set:
            errors.append('Connections found for port %s' %(port))
            
    return(errors)
                
                    
                

                                
                
                
                

                
                
                
    
print(check(scan, saved))

        

    

