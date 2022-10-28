import numpy as np

from gustaf.spline import base


class CrossTile3D(base.GustafBase):

    def __init__(self):
        """Simple crosstile with linear-quadratic branches and a trilinear
        center spline."""
        self._dim = 3
        self._evaluation_points = np.array(
                [
                        [0., .5, .5],
                        [1., .5, .5],
                        [.5, 0., .5],
                        [.5, 1., .5],
                        [.5, .5, 0.],
                        [.5, .5, 1.],
                ]
        )
        self._parameter_space_dimension = 1

    @property
    def parameter_space_dimension(self):
        """Number of parameters per evaluation point."""
        return self._parameter_space_dimension

    @property
    def evaluation_points(self):
        """Positions in the parametrization function to be evaluated when tile
        " "is constructed prior to composition.

        Parameters
        ----------
        None

        Returns
        -------
        evaluation_points : np.ndarray(6,3)
        """
        return self._evaluation_points

    @property
    def dim(self):
        """Returns dimensionality in physical space of the Microtile.

        Parameters
        ----------
        None

        Returns
        -------
        dim : int
        """
        return self._dim

    def closing_tile(
            self,
            parameters=None,
            closure=None,
            boundary_width=0.1,
            filling_height=0.5,
            **kwargs
    ):
        """Create a closing tile to match with closed surface.

        Parameters
        ----------
        parameters : tuple(np.ndarray)
          radii of fitting cylinder at evaluation points
        closure : str
          parametric dimension that needs to be closed.
          Must be {"z_min", "z_max"}
        boundary_width : float
          with of the boundary surronding branch
        filling_height : float
          portion of the height that is filled in parametric domain

        Results
        -------
        list_of_splines : list
        """
        # Check parameters
        if closure is None:
            raise ValueError("No closing direction given")

        if parameters is None:
            self._logd("Tile request is not parametrized, setting default 0.2")
            parameters = tuple([np.ones(6) * 0.2])
        parameters = parameters[0]
        if not (np.all(parameters > 0) and np.all(parameters < .5)):
            raise ValueError("Thickness out of range (0, .5)")

        if not (0. < float(boundary_width) < .5):
            raise ValueError("Boundary Width is out of range")

        if not (0. < float(filling_height) < 1.):
            raise ValueError("Filling must  be in (0,1)")

        inv_boundary_width = 1. - boundary_width
        inv_filling_height = 1. - filling_height
        center_width = 1. - 2 * boundary_width
        ctps_mid_height_top = (1 + filling_height) * .5
        ctps_mid_height_bottom = 1. - ctps_mid_height_top
        r_center = center_width * .5

        spline_list = []
        if closure == "z_min":
            # The branch is located at zmin of current tile
            branch_thickness = parameters[5]
            ctps_corner = np.array(
                    [
                            [0., 0., 0.], [boundary_width, 0., 0.],
                            [0., boundary_width, 0.],
                            [boundary_width, boundary_width, 0.],
                            [0., 0., filling_height],
                            [boundary_width, 0., filling_height],
                            [0., boundary_width, filling_height],
                            [boundary_width, boundary_width, filling_height]
                    ]
            )

            spline_list.append(
                    base.Bezier(degrees=[1, 1, 1], control_points=ctps_corner)
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=(
                                    ctps_corner
                                    + np.array([0., inv_boundary_width, 0.])
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=(
                                    ctps_corner
                                    + np.array([inv_boundary_width, 0., 0.])
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=(
                                    ctps_corner + np.array(
                                            [
                                                    inv_boundary_width,
                                                    inv_boundary_width, 0.
                                            ]
                                    )
                            )
                    )
            )

            center_ctps = np.array(
                    [
                            [boundary_width, boundary_width, 0.],
                            [inv_boundary_width, boundary_width, 0.],
                            [boundary_width, inv_boundary_width, 0.],
                            [inv_boundary_width, inv_boundary_width, 0.],
                            [boundary_width, boundary_width, filling_height],
                            [
                                    inv_boundary_width, boundary_width,
                                    filling_height
                            ],
                            [
                                    boundary_width, inv_boundary_width,
                                    filling_height
                            ],
                            [
                                    inv_boundary_width, inv_boundary_width,
                                    filling_height
                            ]
                    ]
            )

            spline_list.append(
                    base.Bezier(degrees=[1, 1, 1], control_points=center_ctps)
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.maximum(
                                    center_ctps
                                    - np.array([center_width, 0, 0]), 0
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.maximum(
                                    center_ctps
                                    - np.array([0, center_width, 0]), 0
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.minimum(
                                    center_ctps
                                    + np.array([center_width, 0, 0]), 1.
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.minimum(
                                    center_ctps
                                    + np.array([0, center_width, 0]), 1.
                            )
                    )
            )
            branch_ctps = np.array(
                    [
                            [-r_center, -r_center, filling_height],
                            [r_center, -r_center, filling_height],
                            [-r_center, r_center, filling_height],
                            [r_center, r_center, filling_height],
                            [
                                    -branch_thickness, -branch_thickness,
                                    ctps_mid_height_top
                            ],
                            [
                                    branch_thickness, -branch_thickness,
                                    ctps_mid_height_top
                            ],
                            [
                                    -branch_thickness, branch_thickness,
                                    ctps_mid_height_top
                            ],
                            [
                                    branch_thickness, branch_thickness,
                                    ctps_mid_height_top
                            ], [-branch_thickness, -branch_thickness, 1.],
                            [branch_thickness, -branch_thickness, 1.],
                            [-branch_thickness, branch_thickness, 1.],
                            [branch_thickness, branch_thickness, 1.]
                    ]
            ) + np.array([.5, .5, 0.])

            spline_list.append(
                    base.Bezier(degrees=[1, 1, 2], control_points=branch_ctps)
            )

            return spline_list
        elif closure == "z_max":
            # The branch is located at zmax of current tile
            branch_thickness = parameters[4]
            ctps_corner = np.array(
                    [
                            [0., 0., inv_filling_height],
                            [boundary_width, 0., inv_filling_height],
                            [0., boundary_width, inv_filling_height],
                            [
                                    boundary_width, boundary_width,
                                    inv_filling_height
                            ], [0., 0., 1.], [boundary_width, 0., 1.],
                            [0., boundary_width, 1.],
                            [boundary_width, boundary_width, 1.]
                    ]
            )

            spline_list.append(
                    base.Bezier(degrees=[1, 1, 1], control_points=ctps_corner)
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=(
                                    ctps_corner
                                    + np.array([0., inv_boundary_width, 0.])
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=(
                                    ctps_corner
                                    + np.array([inv_boundary_width, 0., 0.])
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=(
                                    ctps_corner + np.array(
                                            [
                                                    inv_boundary_width,
                                                    inv_boundary_width, 0.
                                            ]
                                    )
                            )
                    )
            )

            center_ctps = np.array(
                    [
                            [
                                    boundary_width, boundary_width,
                                    inv_filling_height
                            ],
                            [
                                    inv_boundary_width, boundary_width,
                                    inv_filling_height
                            ],
                            [
                                    boundary_width, inv_boundary_width,
                                    inv_filling_height
                            ],
                            [
                                    inv_boundary_width, inv_boundary_width,
                                    inv_filling_height
                            ], [boundary_width, boundary_width, 1.],
                            [inv_boundary_width, boundary_width, 1.],
                            [boundary_width, inv_boundary_width, 1.],
                            [inv_boundary_width, inv_boundary_width, 1.]
                    ]
            )

            spline_list.append(
                    base.Bezier(degrees=[1, 1, 1], control_points=center_ctps)
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.maximum(
                                    center_ctps
                                    - np.array([center_width, 0, 0]), 0
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.maximum(
                                    center_ctps
                                    - np.array([0, center_width, 0]), 0
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.minimum(
                                    center_ctps
                                    + np.array([center_width, 0, 0]), 1.
                            )
                    )
            )

            spline_list.append(
                    base.Bezier(
                            degrees=[1, 1, 1],
                            control_points=np.minimum(
                                    center_ctps
                                    + np.array([0, center_width, 0]), 1.
                            )
                    )
            )

            branch_ctps = np.array(
                    [
                            [-branch_thickness, -branch_thickness, 0.],
                            [branch_thickness, -branch_thickness, 0.],
                            [-branch_thickness, branch_thickness, 0.],
                            [branch_thickness, branch_thickness, 0.],
                            [
                                    -branch_thickness, -branch_thickness,
                                    ctps_mid_height_bottom
                            ],
                            [
                                    branch_thickness, -branch_thickness,
                                    ctps_mid_height_bottom
                            ],
                            [
                                    -branch_thickness, branch_thickness,
                                    ctps_mid_height_bottom
                            ],
                            [
                                    branch_thickness, branch_thickness,
                                    ctps_mid_height_bottom
                            ], [-r_center, -r_center, inv_filling_height],
                            [r_center, -r_center, inv_filling_height],
                            [-r_center, r_center, inv_filling_height],
                            [r_center, r_center, inv_filling_height]
                    ]
            ) + np.array([.5, .5, 0.])

            spline_list.append(
                    base.Bezier(degrees=[1, 1, 2], control_points=branch_ctps)
            )

            return spline_list
        else:
            raise NotImplementedError(
                    "Requested closing dimension is not supported"
            )

    def create_tile(self, parameters=None, center_expansion=1., **kwargs):
        """Create a microtile based on the parameters that describe the branch
        thicknesses.

        Thickness parameters are used to describe the inner radius of the
        outward facing branches

        Parameters
        ----------
        parameters : tuple(np.array)
          only first entry is used, defines the internal radii of the
          branches
        center_expansion : float
          thickness of center is expanded by a factor

        Returns
        -------
        microtile_list : list(splines)
        """

        if not isinstance(center_expansion, float):
            raise ValueError("Invalid Type")
        if not ((center_expansion > .5) and (center_expansion < 1.5)):
            raise ValueError("Center Expansion must be in (.5,1.5)")
        max_radius = min(.5, (.5 / center_expansion))
        # set to default if nothing is given
        if parameters is None:
            self._logd("Setting branch thickness to default 0.2")
            parameters = tuple([np.ones(6) * 0.2])
        [x_min_r, x_max_r, y_min_r, y_max_r, z_min_r,
         z_max_r] = parameters[0].tolist()
        for radius in [x_min_r, x_max_r, y_min_r, y_max_r, z_min_r, z_max_r]:
            if not isinstance(radius, float):
                raise ValueError("Invalid type")
            if not (radius > 0 and radius < max_radius):
                raise ValueError(
                        f"Radii must be in (0,{max_radius}) for "
                        f"center_expansion {center_expansion}"
                )

        # center radius
        center_r = (
                x_min_r + x_max_r + y_min_r + y_max_r + z_min_r + z_max_r
        ) / 6. * center_expansion
        hd_center = 0.5 * (0.5 + center_r)

        # Create the center-tile
        center_points = np.array(
                [
                        [-center_r, -center_r, -center_r],
                        [center_r, -center_r, -center_r],
                        [-center_r, center_r, -center_r],
                        [center_r, center_r, -center_r],
                        [-center_r, -center_r, center_r],
                        [center_r, -center_r, center_r],
                        [-center_r, center_r, center_r],
                        [center_r, center_r, center_r]
                ]
        )

        center_spline = base.Bezier(
                degrees=[1, 1, 1], control_points=center_points + [.5, .5, .5]
        )

        # X-Axis branches
        # X-Min-Branch
        aux_x_min = min(x_min_r, center_r)
        x_min_ctps = np.array(
                [
                        [-.5, -x_min_r, -x_min_r],
                        [-hd_center, -aux_x_min,
                         -aux_x_min], center_points[0, :],
                        [-.5, x_min_r, -x_min_r],
                        [-hd_center, aux_x_min,
                         -aux_x_min], center_points[2, :],
                        [-.5, -x_min_r, x_min_r],
                        [-hd_center, -aux_x_min, aux_x_min],
                        center_points[4, :], [-.5, x_min_r, x_min_r],
                        [-hd_center, aux_x_min, aux_x_min], center_points[6, :]
                ]
        )
        x_min_spline = base.Bezier(
                degrees=[2, 1, 1], control_points=x_min_ctps + [.5, .5, .5]
        )
        # X-Min-Branch
        aux_x_max = min(x_max_r, center_r)
        x_max_ctps = np.array(
                [
                        center_points[1, :],
                        [hd_center, -aux_x_max, -aux_x_max],
                        [.5, -x_max_r, -x_max_r], center_points[3, :],
                        [hd_center, aux_x_max, -aux_x_max],
                        [.5, x_max_r, -x_max_r], center_points[5, :],
                        [hd_center, -aux_x_max, aux_x_max],
                        [.5, -x_max_r, x_max_r], center_points[7, :],
                        [hd_center, aux_x_max, aux_x_max],
                        [.5, x_max_r, x_max_r]
                ]
        )
        x_max_spline = base.Bezier(
                degrees=[2, 1, 1], control_points=x_max_ctps + [.5, .5, .5]
        )

        # Y-Axis branches
        # Y-Min-Branch
        aux_y_min = min(y_min_r, center_r)
        y_min_ctps = np.array(
                [
                        [-y_min_r, -.5, -y_min_r], [y_min_r, -.5, -y_min_r],
                        [-aux_y_min, -hd_center, -aux_y_min],
                        [aux_y_min, -hd_center,
                         -aux_y_min], center_points[0, :], center_points[1, :],
                        [-y_min_r, -.5, y_min_r], [y_min_r, -.5, y_min_r],
                        [-aux_y_min, -hd_center, aux_y_min],
                        [aux_y_min, -hd_center, aux_y_min],
                        center_points[4, :], center_points[5, :]
                ]
        )
        y_min_spline = base.Bezier(
                degrees=[1, 2, 1], control_points=y_min_ctps + [.5, .5, .5]
        )
        # Y-Min-Branch
        aux_y_max = min(y_max_r, center_r)
        y_max_ctps = np.array(
                [
                        center_points[2, :], center_points[3, :],
                        [-aux_y_max, hd_center, -aux_y_max],
                        [aux_y_max, hd_center, -aux_y_max],
                        [-y_max_r, .5, -y_max_r], [y_max_r, .5, -y_max_r],
                        center_points[6, :], center_points[7, :],
                        [-aux_y_max, hd_center, aux_y_max],
                        [aux_y_max, hd_center, aux_y_max],
                        [-y_max_r, .5, y_max_r], [y_max_r, .5, y_max_r]
                ]
        )
        y_max_spline = base.Bezier(
                degrees=[1, 2, 1], control_points=y_max_ctps + [.5, .5, .5]
        )

        # Y-Axis branches
        # Y-Min-Branch
        aux_z_min = min(z_min_r, center_r)
        z_min_ctps = np.array(
                [
                        [-z_min_r, -z_min_r, -.5], [z_min_r, -z_min_r, -.5],
                        [-z_min_r, z_min_r, -.5], [z_min_r, z_min_r, -.5],
                        [-aux_z_min, -aux_z_min, -hd_center],
                        [aux_z_min, -aux_z_min, -hd_center],
                        [-aux_z_min, aux_z_min, -hd_center],
                        [aux_z_min, aux_z_min,
                         -hd_center], center_points[0, :], center_points[1, :],
                        center_points[2, :], center_points[3, :]
                ]
        )
        z_min_spline = base.Bezier(
                degrees=[1, 1, 2], control_points=z_min_ctps + [.5, .5, .5]
        )
        # Y-Min-Branch
        aux_z_max = min(z_max_r, center_r)
        z_max_ctps = np.array(
                [
                        center_points[4, :], center_points[5, :],
                        center_points[6, :], center_points[7, :],
                        [-aux_z_max, -aux_z_max, hd_center],
                        [aux_z_max, -aux_z_max, hd_center],
                        [-aux_z_max, aux_z_max, hd_center],
                        [aux_z_max, aux_z_max, hd_center],
                        [-z_max_r, -z_max_r, .5], [z_max_r, -z_max_r, .5],
                        [-z_max_r, z_max_r, .5], [z_max_r, z_max_r, .5]
                ]
        )
        z_max_spline = base.Bezier(
                degrees=[1, 1, 2], control_points=z_max_ctps + [.5, .5, .5]
        )

        return [
                center_spline, x_min_spline, x_max_spline, y_min_spline,
                y_max_spline, z_min_spline, z_max_spline
        ]