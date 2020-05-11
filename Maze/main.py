from panda3d.core import WindowProperties
wp = WindowProperties.getDefault() 
wp.setSize(1000,650)
WindowProperties.setDefault(wp)
from panda3d.core import loadPrcFileData
loadPrcFileData("", "notify-level error")
loadPrcFileData("", "audio-library-name	p3openal_audio")
import sys
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *

from direct.actor.Actor import Actor
from direct.showbase.InputStateGlobal import inputState

from panda3d.core import *

from panda3d.bullet import *

def addTextField(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.5, 0.9), align=TextNode.ALeft, scale = .05, mayChange=True)
class Game(ShowBase):

  def __init__(self):
    ShowBase.__init__(self)
    self.loc_text = addTextField(0.45, "[LOC]: ")
    self.imageObject = OnscreenImage(image = 'models/intro.jpg', pos = (-0, 0, 0.02))
    self.imageObject.setScale(1.6,1.2,1.2)
    base.graphicsEngine.renderFrame()
    base.graphicsEngine.renderFrame()
    base.graphicsEngine.renderFrame()
    base.graphicsEngine.renderFrame()
    base.setBackgroundColor(0, 0, 0, 0)
    base.setFrameRateMeter(True)
    _sky      = Vec4( 0.01, 0.01, 0.01, 0.01 )   
    _clouds   = Vec4( 0.01, 0.01, 0.01, 0.01 ) # vx, vy, vx, vy

    base.cam.setPos(0, -20, 4)
    base.cam.lookAt(0, 0, 0)
    self.skyNP = loader.loadModel( 'models/sky' )
    self.skyNP.reparentTo( render )
    self.skyNP.setScale( 1000, 1000, 300 )
    self.skyNP.setPos( 0, 0, 0 )
    self.skyNP.setTexture( loader.loadTexture( 'models/clouds.jpg' ) )
    self.skyNP.setShader( loader.loadShader( 'shaders/sky.sha' ) )
    self.skyNP.setShaderInput( 'sky', _sky )
    self.skyNP.setShaderInput( 'clouds', _clouds )

    # Light
    alight = AmbientLight('ambientLight')
    alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
    alightNP = render.attachNewNode(alight)

    dlight = DirectionalLight('directionalLight')
    dlight.setDirection(Vec3(1, 1, -1))
    dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    dlightNP = render.attachNewNode(dlight)

    render.clearLight()
    render.setLight(alightNP)
    render.setLight(dlightNP)

    # Input
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f1', self.toggleWireframe)
    self.accept('f2', self.toggleTexture)
    self.accept('f3', self.toggleDebug)
    self.accept('s', self.doScreenshot)

    self.accept('space', self.doJump)

    inputState.watchWithModifiers('forward', 'arrow_up')
    #inputState.watchWithModifiers('left', 'arrow_left')
    inputState.watchWithModifiers('reverse', 'arrow_down')
    #inputState.watchWithModifiers('right', 'arrow_right')
    inputState.watchWithModifiers('turnLeft', 'arrow_left')
    inputState.watchWithModifiers('turnRight', 'arrow_right')

    # Task
    taskMgr.add(self.update, 'updateWorld')

    # Physics
    self.worldNP = render.attachNewNode('World')

    # World
    self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()

    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
   # self.world.setDebugNode(self.debugNP.node())

    # Ground
    shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

    #img = PNMImage(Filename('models/elevation2.png'))
    #shape = BulletHeightfieldShape(img, 1.0, ZUp)

    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
    np.node().addShape(shape)
    np.setPos(0, 0, -100)
    np.setCollideMask(BitMask32.allOn())

    self.world.attachRigidBody(np.node())

    # Box
 
    # Character
    self.crouching = False

    h = 2.75
    w = 0.9
    shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

    self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
    self.characterNP = self.worldNP.attachNewNode(self.character)
    self.characterNP.setPos(-2, 0, 14)
    #self.characterNP.setPos(-4, 75, 74)

    self.characterNP.setCollideMask(BitMask32.allOn())
    self.world.attachCharacter(self.character)

    base.cam.reparentTo(self.characterNP)

    self.pvisualNP = Actor("models/panda-model",
                 {"walk": "models/panda-walk4"})
    self.pvisualNP.clearModelNodes()
    self.pvisualNP.setScale(0.003)
    self.pvisualNP.setZ(-1.2)
    self.pvisualNP.reparentTo(self.characterNP)
    self.pvisualNP.setH(180)
    #self.pvisualNP.loop("walk")
    self.accept('arrow_up', self.pandawalk)
    self.accept('arrow_up-up', self.pandastop)
    self.accept('arrow_down', self.pandawalk)
    self.accept('arrow_down-up', self.pandastop)


    '''
    visualNP.reparentTo(self.characterNP)
    visualNP = loader.loadModel('models/pilot-model')
    visualNP.clearModelNodes()
    visualNP.setScale(0.05)
    visualNP.setZ(-1.1)
    visualNP.setH(190)
    visualNP.reparentTo(self.characterNP)
    '''
    shape = BulletBoxShape(Vec3(2, 2, 0.2))

    self.Elev = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.Elev.node().setMass(0)
    self.Elev.node().addShape(shape)
    self.Elev.setPos(-0.4, 90, 5)
    self.Elev.setScale(2)
    self.Elev.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(self.Elev.node())

    visualNP = loader.loadModel('models/elevator')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.Elev)
    visualNP.setScale(0.5)
    shape = BulletBoxShape(Vec3(2, 2, 0.2))
    
    self.Elev2 = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.Elev2.node().setMass(0)
    self.Elev2.node().addShape(shape)
    self.Elev2.setPos(0,0,28)
    self.Elev2.setScale(2)
    self.Elev2.setH(180)

    self.Elev2.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)
    
    self.world.attachRigidBody(self.Elev2.node())
    
    visualNP = loader.loadModel('models/elevator')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.Elev2)
    visualNP.setScale(0.5)

#self.makeblockwood(1,1,1,1,1,1)

    self.makeblock(0,0,0,5,5,0.5)
    self.makeblock(0,10,-1,2,20,0.5)
    self.makeblock(0,20,0,2,3,0.5)
    self.makeblock(0,25,1,2,3,0.5)
    self.makeblock(0,30,2,2,3,0.5)
    self.makeblock(0,35,3,2,3,0.5)
    self.makeblock(0,40,4,2,3,0.5)
    self.makeblock(0,50,4,10,20,0.5)
    self.makeblockgold(-1,50,5,1,1,1)
    self.makeblockcrate(0,50,6,0.7,0.7,0.7)

    self.makeblockwood(1,50,5,1,1,1)
    self.makeblocksilver(-2.5,50,5,1,1,1)
    self.makeblockstone(2.5,50,5,1,1,1)
    self.makeblock(0,70,4,2,20,0.5)
    self.makeblock(0,90,4,20,20,0.5)
    self.makeblock(0,75,20,20,20,0.5)
    self.makeblockcrate(-1,75,25,1,1,1)
    self.makeblockwood(-1,75,28,1,1,1)
    self.makeblocksilver(-1,75,31,1,1,1)
    self.makeblockgold(-1,75,34,1,1,1)
    self.makeblockstone(-1,75,38,1,1,1)
    self.makeblock(-0.53,50,21.58,2,20,0.5)
    self.makeblock(0,40,23,5,5,0.5)
    self.makeblock(0,20,23,5,5,0.5)
    self.makeblock(0,0,23,5,5,0.5)
    self.makeblock(0,0,26,20,20,0.5)
    self.makeblock(0,25,46,50,50,0.5)



    self.imageObject.hide()

  # _____HANDLER_____

  def doExit(self):
    self.cleanup()
    sys.exit(1)
  def pandawalk(self):
    self.pvisualNP.loop("walk")
  def pandastop(self):
    self.pvisualNP.stop()
  def doReset(self):
    self.characterNP.setPos(-2, 0, 14)
    self.Elev.setPos(-0.4, 90, 5)
    self.Elev2.setPos(0,0,28)


  def toggleWireframe(self):
    base.toggleWireframe()

  def toggleTexture(self):
    base.toggleTexture()

  def toggleDebug(self):
    if self.debugNP.isHidden():
      self.debugNP.show()
    else:
      self.debugNP.hide()

  def doScreenshot(self):
    base.screenshot('Bullet')

  def doJump(self):
    self.character.setMaxJumpHeight(5.0)
    self.character.setJumpSpeed(8.0)
    self.character.doJump()

  def doCrouch(self):
    self.crouching = not self.crouching
    sz = self.crouching and 0.6 or 1.0

    self.characterNP.setScale(Vec3(1, 1, sz))

    #self.character.getShape().setLocalScale(Vec3(1, 1, sz))
    #self.characterNP.setScale(Vec3(1, 1, sz) * 0.3048)
    #self.characterNP.setPos(0, 0, -1 * sz)

  # ____TASK___

  def processInput(self, dt):
    speed = Vec3(0, 0, 0)
    omega = 0.0

    if inputState.isSet('forward'): speed.setY( 20.0)
    if inputState.isSet('reverse'): speed.setY(-20.0)
    if inputState.isSet('left'):    speed.setX(-10.0)
    if inputState.isSet('right'):   speed.setX( 10.0)
    if inputState.isSet('turnLeft'):  omega =  120.0
    if inputState.isSet('turnRight'): omega = -120.0

    self.character.setAngularMovement(omega)
    self.character.setLinearMovement(speed, True)

  def update(self, task):
    dt = globalClock.getDt()
   # self.characterNP.setHpr(0,0,0)
    base.cam.setHpr(0,-5,0)
    
    self.processInput(dt)
    self.world.doPhysics(dt, 4, 1./240.)
    render.setShaderInput( 'time', task.time )
    #charpos = self.characterNP.getPos()
  # self.Elev.setHpr(0,0,0)
    self.Elevtask()
    self.Elevtask2()

#import pickle
    #gg = pickle.dumps(charpos)
    # self.title.setText(gg)
    self.loc_text.setText('[LOC] : %03.2f, %03.2f,%03.2f ' % \
                          ( self.characterNP.getX(), self.characterNP.getY(), self.characterNP.getZ() ) )
    

    return task.cont
  def Elevtask(self):
    if not self.characterNP.node() or not  self.Elev.node():
      return
    result = self.world.contactTestPair(self.characterNP.node(),  self.Elev.node())
    for contact in result.getContacts():
     cp = contact.getManifoldPoint()
     node0 = contact.getNode0()
     node1 = contact.getNode1()
     dt = globalClock.getDt()
    # print('HI')
     #force = Vec3(0, 0, 0)
     self.ElevZ = self.Elev.getZ()
     print (self.ElevZ)

	  #force.setZ( 100.0)
     #force *= 30.0
     #force = render.getRelativeVector(self.Elev, force)
     self.Elev.setZ(self.Elev.getZ() + 4 * dt)
	 #self.characterNP.setZ(self.Elev.getZ() + 30 * dt)
#self.characterNP.setH(180)
  def Elevtask2(self):
    if not self.characterNP.node() or not  self.Elev2.node():
        return
    result = self.world.contactTestPair(self.characterNP.node(),  self.Elev2.node())
    for contact in result.getContacts():
     cp = contact.getManifoldPoint()
     node0 = contact.getNode0()
     node1 = contact.getNode1()
     dt = globalClock.getDt()
                        # print('HI')
                        #force = Vec3(0, 0, 0)
     self.ElevZ2 = self.Elev2.getZ()
     print (self.ElevZ2)
                                
                                #force.setZ( 100.0)
                                #force *= 30.0
                                #force = render.getRelativeVector(self.Elev, force)
     self.Elev2.setZ(self.Elev2.getZ() + 4 * dt)
                                    #self.characterNP.setZ(self.Elev.getZ() + 30 * dt)
                                    #self.characterNP.setH(180)
                                    

  def cleanup(self):
    self.world = None
    self.worldNP.removeNode()
  def makeblock(self,x,y,z,xs,ys,zs):
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

    self.boxNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.boxNP.node().setMass(0.0)
    self.boxNP.node().addShape(shape)
    self.boxNP.setX(x)
    self.boxNP.setY(y)
    self.boxNP.setZ(z)
    self.boxNP.setScale(xs,ys,zs)

    self.boxNP.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(self.boxNP.node())

    visualNP = loader.loadModelCopy('models/blockmetal')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.boxNP)
    visualNP.setScale(0.5)
  def makeblockwood(self,x,y,z,xs,ys,zs):
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

    self.boxNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.boxNP.node().setMass(10.2)
    self.boxNP.node().addShape(shape)
    self.boxNP.setX(x)
    self.boxNP.setY(y)
    self.boxNP.setZ(z)
    self.boxNP.setScale(xs,ys,zs)

    self.boxNP.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(self.boxNP.node())

    visualNP = loader.loadModelCopy('models/blockwood')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.boxNP)
    visualNP.setScale(0.5)
  def makeblockgold(self,x,y,z,xs,ys,zs):
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

    self.boxNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.boxNP.node().setMass(10.2)
    self.boxNP.node().addShape(shape)
    self.boxNP.setX(x)
    self.boxNP.setY(y)
    self.boxNP.setZ(z)
    self.boxNP.setScale(xs,ys,zs)

    self.boxNP.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(self.boxNP.node())

    visualNP = loader.loadModelCopy('models/blockgold')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.boxNP)
    visualNP.setScale(0.5)
 
  def makeblocksilver(self,x,y,z,xs,ys,zs):
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

    self.boxNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.boxNP.node().setMass(10.2)
    self.boxNP.node().addShape(shape)
    self.boxNP.setX(x)
    self.boxNP.setY(y)
    self.boxNP.setZ(z)
    self.boxNP.setScale(xs,ys,zs)

    self.boxNP.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(self.boxNP.node())

    visualNP = loader.loadModelCopy('models/blocksilver')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.boxNP)
    visualNP.setScale(0.5)
  def makeblockstone(self,x,y,z,xs,ys,zs):
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

    self.boxNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.boxNP.node().setMass(10.2)
    self.boxNP.node().addShape(shape)
    self.boxNP.setX(x)
    self.boxNP.setY(y)
    self.boxNP.setZ(z)
    self.boxNP.setScale(xs,ys,zs)

    self.boxNP.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(self.boxNP.node())

    visualNP = loader.loadModelCopy('models/blockstone')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.boxNP)
    visualNP.setScale(0.5) 
  def makeblockcrate(self,x,y,z,xs,ys,zs):
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

    self.boxNP = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
    self.boxNP.node().setMass(10.2)
    self.boxNP.node().addShape(shape)
    self.boxNP.setX(x)
    self.boxNP.setY(y)
    self.boxNP.setZ(z)
    self.boxNP.setScale(xs,ys,zs)

    self.boxNP.setCollideMask(BitMask32.allOn())
    #self.boxNP.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(self.boxNP.node())

    visualNP = loader.loadModelCopy('models/crate')
    visualNP.clearModelNodes()
    visualNP.reparentTo(self.boxNP)
    visualNP.setScale(0.5) 


game = Game()
base.run()

