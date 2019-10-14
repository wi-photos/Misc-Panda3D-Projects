from panda3d.core import *
from direct.task import Task
from direct.interval.IntervalGlobal import *

class short_vfx():
    def __init__(self, parent, texture=None, scale=1.0, Z=0.0, depthTest=False, depthWrite=False):
        self.vfx=loader.loadModel('vfx/short_vfx')         
        if texture != None:
            self.vfx.setTexture(TextureStage.getDefault(), loader.loadTexture(texture), 1)
        self.vfx.reparentTo(render)                       
        self.vfx.setBin('fixed', 40)        
        self.vfx.setDepthWrite(depthWrite)
        self.vfx.setDepthTest(depthTest)
        self.vfx.setLightOff()
        self.vfx.setScale(scale)
        self.vfx.setHpr(-90, 0, 0)
        self.vfx.flattenLight()
        self.Z=Z
        self.parent=parent
        self.vfxU=-0.5
        self.vfxV=0
                
    def start(self, speed=0.05):
        taskMgr.doMethodLater(speed, self.run,'vfx')
        
    def run(self, task): 
        self.vfx.setPos(self.parent.getPos(render))    
        self.vfx.setZ(self.vfx.getZ()+self.Z)
        self.vfxU=self.vfxU+0.5   
        if self.vfxU>=1.0:
            self.vfxU=0
            self.vfxV=self.vfxV-0.5
        if self.vfxV <=-1:
            self.vfx.removeNode()
            return task.done          
        self.vfx.lookAt(base.camera)
        self.vfx.setTexOffset(TextureStage.getDefault(), self.vfxU, self.vfxV)
        return task.again
        
class vfx():
    def __init__(self, parent, texture=None, scale=1.0, Z=0.0, depthTest=False, depthWrite=False):
        self.vfx=loader.loadModel('vfx/vfx2')         
        if texture != None:
            self.vfx.setTexture(TextureStage.getDefault(), loader.loadTexture(texture), 1)
        self.vfx.reparentTo(render)                       
        self.vfx.setBin('fixed', 40)        
        self.vfx.setDepthWrite(depthWrite)
        self.vfx.setDepthTest(depthTest)
        self.vfx.setLightOff()
        self.vfx.setScale(scale)
        self.vfx.setHpr(-90, 0, 0)
        self.vfx.flattenLight()
        self.Z=Z
        self.parent=parent
        self.vfxU=-0.125
        self.vfxV=0
        self.auto_destruct=False
    
    def remove_loop(self):
        self.auto_destruct=True
    
    def loop(self, speed=0.015):
        taskMgr.doMethodLater(speed, self.run_loop,'vfx')
        
    def start(self, speed=0.015):
        taskMgr.doMethodLater(speed, self.run,'vfx')
     
    def run_loop(self,task): 
        if self.auto_destruct:
            self.vfx.removeNode()
            return task.done 
        self.vfx.setPos(self.parent.getPos(render))    
        self.vfx.setZ(self.vfx.getZ()+self.Z)
        self.vfxU=self.vfxU+0.125   
        if self.vfxU>=1.0:
            self.vfxU=0
            self.vfxV=self.vfxV-0.125                         
        self.vfx.lookAt(base.camera)
        #self.vfx.headsUp(base.camera)
        self.vfx.setTexOffset(TextureStage.getDefault(), self.vfxU, self.vfxV)
        return task.again
     
    def run(self,task): 
        self.vfx.setPos(self.parent.getPos(render))    
        self.vfx.setZ(self.vfx.getZ()+self.Z)
        self.vfxU=self.vfxU+0.125   
        if self.vfxU>=1.0:
            self.vfxU=0
            self.vfxV=self.vfxV-0.125
        if self.vfxV <=-1:
            self.vfx.removeNode()
            return task.done          
        self.vfx.lookAt(base.camera)
        self.vfx.setTexOffset(TextureStage.getDefault(), self.vfxU, self.vfxV)
        return task.again
        
class P2Pvfx():
    def  __init__(self, from_target, to_target, texture, scale=1.0, Z=0.0, depthTest=False, depthWrite=False):
        self.vfx=loader.loadModel('vfx/vfx1')         
        if texture != None:
            self.vfx.setTexture(TextureStage.getDefault(), loader.loadTexture(texture), 1)
        self.vfx.reparentTo(render)           
        self.vfx.setBin('fixed', 40)        
        self.vfx.setDepthWrite(depthWrite)
        self.vfx.setDepthTest(depthTest)
        self.vfx.setLightOff()
        self.vfx.setScale(scale)      
        self.vfx.flattenLight()
        self.Z=Z
        self.vfxU=-0.125
        self.vfxV=0
        length =from_target.getDistance(to_target)
        #print length
        self.vfx.setScale(length,1,1)
        self.parent=from_target        
        oldHPR=from_target.getHpr()
        from_target.lookAt(to_target)        
        self.vfx.setHpr(from_target.getHpr())        
        self.vfx.setH(self.vfx,90) 
        from_target.setHpr(oldHPR)
        self.vfx.hide()
        
    def start(self, speed=0.030):    
        taskMgr.doMethodLater(speed, self.run,'vfx')
        
    def run(self, task):         
        self.vfx.setPos(self.parent.getPos(render))  
        self.vfx.show()
        self.vfx.setZ(self.vfx.getZ()+self.Z)        
        self.vfxU=self.vfxU+0.5   
        if self.vfxU>=1.0:
            self.vfxU=0
            self.vfxV=self.vfxV-0.125
        if self.vfxV <=-1:
            self.vfx.removeNode()
            return task.done
        self.vfx.setTexOffset(TextureStage.getDefault(), self.vfxU, self.vfxV)
        return task.again   

class MovingVfx():
    def  __init__(self, from_target, to_target, texture=None, scale=1.0, Z=0.0, time=1.0, gravity=1.0, depthTest=False, depthWrite=False):
        self.vfx=loader.loadModel('vfx/vfx2')         
        if texture != None:
            self.vfx.setTexture(TextureStage.getDefault(), loader.loadTexture(texture), 1)
        self.vfx.reparentTo(render)                       
        self.vfx.setBin('fixed', 40)        
        self.vfx.setDepthWrite(depthWrite)
        self.vfx.setDepthTest(depthTest)
        self.vfx.setLightOff()
        self.vfx.setScale(scale)
        self.vfx.setHpr(-90, 0, 0)
        #self.vfx.setPos(from_target.getPos(render))
        self.vfx.flattenLight()
        self.Z=Z
        self.vfxU=-0.125
        self.vfxV=0
        self.target=to_target
        self.from_target=from_target
        self.time=time
        self.gravity=gravity
        
    def start(self):
        speed=self.time/64
        taskMgr.doMethodLater(speed, self.run,'vfx')
        ProjectileInterval(self.vfx, startPos=self.from_target.getPos(render), endPos=self.target.getPos(render), duration=self.time, gravityMult=self.gravity).start()
        
    def run(self, task):        
        self.vfxU=self.vfxU+0.125   
        if self.vfxU>=1.0:
            self.vfxU=0
            self.vfxV=self.vfxV-0.125
        if self.vfxV <=-1:
            self.vfx.removeNode()
            return task.done          
        self.vfx.lookAt(base.camera)
        self.vfx.setTexOffset(TextureStage.getDefault(), self.vfxU, self.vfxV)
        return task.again
        