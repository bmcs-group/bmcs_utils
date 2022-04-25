
import traits.api as tr
from bmcs_utils.app_window import AppWindow
from bmcs_utils.view import View
from bmcs_utils.i_model import IModel
from .controller import Controller

@tr.provides(IModel)
class Model(tr.HasTraits):
    """Base class for interactive bmcs_utils
    """

    name = tr.Str("<unnamed>")

    tree = []

    depends_on = []

    ipw_view = View()

    def __init__(self,*args,**kw):
        super().__init__(*args, **kw)
        self.update_observers()

    def get_controller(self, app_window):
        return Controller(model=self, app_window=app_window)

    plot_backend = 'mpl'
    """"plot_backend = 'mpl' or 'k3d'"""

    def subplots(self, fig):
        if self.plot_backend == 'mpl':
            return fig.subplots(1, 1)
        elif self.plot_backend == 'k3d':
            return fig
        else:
            raise NameError(self.plot_backend + ' is not a valid plot_backend!')

    def plot(self, axes):
        """Alias to update plot - to be overloaded by subclasses"""
        self.update_plot(axes)

    def update_plot(self, axes):
        pass

    def interact(self,**kw):
        return AppWindow(self, **kw).interact()

    def app(self,**kw):
        return AppWindow(self,**kw).interact()

    def get_tree_items(self):
        return self.tree

    def get_tree_submodels(self):
        submodels = []
        for key in self.get_tree_items():
            trait = self.trait(key)
            if trait == None:
                raise ValueError('trait %s not found in %s' % (key, self))
            if trait.is_mapped:
                submodels.append(getattr(self, key + '_'))
            else:
                submodels.append(getattr(self, key))
        return submodels

    def get_tree_subnode(self, name):
        # Construct a tree structure of instances tagged by `tree`
        submodels = self.get_tree_submodels()
        tree_subnodes = [
            submodel.get_tree_subnode(node_name)
            for node_name, submodel in zip(self.tree, submodels)
        ]
        return (name, self, tree_subnodes)

    as_tree_node = get_tree_subnode

    # Notifications along the dependency tree

    def _notify_tree_change(self, event):
        self.tree_changed = True
#        self.update_observers()

    tree_changed = tr.Event
    """Event signaling the tree widgets to rebuild"""

    @tr.observe('+TIME,+MESH,+MAT,+CS,+BC,+ALG,+FE,+DSC,+GEO,+ITR')
    def notify_state_change(self, event):
        if self.state_change_debug:
            print('state_changed', self, event)
        self.state_changed = True

    state_change_debug = tr.Bool(False)

    state_changed = tr.Event
    """Event used in model implementation to notify the need for update"""

    def update_observers(self):
        name, model, nodes = self.as_tree_node('root')
        for sub_name, submodel, subnodes in nodes:
#            model.observe(self._notify_tree_change,'state_changed')
#            model.observe(self._notify_tree_change,sub_name)
            submodel.observe(model.notify_state_change,'state_changed')


# backward compatibility
InteractiveModel = Model