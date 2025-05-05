def plot_grid():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_com, y_com, z_com, color='green', s=2)
    for i in range(HOW_MANY):
        index=neighbors[i][1]
        x_n=fib_grid.x_cart[index]
        y_n=fib_grid.y_cart[index]
        z_n=fib_grid.z_cart[index]
        ax.scatter(x_n,y_n,z_n, color='pink',s=100)
    ax.scatter(fib_grid.x_cart[reference], fib_grid.y_cart[reference], fib_grid.z_cart[reference], color='yellow', s=100)
    ax.set_box_aspect([radius_of_earth,radius_of_earth,radius_of_earth])
    ax.legend()
    plt.show()