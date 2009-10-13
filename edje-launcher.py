#!/usr/bin/env python

import evas
import ecore
import ecore.evas
import edje
import os, sys, time

def unlockScreenTest(obj,signal,source):
    ee.hide()

# Resize callback
def resize_callback(ee):
    c.size = ee.evas.size

ee = ecore.evas.SoftwareX11(w=480, h=640)
edje_file = sys.argv[1]
print "opening '%s'" % edje_file

t = time.localtime()
c = edje.Edje(ee.evas,file=edje_file,group="shr-today")
c.size = ee.evas.size
c.signal_callback_add("unlockScreen","slider",unlockScreenTest)
c.part_text_set("time",time.strftime("%H:%M", t))
c.part_text_set("date",time.strftime("%d %b %Y", t))
ee.callback_resize = resize_callback

c.signal_emit("100","batteryPowerChange")

c.signal_emit("100","gsmSignalChange")
c.part_text_set("gsmProvider","congstar")

c.signal_emit("","activateCpuResource")
c.signal_emit("","activateDisplayResource")
c.signal_emit("","activateBluetoothResource")
c.signal_emit("","activateWifiResource")
c.signal_emit("","activateGpsResource")
c.signal_emit("","activateAlarm")
c.signal_emit("","activate_incomingCall")
#c.signal_emit("","deactivate_incomingCall")

c.signal_emit("","showUnfinishedTasks")
c.signal_emit("","showUnreadMessages")
c.signal_emit("","showMissedCalls")
c.part_text_set("unfinishedTasksLabel", "2")
c.part_text_set("unreadMessagesLabel", "5")
c.part_text_set("missedCallsLabel", "3")
c.part_text_set("profile", "Vibrate")

#ee.fullscreen = True

c.show()
ee.show()
ecore.main_loop_begin();
