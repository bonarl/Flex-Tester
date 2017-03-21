# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:29:01 2017

@author: bonar
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def defaults(app, net_select):
    #funcion for use in app to check if data such as tape id etc have been entered to avoid 
    #saving lots of data with default names into database
    tape_ID_entry = app.builder.get_object("tape_ID_entry")
    net_ID_entry = app.builder.get_object("net_ID_entry") 
    user_ID_entry = app.builder.get_object("user_ID_entry")
    connectors_entry = app.builder.get_object("connectors_entry")
    pins_entry = app.builder.get_object("pins_entry")
    net_select_ID = net_select   
    #get all info about network to check against default entries
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
    #check which entries are defaults, return a list of 1s or 0s corresponding to certain functions and wether they can run or not
    #main program can then implement defaults() and use this function for different operations by viewing different return indices
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
    #displays text in the textview preceded by a newline character
    for arg in args:
        app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(),  "\n" + str(arg))
       
def displayl(app, *args):
    #displays a list (or list of lists) in textview, each item in list displayed on a newline
    for arg in args:
        for i in range(len(arg)):
            app.text_view.get_buffer().insert(app.text_view.get_buffer().get_end_iter(),  "\n" + str(arg[i]))
              
def check(scan, saved):
    #compares two network scans (lists of PORT x PIN y -> PORT etc...) in format retuned by microcontroller
    #returns list of differences between these scans in human readable form
    scan_ints = []
    saved_ints = []
    errors = []
    scan_ports = []
    save_ports = []
    #loop over scan and saved list and create new list of integers only, first 3 numbers are 
    #[SENDERPORT, SENDERPIN,        RECEIVERPORT,...] 
    #followed by list of receiver port pins where connections are
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
    #compare all lists and append appropriate errors forany differences found
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