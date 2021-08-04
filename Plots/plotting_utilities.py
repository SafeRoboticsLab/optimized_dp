import plotly.graph_objects as go
import numpy as np
import os 

def plot_isosurface(grid, V, plot_option):
    dims_plot = plot_option.dims_plot
    idx = [slice(None)] * grid.dims
    slice_idx = 0

    dims_list = list(range(0, grid.dims))
    for i in dims_list:
        if i not in dims_plot:
            idx[i] = plot_option.slices[slice_idx]
            slice_idx += 1

    if plot_option.plot_type == '3d_plot':
        if len(dims_plot) != 3:
            raise Exception('dims_plot length should be equal to 3\n')
        else:
            dim1, dim2, dim3 = dims_plot[0], dims_plot[1], dims_plot[2]
            complex_x = complex(0, grid.pts_each_dim[dim1])
            complex_y = complex(0, grid.pts_each_dim[dim2])
            complex_z = complex(0, grid.pts_each_dim[dim3])
            mg_X, mg_Y, mg_Z = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y,
                                        grid.min[dim3]:grid.max[dim3]: complex_z]

            # graph value table while keeping speed constant
            # if V.ndim == 4:
            #     V = V[:, :, s, :]
            my_V = V[tuple(idx)]

            if (V > 0.0).all() or (V < 0.0).all():
                print("Implicit surface will not be shown since all values have the same sign ")
            print("Plotting beautiful plots. Please wait\n")
            fig = go.Figure(data=go.Isosurface(
                x=mg_X.flatten(),
                y=mg_Y.flatten(),
                z=mg_Z.flatten(),
                value=my_V.flatten(),
                colorscale='jet',
                isomin=0,
                surface_count=1,
                isomax=0,
                caps=dict(x_show=True, y_show=True)
            ))
            fig.show()
            print("Please check the plot on your browser.")
    elif plot_option.plot_type == '2d_plot':
        if len(dims_plot) != 2:
            raise Exception('dims_plot length should be equal to 2\n')
        else:
            dim1, dim2 = dims_plot[0], dims_plot[1]
            complex_x = complex(0, grid.pts_each_dim[dim1])
            complex_y = complex(0, grid.pts_each_dim[dim2])
            mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
            
            # graph value table while keeping speed constant
            # if V.ndim == 4:
            #     V = V[:, :, s, :]
            my_V = V[tuple(idx)]

            if (V > 0.0).all() or (V < 0.0).all():
                print("Implicit surface will not be shown since all values have the same sign ")
            print("Plotting beautiful plots. Please wait\n")
            fig = go.Figure(data=go.Contour(
                x=mg_X.flatten(),
                y=mg_Y.flatten(),
                z=my_V.flatten(),
                #value=my_V.flatten(),
                colorscale='jet',
                ncontours= 1,
                zmin= 0,
                zmax= 0.1,
                contours_coloring='lines',
                line_width=2,
                showlegend = False
                
            ))
            #if not os.path.exists("images"):
            #    os.mkdir("images")
            #fig.write_image("images/fig1.png")
            fig.show()
            print("Please check the plot on your browser.")
