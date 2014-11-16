#!/Users/neavemj/anaconda/bin/python

"""
Selection of putative genome bins

"""


import traits.api as traits
import traitsui.api as traitsui
import chaco.api as chaco
import chaco.tools.api as chacoTools
import enable.component_editor as enable
import numpy as np


class ScatterPlot(traits.HasTraits):       # ScatterPlot inherits from traits.HasTraits
    mattsplot = traits.Instance(chaco.Plot)
    # marker_size = int(40)    
    traits_view = traitsui.View(
        traitsui.Item('plot',editor=enable.ComponentEditor(), show_label=False),
        width=1000, height=1000, resizable=True, title="Chaco Plot")
        

    def __init__(self, points):
        super(ScatterPlot, self).__init__()
        # points = 100        
        x = np.sort(np.random.random(points))
        y = np.random.random(points)
        plotdata = chaco.ArrayPlotData(x = x, y = y)
        mattsplot = chaco.Plot(plotdata)
        mattsplot.plot(("x", "y"), type="scatter", 
                       color="green", marker_size = x, 
                       marker='circle', name="my_plot")
        mattsplot.title = "Differential Coverage Plot"
             
        my_plot = mattsplot.plots["my_plot"][0]
        
        # add zoom and pan tools
        # the min zoom factors don't allow zooming way out on the plot
        
        zoom = chacoTools.ZoomTool(component=my_plot, tool_mode='range', x_min_zoom_factor = 1, y_min_zoom_factor = 1)      
        my_plot.overlays.append(zoom)
        
        # the restrict to data stops panning into empty space
        pan = chacoTools.PanTool(component=my_plot, constrain_key="shift", 
                                 restrict_to_data=True, drag_button="left")        
        my_plot.tools.append(pan) 

        #lasso_selection = chacoTools.LassoSelection(component=my_plot,
        #                             selection_datasource=my_plot.index,
        #                             #drag_button="left")
        #                             drag_button="right")
        #my_plot.active_tool = lasso_selection
        #my_plot.tools.append(chacoTools.ScatterInspector(my_plot))
        #lasso_overlay = chaco.LassoOverlay(lasso_selection=lasso_selection,
        #                         component=my_plot)
        #my_plot.overlays.append(lasso_overlay)
        
        self.plot = mattsplot
        

if __name__ == "__main__":
    ScatterPlot(1000).configure_traits()





























