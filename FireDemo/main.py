from direct.showbase.ShowBase import ShowBase
from direct.particles.ParticleEffect import ParticleEffect
from vfx_loader import createEffect
import json
from vfx import *

class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
        base.cam.setPos(0,-60,0)
        base.enableParticles()
        with open('fire.json') as f:
          values=json.load(f)
        particle_effect=createEffect(values)
        p = ParticleEffect()
        p.loadConfig('fireish.ptf')
        p.start(parent = render, renderParent = render)
        p.setPos(5,0,0)
        p2 = ParticleEffect()
        p2.loadConfig('fireish2.ptf')
        p2.start(parent = render, renderParent = render)
        p2.setPos(10,0,0)
        self.smiley2 = loader.loadModel('smiley')
        self.smiley2.setPos(-5,0,0)
        vfx(self.smiley2, texture='vfx/big_fire3.png',scale=1.0).loop()

app = MyApp()
app.run()
