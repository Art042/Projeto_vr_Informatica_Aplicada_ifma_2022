import viz
import vizinfo
import vizconnect
from vizconnect.util import view_collision

def collide_config():
        collide = view_collision.AvatarCollision(collideVertical=True)
        #collide.setCollideList([vizconnect.AVATAR_HEAD])
        collide.setCollideList([vizconnect.AVATAR_HEAD,vizconnect.AVATAR_BASE])
        collide.setTransport(vizconnect.getTransport().getNode3d())

    # Get a handle to the group tracker and update it's position every frame
    # groupTracker = vizconnect.getTracker('group').getRaw()
    # def updateGroup():
    #     groupTracker.setPosition([0,0,0.01],viz.REL_LOCAL)
    # event_handle = vizact.onupdate(0,updateGroup)
    # event_handle.setEnabled(viz.OFF)

    # # Toggle update event with spacebar
    # vizact.onkeydown(' ', event_handle.setEnabled, viz.TOGGLE )