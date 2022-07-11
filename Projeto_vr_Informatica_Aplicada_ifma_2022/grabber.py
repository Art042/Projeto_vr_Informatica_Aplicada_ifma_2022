import viz
import vizconnect
import vizshape
import vizact


def grabber(shapes):
    # Code to get the grabber tool by name and supply the list of items which can be grabbed 
    grabber = vizconnect.getRawTool('grabber')
    grabber.setItems(shapes)

    highLighter = grabber.getHighlight()

    #Muda a escala do objeto
    scaleAction = vizact.sequence([vizact.sizeTo(size=[1.3,1.3,1.3],time=1),vizact.sizeTo(size=[1,1,1],time=1)], viz.FOREVER)
    #Muda a cor do Objeto
    fadeAction = vizact.sequence([vizact.fadeTo([0.63,0.32,0.18],time=2),vizact.fadeTo(viz.WHITE,time=2)], viz.FOREVER)

    def onGrab(e):
        e.grabbed.runAction(scaleAction,pool=1)

    def onRelease(e):
        e.released.endAction(pool=1)

    def onIntersection(e):
        for shape in shapes:
            if e.new == shape:
                print('New intersection:',shape.name)
            if e.old == shape:
                print('Old intersection:',shape.name)		

    from tools import grabber
    viz.callback(grabber.GRAB_EVENT, onGrab)
    viz.callback(grabber.RELEASE_EVENT, onRelease)
    viz.callback(grabber.UPDATE_INTERSECTION_EVENT, onIntersection)
    