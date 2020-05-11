from panda3d.core import loadPrcFileData
loadPrcFileData('', 'sync-video f')
loadPrcFileData('', 'show-frame-rate-meter f')
loadPrcFileData('', 'win-size 800 600')
loadPrcFileData('', 'window-title ')
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.task import Task
import os
base = ShowBase()
w, h = 800, 600
props = WindowProperties()
props.setSize(w, h)
props.setFixedSize(True)
props.setTitle("")
base.win.requestProperties(props)
text = TextNode("node name")
textNodePath = aspect2d.attachNewNode(text)
textNodePath.setScale(0.4)
textNodePath.setScale(1.3)
textNodePath.setPos(-10.6,30,0)
textNodePath.reparentTo(render)
text.setTextColor(1,1,1,1)
font = text.getFont()
text.setWordwrap(16.5)
font.setPixelsPerUnit(60)
text.setFont(font)
base.setBackgroundColor(0,0,0)
base.disableMouse()
def itemSel():
    textfile = open('test.txt')
    f=open("test.txt", "r")
    b = f.read()
    text.setText(b)
    base.trackball.node().setPos(0, 0,6)
itemSel()
def exampleTask(task):
    dt = globalClock.getDt()
    base.camera.setZ(base.camera, -2 * dt)
    return task.cont
taskMgr.doMethodLater(2, exampleTask, 'MyTaskName')
base.run()
