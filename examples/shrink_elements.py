import gustaf as gus

if __name__ == "__main__":
    # create 2x3x4 test hexa element
    v_res = [2, 3, 4]
    vertices = gus.create.vertices.raster(
            bounds=[[0, 0, 0], [1, 1, 1]], resolutions=v_res
    )
    connec = gus.utils.connec.make_hexa_volumes(v_res)
    v = gus.Volumes(vertices.vertices, connec)

    try:
        # v shrink - f shrink - e shrink
        e = v.shrink().tofaces().shrink().toedges().shrink()
        e.vis_dict["arrows"] = True

        direct_toedges = v.toedges(unique=False).shrink()
        direct_toedges.vis_dict["arrows"] = True

        # not the most efficient way, but it is possible.
        gus.show.show_vedo(
                ["v, Volumes", v],
                ["v.shrink()", v.shrink()],
                [
                        "v.shrink().tofaces().shrink()",
                        v.shrink().tofaces().shrink(),
                ],
                [
                        "v.shrink().tofaces().shrink().toedges().shrink()",
                        v.shrink().tofaces().shrink().toedges().shrink(),
                ],
                [
                        "as arrows - useful for orientation check!",
                        e,
                ],
                [
                        "v.toedges(unique=False).shrink()\nas arrows",
                        direct_toedges,
                ],
        )

    except BaseException:
        v.show()
        v.shrink().tofaces().show()
        v.shrink().tofaces().shrink().show()
        v.shrink().tofaces().shrink().toedges().show()
        v.shrink().tofaces().shrink().toedges().shrink().show()
