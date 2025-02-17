import gustaf as gus
try:
    from . import common as c
except BaseException:
    import common as c


class BasicCallsTest(c.unittest.TestCase):
    """
    Checks basic calls - calls without specific arguments + without further
    dependencies.
    Does not really
    """

    def test_vertices_basics(self):
        """
        Call available properties/methods-without-args of Vertices.
        """
        v = gus.Vertices(c.V)
        v.vertices = v.vertices
        v.const_vertices
        v.whatami
        # v.unique_vertices()
        v.bounds()
        v.bounds_diagonal()
        v.bounds_diagonal_norm()
        v.select_vertices([[-1, .5], [-1, .5], [-1, .5]])
        v.copy()

        # v.update_vertices()
        # v.remove_vertices()
        # v.merge_vertices()
        # v.showable()
        # v.show()
        # gus.Vertices.concat()

    def test_edges_basics(self):
        """
        """
        es = gus.Edges(c.V, c.E)
        es.edges = es.edges
        es.const_edges
        es.whatami
        es.sorted_edges()
        es.unique_edges()
        es.single_edges()
        es.elements = es.elements
        es.const_elements
        es.centers()
        es.referenced_vertices()
        es.dashed()
        es.shrink()
        es.tovertices()
        es.single_edges()
        es.remove_unreferenced_vertices()

        # es.update_elements()
        # es.update_edges()

    def test_faces_basics(self):
        for fs in (gus.Faces(c.V, c.TF), gus.Faces(c.V, c.QF)):
            fs.edges()
            fs.whatami
            fs.faces = fs.faces
            fs.const_faces
            fs.sorted_faces()
            fs.unique_faces()
            fs.single_faces()

            fs.sorted_edges()
            fs.unique_edges()
            fs.single_edges()
            fs.centers()
            fs.referenced_vertices()
            fs.shrink()
            fs.tovertices()
            fs.remove_unreferenced_vertices()

            # fs.update_faces()
            # gus.Faces.whatareyou()

    def test_volumes_bascis(self):
        for vs in (gus.Volumes(c.V, c.TV), gus.Volumes(c.V, c.HV)):
            vs.faces()
            vs.whatami
            vs.volumes = vs.volumes
            vs.const_volumes
            vs.sorted_volumes()
            vs.unique_volumes()
            vs.tofaces()

            vs.sorted_edges()
            vs.unique_edges()
            vs.single_edges()
            vs.centers()
            vs.referenced_vertices()
            vs.shrink()
            vs.tovertices()
            vs.remove_unreferenced_vertices()

            vs.sorted_faces()
            vs.unique_faces()
            vs.single_faces()
            # gus.Faces.whatareyou()


if __name__ == "__main__":
    c.unittest.main()
