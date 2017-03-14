# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:06:09 2017

@author: bonar
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 10:59:50 2017

@author: bonar
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from board_functions import *
import sqlite3 as lite
import datetime
import serial


class MyApp(object):

    def __init__(self):
        #connect to microcontroller
        try:
            ports = listSerialPorts()
            self.board = expander(str(ports[0]), 9600)
            print('connected to board on COM port %s' %(ports[0]))
            print('board id is %s' %(self.board.i_d()))
        except:
            print('no board connected')
        """
        board.clear()
        print(board.errors())
        board.set_connectors(10)
        print(board.errors())
        print(board.scan_results())
        print(board.errors())
        """
        #connect to database/create database if not present
        self.db = lite.connect('sql_db')
        self.c = self.db.cursor()
        try:
            self.c.execute('CREATE TABLE networks(id TEXT unique, timestamp TEXT, user TEXT, no_connectors INTEGER, no_pins INTEGER, network TEXT)')            
        except:
            pass
            

        # Build GUI
        self.builder = Gtk.Builder()
        self.glade_file = 'test1.glade'
        self.builder.add_from_file(self.glade_file)

        # Get objects
        go = self.builder.get_object
        self.window = go('window')
        self.test_button = go('test_button')
        self.learn_button = go('learn_button')
        self.log_button = go('log_button')
        self.reconnect_button = go('reconnect_board')
        
        #create liststore of network names
        #needs to draw network names from database
        self.net_liststore = Gtk.ListStore(int, str)
        self.net_liststore.append([0, 'Select Tape Network ID'])
        self.c.execute('SELECT id FROM networks')
        nets = self.c.fetchall()
        
       
        for i in range(len(nets)):
            self.net_liststore.append([i, nets[i][0]])
        
        
        #create cell renderer and populate combobox with initial list of network names
        self.cell = Gtk.CellRendererText()
        self.net_combo = self.builder.get_object('network_list_combo')
        self.net_combo.set_model(self.net_liststore)
        self.net_combo.pack_start(self.cell, True)
        self.net_combo.add_attribute(self.cell, 'text', 1)
        self.net_combo.set_active(0)
        
        # Connect signals
        self.builder.connect_signals(self)

        # Everything is ready
        self.window.show()
    
    def onDeleteWindow(self, widget):
        self.db.close()
        Gtk.main_quit()
        
    def test(self, test_button):
        print("test")
        self.board.clear()
        print(self.board.scan())
        tree_iter = self.net_combo.get_active_iter()
        model = self.net_combo.get_model()
        row_id, name = model[tree_iter][:2]
        print("Netname = %s" % (name))
        #get results
        #compare with stored net
        #display results in info box
        
        
    def learn(self, learn_button):
        net_ID_entry = self.builder.get_object("net_ID_entry") 
        user_ID_entry = self.builder.get_object("user_ID_entry")
        connectors_entry = self.builder.get_object("connectors_entry")
        pins_entry = self.builder.get_object("pins_entry")
        #get all info about network to save into database
        net_ID = Gtk.Entry.get_text(net_ID_entry)
        user_ID = Gtk.Entry.get_text(user_ID_entry)
        connectors = Gtk.Entry.get_text(connectors_entry)
        pins = Gtk.Entry.get_text(pins_entry)   
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        network = self.board.report_all()
        
        print(net_ID, user_ID, connectors, pins, timestamp, network)
        ###check net_ID not in database already
        self.c.execute('SELECT EXISTS(SELECT 1 FROM networks WHERE id = ?)',(net_ID,))
        
        if self.c.fetchone()[0]==1:
            print('network already found with name  %s'%(net_ID))      
        else:        
        
            #add network
            self.c.execute('INSERT INTO networks(id, timestamp, user, no_connectors, no_pins, network) VALUES(?,?,?,?,?,?)', (net_ID, timestamp, user_ID, connectors, pins, network))
            self.db.commit()
            print('added to database')
            #update liststore and combobox with new network name taken 
            self.net_liststore.append([4, str(net_ID)])
        
        #run program and learn network
        #update database with learned network
        #(option to delete nets in database)
       
    def log(self, log_button):
        tape_ID_entry = self.builder.get_object("tape_ID_entry")
        user_ID_entry = self.builder.get_object("user_ID_entry")
        tree_iter = self.net_combo.get_active_iter()
        model = self.net_combo.get_model()
        row_id, net_ID = model[tree_iter][:2]
        tape_ID = Gtk.Entry.get_text(tape_ID_entry)
        user_ID = Gtk.Entry.get_text(user_ID_entry)
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        scan = self.board.scan() 
        print(scan)       
        #get errors by comparing scan with net scan in database
        self.c.execute('SELECT network FROM networks WHERE id=?', (net_ID,))        
        db_net = self.c.fetchone()
        if scan != db_net:
            print('errors found')
            errors = 'some'
        else:
            print('no errors found')
            errors = 'none'
        #create a table for tape ID in database if there isnt one already and insert dated test results as row in database
        self.c.execute("CREATE TABLE IF NOT EXISTS [" +str(tape_ID)+ "](timestamp TEXT, user TEXT, network TEXT, errors TEXT, scan TEXT)")
        self.db.commit()
        self.c.execute('INSERT INTO ['+str(tape_ID)+'](timestamp, user, network, errors, scan) VALUES(?,?,?,?,?)',(timestamp, user_ID, net_ID, errors, scan))
        print(tape_ID)
        
        
    def reconnect(self, reconnect_button):
        ports = listSerialPorts()
        print(ports)
        try:
            self.board.serial.close()
        except:
            pass
        try:
            self.board = expander(str(ports[0]), 9600)
            print('connected to board on COM port %s' %(ports[0]))
            print('board id is %s' %(self.board.i_d()))
            print('if no board ID is displayed try reconnect')
            
        except:
            print('connection failed on COM port %s, try plug board in again' % (ports[0]))
if __name__ == '__main__':
    try:
        
        gui = MyApp()
        Gtk.main()
    except KeyboardInterrupt:
        pass


