
import ipytree as ipt
import traitlets as tl
from bmcs_utils.controller import Controller

class BMCSNode(ipt.Node):
    trait = tl.Any
    controller = tl.Any

