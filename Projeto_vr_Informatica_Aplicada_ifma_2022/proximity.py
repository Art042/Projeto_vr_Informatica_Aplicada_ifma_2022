import viz
import vizact
import vizcam
import vizproximity

import vizinfo

def proximity(manager):
    vizinfo.InfoPanel()

    # Create proximity manager
    manager = vizproximity.Manager()
    manager.setDebug(True)

    # Add main viewpoint as proximity target
    target = vizproximity.Target(viz.MainView)
    manager.addTarget(target)

    # Register callbacks for proximity sensors
    def EnterProximity(e):
        print('Entrou',e.sensor)

    def ExitProximity(e):
        print('Saiu',e.sensor)

    manager.onEnter(None, EnterProximity)
    manager.onExit(None, ExitProximity)

    # Press spacebar to toggle debug shapes
    vizact.onkeydown(' ',manager.setDebug,viz.TOGGLE)

