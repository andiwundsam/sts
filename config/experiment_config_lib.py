import itertools
import string
import sys

class ControllerConfig(object):
  _port_gen = itertools.count(8888)

  def __init__(self, cmdline="", address="127.0.0.1", port=None, cwd=None, sync=None):
    '''
    Store metadata for the controller.
      - cmdline is an array of command line tokens.

        Note: if you need to pass in the address and port to controller's
        command line, use the aliases __address__ and __port__ to have the
        values interpolated automatically
      - address and port are the sockets switches will bind to
    '''
    if cmdline == "":
      raise RuntimeError("Must specify boot parameters.")
    self.cmdline = cmdline
    self.address = address
    if not port:
      port = self._port_gen.next()

    self.port = port
    if "pox" in self.cmdline:
      self.name = "pox"

    self.cwd = cwd
    if not cwd:
        sys.stderr.write("""
        =======================================================================
        WARN - no working directory defined for controller with command line 
        %s
        The controller is run in the STS base directory. This may result
        in unintended consequences (i.e., POX not logging correctly).
        =======================================================================
        \n""" % (self.cmdline) )

    self.sync = sync

  @property
  def uuid(self):
    return (self.address, self.port)

  @property
  def expanded_cmdline(self):
    return map(lambda(x): string.replace(x, "__port__", str(self.port)),
           map(lambda(x): string.replace(x, "__address__", str(self.address)),
             self.cmdline.split()))

  def __repr__(self):
    attributes = ("cmdline", "address", "port", "cwd", "sync")

    pairs = ( (attr, getattr(self, attr)) for attr in attributes)
    quoted = ( "%s=%s" % (attr, repr(value)) for (attr, value) in pairs if value)

    return self.__class__.__name__  + "(" + ", ".join(quoted) + ")"