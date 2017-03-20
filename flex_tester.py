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
from app_tools import *
import sqlite3 as lite
import datetime
import pickle




class MyApp(object):

    def __init__(self):
        
        #connect to database/create database if not present
        self.db = lite.connect('sql_db')
        self.c = self.db.cursor()
        try:
            self.c.execute('CREATE TABLE networks(id TEXT unique, timestamp TEXT, user TEXT, no_connectors INTEGER, no_pins INTEGER, network BLOB)')            
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
        self.open_button = go('open_button')
        self.open_net_button = go('open_net_button')
        self.text_view = go('display')
        self.scrolled_window = go('scroll')
        self.text_view.connect("size-allocate", self.autoscroll)
        
        
        
        #create liststore of network names
        #needs to draw network names from database
        self.net_liststore = Gtk.ListStore(int, str)
        self.net_liststore.append([0, 'Select Tape Network ID'])
        self.c.execute('SELECT id FROM networks')
        nets = self.c.fetchall()
        
        self.net_liststore1 = Gtk.ListStore(int, str)
        self.net_liststore1.append([0, 'Select Tape Network ID to view'])
        self.c.execute('SELECT id FROM networks')
        nets = self.c.fetchall()
        
        for i in range(len(nets)):
            self.net_liststore.append([i, nets[i][0]])
            self.net_liststore1.append([i, nets[i][0]])
        
        
        #create cell renderer and populate combobox with initial list of network names
        self.cell = Gtk.CellRendererText()
        self.net_combo = self.builder.get_object('network_list_combo')
        self.net_combo.set_model(self.net_liststore)
        self.net_combo.pack_start(self.cell, True)
        self.net_combo.add_attribute(self.cell, 'text', 1)
        self.net_combo.set_active(0)
        
        self.cell1 = Gtk.CellRendererText()
        self.net_combo1 = self.builder.get_object('network_list_combo1')
        self.net_combo1.set_model(self.net_liststore1)
        self.net_combo1.pack_start(self.cell1, True)
        self.net_combo1.add_attribute(self.cell1, 'text', 1)
        self.net_combo1.set_active(0)
        # Connect signals
        self.builder.connect_signals(self)

        # open gui
        self.window.show()
    

        #connect to microcontroller if present (defaults to last connected com port)
        try:
            ports = listSerialPorts()
            if len(ports) > 1:
                self.board = expander(str(ports[0]), 9600)           
                display(self,'connected to board on COM port %s' %(ports[0]))
                display(self,'board id is %s' %(self.board.i_d()))

        except:
            display(self,'no board connected')
 
    def onDeleteWindow(self, widget):
        self.db.commit()
        self.db.close()
        Gtk.main_quit()
        
    def autoscroll(self, *args):
        #scrolling method for text display window
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        
    def test(self, test_button):
        #run a quick test of tape and display scan (need to specify number of connectors, 
        #optional to compare with network to view errors)
        display(self, '\n')
        connectors_entry = self.builder.get_object("connectors_entry")
        pins_entry = self.builder.get_object("pins_entry")
        tree_iter = self.net_combo.get_active_iter()
        model = self.net_combo.get_model()
        row_id, name = model[tree_iter][:2]
         
        default_errors = defaults(self, 'yep')
        if default_errors[4] == 0 and name == 'Select Tape Network ID':
            display(self, 'Enter number of connectors and pins or select stored network to quick test')
        else:         
            test = 0
            if name == 'Select Tape Network ID':
                connectors = Gtk.Entry.get_text(connectors_entry)
                pins = Gtk.Entry.get_text(pins_entry) 
            else:
                display(self, "Netname = %s" % (name))   
                self.c.execute('SELECT network FROM networks WHERE id=?', (name,))        
                db_net = pickle.loads(self.c.fetchall()[0][0])
                self.c.execute('SELECT no_pins FROM networks WHERE id=?', (name,))
                pins = self.c.fetchone()[0]
                self.c.execute('SELECT no_connectors FROM networks WHERE id=?', (name,))
                connectors = self.c.fetchone()[0]
                test = 1              
            self.board.set_connectors(connectors)
            self.board.set_pins(pins)
            
            scan = self.board.scan_results()
            displayl(self,scan)
            if scan != db_net and test == 1:
                display(self, 'errors found')
                displayl(self, check(scan, db_net))
            elif scan == db_net and test == 1:
                display(self,'no errors found')
            

            
        
    def learn(self, learn_button):
        display(self, '\n')
        net_ID_entry = self.builder.get_object("net_ID_entry") 
        user_ID_entry = self.builder.get_object("user_ID_entry")
        connectors_entry = self.builder.get_object("connectors_entry")
        pins_entry = self.builder.get_object("pins_entry")
        #get all info about network to save into database
        net_ID = Gtk.Entry.get_text(net_ID_entry)
        user_ID = Gtk.Entry.get_text(user_ID_entry)
        connectors = Gtk.Entry.get_text(connectors_entry)
        pins = Gtk.Entry.get_text(pins_entry)   
        timestamp = '{:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now())
        
        default_errors = defaults(self, 'Select Tape Network ID')
        #first check all required info has been added to save
        if default_errors[2] == 0:      
            displayl(self,default_errors[0])
        else:    
            
            ###check net_ID not in database already
            self.c.execute('SELECT EXISTS(SELECT 1 FROM networks WHERE id = ?)',(net_ID,))
            
            if self.c.fetchone()[0]==1:
                display(self,'network already found with name  %s'%(net_ID))      
            else:        
                #update board with pin/connector info and scan
                self.board.set_connectors(connectors)
                self.board.set_pins(pins)
                network = self.board.scan_results()

                display(self,net_ID, user_ID, connectors, pins, timestamp)
                displayl(network)
                #add network
                self.c.execute('INSERT INTO networks(id, timestamp, user, no_connectors, no_pins, network) VALUES(?,?,?,?,?,?)', (net_ID, timestamp, user_ID, connectors, pins, pickle.dumps(network)))
                self.db.commit()
                display(self,'added to database')
                #update liststore and combobox with new network name taken 
                self.net_liststore.append([1, str(net_ID)])
                self.net_liststore1.append([1, str(net_ID)])
                
            
            #run program and learn network
            #update database with learned network
            #(option to delete nets in database)
       
    def log(self, log_button):
        display(self, '\n')
        tape_ID_entry = self.builder.get_object("tape_ID_entry")
        user_ID_entry = self.builder.get_object("user_ID_entry")
        tree_iter = self.net_combo.get_active_iter()
        model = self.net_combo.get_model()
        row_id, net_ID = model[tree_iter][:2]
        tape_ID = Gtk.Entry.get_text(tape_ID_entry)
        user_ID = Gtk.Entry.get_text(user_ID_entry)
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        
        #first check all required info has been added to save
        default_errors = defaults(self, net_ID)
        
        error_list = []
        if default_errors[3] == 0:      
            displayl(self,default_errors[1])         
        else:
            if net_ID != 'Select Tape Network ID':

                self.c.execute('SELECT no_pins FROM networks WHERE id=?', (net_ID,))
                pins = self.c.fetchone()[0]
                self.c.execute('SELECT no_connectors FROM networks WHERE id=?', (net_ID,))
                connectors = self.c.fetchone()[0]
                self.board.set_connectors(connectors)
                self.board.set_pins(pins)

                scan = self.board.scan_results() 
                displayl(self, scan)       
                #get errors by comparing scan with net scan in database
                self.c.execute('SELECT network FROM networks WHERE id=?', (net_ID,))        
                db_net = pickle.loads(self.c.fetchall()[0][0])

            else:
                display(self, 'Select a network to test against')
            
            if scan != db_net:
                display(self,'errors found')
                error = 'Failed'
                displayl(self, check(scan, db_net))
                error_list = check(scan, db_net)
                
                    
                ########display errors and add to table############################################################################
            else:
                display(self,'no errors found')
                error_list.append('No Errors')
                error = 'Passed'
            #create a table for tape ID in database if there isnt one already and insert dated test results as row in database
            self.c.execute("CREATE TABLE IF NOT EXISTS [" +str(tape_ID)+ "](timestamp TEXT, user TEXT, network TEXT, errors TEXT, scan BLOB, errorlist BLOB)")
            try:

                self.c.execute('INSERT INTO [' +str(tape_ID)+ '](timestamp, user, network, errors, scan, errorlist) VALUES(?,?,?,?,?,?)',(timestamp, user_ID, net_ID, error, pickle.dumps(scan), pickle.dumps(error_list)))
                display(self, 'added to database')
            except:
                pass
            self.db.commit()
            display(self,tape_ID)
            
            
            

       
        
        
    def reconnect(self, reconnect_button):
        display(self, '\n')
        ports = listSerialPorts()
        displayl(self,ports)
        if len(ports) >1:
            try:
                self.board.serial.close()
            except:
                pass
            try:
                self.board = expander(str(ports[0]), 9600)
                display(self,'connected to board on COM port %s' %(ports[0]))
                display(self,'board id is %s' %(self.board.i_d()))
                display(self,'if incorrect board ID is displayed try unplug board and reconnect, connects automatically to last COM port plugged in')
                
            except:
                display(self,'connection failed on COM port %s, try plug board in again' % (ports[0]))
        else:
            display(self, 'no board connected')
            
    def open_results(self, open_button):
        display(self, '\n')
        open_entry = self.builder.get_object('open_entry')
        filename = Gtk.Entry.get_text(open_entry)
        try:
            self.c.execute('SELECT timestamp, user, network, errors, errorlist FROM [' +str(filename)+ ']')
            display(self, 'Timestamp                        |User            |Net              |Passed             |Errors')
            data = self.c.fetchall()
            for i in range(len(data)):
                errors = pickle.loads(data[i][4])
                print(errors)
                display(self, ''+data[i][0]+'        '+data[i][1]+'            '+data[i][2]+'             '+data[i][3]+'             '+str(errors)+'')

        except:
            display(self, 'No results found in database for tape ID given')
            
    def open_net(self, open_net_button):
        display(self, '\n')
        tree_iter = self.net_combo1.get_active_iter()
        model = self.net_combo1.get_model()
        row_id, netname = model[tree_iter][:2]       
        try:
            self.c.execute('SELECT network FROM networks WHERE id=?', (netname,))
            string_net = self.c.fetchall()
            displayl(self, pickle.loads(string_net[0][0]))
        except:
            pass
                
                
                
if __name__ == '__main__':
    try:
        
        gui = MyApp()
        Gtk.main()
    except KeyboardInterrupt:
        pass


