import random
import Pyro4
import sys

sys.excepthook = Pyro4.util.excepthook

@Pyro4.expose
class MediatorCh:
    def __init__(self, m):
        self._nodes = []#limit the size
        self._mbits = m

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self,value):
        self._nodes = value
    
    @property
    def mbits(self):
        return self._mbits
    


    def GetUriNode(self,uriNode):
        if not uriNode in self.nodes:
            while True:
                try:
                    uri = random.choice(self.nodes)
                    try:
                        n = Pyro4.Proxy(uri)
                        n.key
                        self.nodes.append(uriNode)
                        return uri
                    except:
                        self._nodes.remove(uri)
                    
                except IndexError:
                    self.nodes.append(uriNode)
                    return ''
        else:
            return -1

    def RemoveUri(self,uri):
        print(self._nodes)
        self._nodes.remove(uri)
    

if __name__ == "__main__":
    m = 4
    if len(sys.argv) > 1:
        m = int(sys.argv[1])
    
    mediator = MediatorCh(m)
    
    with Pyro4.Daemon() as daemon:
        mediator_uri = daemon.register(mediator)

        with Pyro4.locateNS() as ns:
            ns.register(f"Mediator", mediator_uri)
        daemon.requestLoop()                 