from __future__ import division
import numpy as np
import numpy.polynomial.polynomial as poly
from scipy import constants
from scipy.optimize import newton

def y_deflection(initial_trajectory, flight_length, speed):
    """
    The vertical displacement of an object moving in a parabolic path.

    Parameters
    ----------
    initial_trajectory : float
        The initial angular trajectory of the path (degrees), measured from
        the x-axis. A positive angle is in an anticlockwise direction.
    flight_length : float
        The horizontal component of the distance of the object from the origin
        (m).
    speed : float
        The initial speed of the object (m/s)

    Returns
    -------
    displacement : float
        Vertical displacement of the object (m).
    """
    eqn = parabola_eqn(initial_trajectory, speed)
    return poly.polyval(flight_length, eqn)


def elevation(initial_trajectory, flight_length, speed):
    """
    The immediate inclination of an object moving in a parabolic path

    Parameters
    ----------
    initial_trajectory : float
        The initial angular trajectory of the path (degrees), measured from
        the x-axis. A positive angle is in an anticlockwise direction.
    flight_length : float
        The horizontal component of the distance of a point on the line from
        the origin (m).
    speed : float
        The initial speed of the object (m/s)

    Returns
    -------
    elevation : float
        The direction in which the object is currently moving (degrees). The
        angle is measured relative to the x-axis, with a positive angle in an
        anticlockwise direction.
    """
    eqn = parabola_eqn(initial_trajectory, speed)
    dydx = poly.polyder(eqn)
    return np.degrees(np.arctan(poly.polyval(flight_length, dydx)))


def find_trajectory(theta, flight_length, speed):
    """
    Find the initial trajectory of an object that has to pass through a certain
    point on a parabolic path

    Parameters
    ----------
    theta : float
        The angle between the x-axis and the point (degrees). A positive angle
        is in an anticlockwise direction.
    flight_length : float
        The horizontal component of the distance of a point on the line from
        the origin (m).
    speed : float
        The initial speed of the object (m/s)

    Returns
    -------
    trajectory : float
        Initial trajectory of the object (degrees).  A positive angle lies
        above the x-axis.
    """
    theta_rad = np.radians(theta)
    vertical_deflection_vertex = np.tan(theta_rad) * flight_length

    # now find trajectory that will put object through defined point
    def traj(trajectory):
        return (vertical_deflection_vertex
                - y_deflection(trajectory, flight_length, speed))

    trajectory = newton(traj, 0)
    return trajectory


def parabola_eqn(initial_trajectory, speed):
    """
    Find the quadratic form of the parabolic path

    Parameters
    ----------
    initial_trajectory : float
        The initial angular trajectory of the path (degrees), measured from
        the x-axis. A positive angle is in an anticlockwise direction.
    speed : float
        The initial speed of the object (m/s)
    """
    traj_rad = np.radians(initial_trajectory)
    return np.array([0., np.tan(traj_rad),
                     -constants.g / 2. / (speed * np.cos(traj_rad)) ** 2.])


def parabola_line_intersection_point(initial_trajectory, speed, theta,
                                     flight_length, omega):
    """
    Find the intersection point of the parabolic motion path and a line.
    The line is specified by an angle and a point through which the line
    goes.

    Parameters
    ----------
    initial_trajectory : float
        The initial trajectory of the object (degrees). A positive angle is in
        an anticlockwise direction.
    speed : float
        The initial speed of the object (m/s).
    theta : float
        The declination of a point on the line from the origin (degrees). A
        positive angle is in an anticlockwise direction.
    flight_length : float
        The horizontal component of the distance of a point on the line from
        the origin (m).
    omega : float
        The arctan of the gradient of the line (degrees) going through that
        point (degrees).  i.e. np.tan(np.radians(omega)) is the gradient of
        the line.

    Returns
    -------
    intersect_x, intersect_y, distance : float, float, float
        Co-ordinates of intersection point of parabola and line, and distance
        from the intersection to the point used to specify the line.
    """
    omega_rad = np.radians(omega)
    theta_rad = np.radians(theta)

    # equation of line
    a1 = flight_length * (np.tan(theta_rad) - np.tan(omega_rad))
    b1 = np.tan(omega_rad)

    # equation of parabola
    eqn = parabola_eqn(initial_trajectory, speed)

    intersection_x = np.max(poly.polyroots([eqn[0] - a1, eqn[1] - b1, eqn[2]]))
    intersection_y = a1 + intersection_x * b1
    distance = ((intersection_x - flight_length) ** 2
                + (intersection_y - flight_length * np.tan(theta_rad)) ** 2)
    return intersection_x, intersection_y, np.sqrt(distance)
