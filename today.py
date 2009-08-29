#!/usr/bin/env python
#-*- coding: utf-8 -*-

import elementary, ecore
import dbus, e_dbus
import time
import ConfigParser

class MainWindow:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("today.conf")
        self.BACKGROUND = self.config.get("background", "image")

        self.bus = dbus.SystemBus(mainloop = e_dbus.DBusEcoreMainLoop())
        self.bus.add_signal_receiver(self.dbus_suspend_handler, dbus_interface="org.freesmartphone.Usage", signal_name="SystemAction")
        self.bus.add_signal_receiver(self.dbus_aux_handler, dbus_interface="org.freesmartphone.Device.Input", signal_name="Event")
        self.bus.add_signal_receiver(self.dbus_idle_handler, dbus_interface="org.freesmartphone.Device.IdleNotifier", signal_name="State")
        self.bus.add_signal_receiver(self.IncomingCall, dbus_interface="org.freesmartphone.GSM.Call", signal_name="CallStatus")
        self.bus.add_signal_receiver(self.NewMissedCalls, dbus_interface="org.freesmartphone.PIM.Calls", signal_name="NewMissedCalls")
        self.bus.add_signal_receiver(self.UnreadMessages, dbus_interface="org.freesmartphone.PIM.Messages", signal_name="UnreadMessages")
        self.proxy = self.bus.get_object('org.freesmartphone.odeviced', '/org/freesmartphone/Device/Display/0')

        self.win = elementary.Window("today", elementary.ELM_WIN_BASIC)
        self.win.title_set("Today")
        self.win.destroy = self.destroy

        bg = elementary.Background(self.win)
        self.win.resize_object_add(bg)
        bg.file_set(self.BACKGROUND)
        bg.size_hint_weight_set(1.0, 1.0)
        bg.show()

        mainbox = elementary.Box(self.win)
        mainbox.size_hint_weight_set(1.0, 1.0)
        self.win.resize_object_add(mainbox)
        mainbox.show()

        self.timeLabel = elementary.Label(self.win)
        self.timeLabel.label_set("")
        self.timeLabel.scale_set(5.0)
        mainbox.pack_end(self.timeLabel)
        self.timeLabel.show()

        self.dateLabel = elementary.Label(self.win)
        self.dateLabel.label_set("")
        self.dateLabel.scale_set(1.75)
        mainbox.pack_end(self.dateLabel)
        self.dateLabel.show()

        subBox = elementary.Box(self.win)
        subBox.size_hint_weight_set(1.0, 0.1)
        self.win.resize_object_add(subBox)
        mainbox.pack_end(subBox)
        subBox.show()

        self.IncomingCallLabel = elementary.Label(self.win)
        self.IncomingCallLabel.label_set("")
        self.IncomingCallLabel.scale_set(1.75)
        subBox.pack_end(self.IncomingCallLabel)
        self.IncomingCallLabel.show()

        self.callsLabel = elementary.Label(self.win)
        self.callsLabel.label_set("")
        self.callsLabel.scale_set(1.75)
        subBox.pack_end(self.callsLabel);
        self.callsLabel.show()

        self.messagesLabel = elementary.Label(self.win)
        self.messagesLabel.label_set("")
        self.messagesLabel.scale_set(1.75)
        subBox.pack_end(self.messagesLabel);
        self.messagesLabel.show()

        self.toggle = elementary.Toggle(self.win)
        self.toggle.label_set("")
        self.toggle.states_labels_set("unlocked", "slide to unlock")
        self.toggle.scale_set(2.0)
        self.toggle.changed = self.toggleChanged
        self.toggle.state_set(False)
        mainbox.pack_end(self.toggle)
        self.toggle.show()

    ### functions ###
    def dbus_suspend_handler(self, name):
        """Locks the screen on suspend"""
        if name == "SUSPEND":
            print "SetBacklightPower(False)"
            self.proxy.SetBacklightPower(False)
            self.lockScreen()
        elif name == "RESUME":
            print "SetBacklightPower(True)"
            self.proxy.SetBacklightPower(True)

    def dbus_aux_handler(self, name, action, seconds):
        """Locks the screen on AUX keypress < 2 sec"""
        if name == "AUX" and action == "released" and int(seconds) < 2:
            self.lockScreen()

    def dbus_idle_handler(self, name):
        """Locks the screen on FSO 'lock' signal"""
        if name == "lock":
            self.lockScreen()

    def IncomingCall(self, *args):
        """Updates screen on incoming call"""
        if args[1] == "incoming":
            self.IncomingCallLabel.label_set(args[2]['peer']+" is calling")
        elif args[1] == "active":
            self.IncomingCallLabel.label_set("active call")
        elif args[1] == "release":
            self.IncomingCallLabel.label_set("")

    def NewMissedCalls(self, missedCalls):
        """Updates screen on new missed call"""
        if missedCalls == 0:
            self.callsLabel.label_set("")
        elif missedCalls == 1:
            self.callsLabel.label_set(str(missedCalls)+" missed call")
        else:
            self.callsLabel.label_set(str(missedCalls)+" missed calls")

    def UnreadMessages(self, unreadMessages):
        """Updates screen on new unread message"""
        if unreadMessages == 0:
            self.messagesLabel.label_set("")
        elif unreadMessages == 1:
            self.messagesLabel.label_set(str(unreadMessages)+" unread message")
        else:
            self.messagesLabel.label_set(str(unreadMessages)+" unread messages")

    def toggleChanged(self, obj, event, *args, **kargs):
        """Unlocks Screen if toggle is slided"""
        if self.toggle.state_get():
            self.unlockScreen()
            self.toggle.state_set(False)

    def lockScreen(self):
        """Locks the screen"""
    	self.win.fullscreen_set(True)
        self.win.show()

    def unlockScreen(self):
        """Unlocks the screen"""
        self.win.hide()

    def updateScreen(self):
        """Updates the time and date labels on the screen every second"""
        t = time.localtime()
        self.timeLabel.label_set("%02d:%02d" % (t.tm_hour, t.tm_min))
        self.dateLabel.label_set("%02d-%02d-%04d" % (t.tm_mon, t.tm_mday,t.tm_year))
        ecore.timer_add(1, self.updateScreen)

    def destroy(obj, event, *args, **kargs):
        """Closes the application"""
        elementary.exit()

if __name__ == "__main__":
    elementary.init()
    win = MainWindow()
    win.updateScreen()
    elementary.run()
    elementary.shutdown()
