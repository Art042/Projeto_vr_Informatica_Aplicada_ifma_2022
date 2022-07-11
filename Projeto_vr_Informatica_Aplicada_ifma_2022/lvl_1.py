import viz
import vizconnect
import vizshape
import vizact
import grabber as gb
import vizinfo
import collide_config as cl
import proximity as pxt
import vizcam
import vizproximity
import viztask
import sys
    
def lvl_1():
    resource = 'quarto.osgb'

    viz.setMultiSample(4)
    vizconnect.go('config.py')
    vizinfo.InfoPanel('Coloque os Objetos no Local que voce julga o certo e encontre a saida')

    # Add a background environment
    viz.addChild('scenario/'+resource)

    #Add shapes
    pyramid = vizshape.addPyramid(base=(0.2,0.2),height=0.2,pos=[-0.5,1.7,1],alpha=0.7)
    torus = vizshape.addTorus(radius=0.1,tubeRadius=0.015,axis=vizshape.AXIS_X, pos=[0,1.7,1])
    box = vizshape.addCube(size=0.1, pos=[0.5,1.7,1],alpha=0.8)
    #pyramid.texture(viz.addTexture('images/lvl1/espelho.jpg'))
    #torus.texture(viz.addTexture('images/lvl1/espelho.jpg'))
    #box.texture(viz.addTexture('images/lvl1/espelho.jpg'))

    #Animate shapes
    pyramid.addAction(vizact.spin(0,-1,0,15))
    torus.addAction(vizact.spin(0,1,0,15))
    box.addAction(vizact.spin(1,1,1,15))

    pyramid.name = 'pyramid'
    torus.name = 'torus'
    box.name = 'box'

    shapes = [pyramid,torus,box]
    
    #Sensor
    #pxt.proximity()
    manager = vizproximity.Manager()
    manager.setDebug(False)

    # Add main viewpoint as proximity target
    target = vizproximity.Target(viz.MainView)
    manager.addTarget(target)

    # Create sensor
    
    sensor_fim = vizproximity.Sensor(vizproximity.Box([1,1,1],center=[-0.3,0,0]),source=viz.Matrix.translate(3.55380, 1.8, -0.11)) 
    manager.addSensor(sensor_fim)
    
    sensor2 = vizproximity.Sensor(vizproximity.Box([1,1,1],center=[-0.3,0,0]),source=viz.Matrix.translate(3.55381, 1.8, -3.8))
    manager.addSensor(sensor2)
    
    sensor3 = vizproximity.Sensor(vizproximity.Box([1,1,1],center=[0.3,0,0]),source=viz.Matrix.translate(-3.55380, 1.8, -4.49856))
    manager.addSensor(sensor3)

    sensor4 = vizproximity.Sensor(vizproximity.Box([1,1,1],center=[0.3,0,0]),source=viz.Matrix.translate(-3.55380, 1.8, -0.9)) 
    manager.addSensor(sensor4)
    
    #Collision
    cl.collide_config()
    #Grabber
    gb.grabber(shapes)
    
    def Exit(e):
        viz.quit()
    
    manager.onEnter(sensor_fim,Exit)

lvl_1()