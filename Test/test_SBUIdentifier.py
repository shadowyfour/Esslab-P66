import unittest

from MofIdentifier.fileIO import XyzReader
from MofIdentifier.fileIO.CifReader import get_mof


class SBUIdentifierTest(unittest.TestCase):
    def test_simple_mof(self):
        mof_abavij = get_mof('../MofIdentifier/mofsForTests/ABAVIJ_clean.cif')
        sbu_breakdown = mof_abavij.sbus()

        assert (len(sbu_breakdown.clusters) == 1)
        assert (sbu_breakdown.clusters[0].frequency == 4)
        assert (len(sbu_breakdown.clusters[0].adjacent_connector_ids) == 6)
        assert (len(sbu_breakdown.clusters[0].atoms) == 1)

        assert (len(sbu_breakdown.connectors) == 1)
        assert (sbu_breakdown.connectors[0].frequency == 8)
        assert (len(sbu_breakdown.connectors[0].adjacent_cluster_ids) == 3)
        assert (len(sbu_breakdown.connectors[0].atoms) == 13)

        assert (len(sbu_breakdown.auxiliaries) == 0)

    def test_complex_mof(self):
        mof_808 = get_mof('../MofIdentifier/mofsForTests/smod7-pos-1.cif')
        sbu_breakdown = mof_808.sbus()

        assert (len(sbu_breakdown.clusters) == 1)
        assert (sbu_breakdown.clusters[0].frequency == 4)
        assert (len(sbu_breakdown.clusters[0].adjacent_cluster_ids) == 0)
        assert (len(sbu_breakdown.clusters[0].adjacent_connector_ids) == 6)
        assert (len(sbu_breakdown.clusters[0].adjacent_auxiliary_ids) == 10)
        assert (len(sbu_breakdown.clusters[0].atoms) == 18)

        assert (len(sbu_breakdown.connectors) == 1)
        assert (sbu_breakdown.connectors[0].frequency == 8)
        assert (len(sbu_breakdown.connectors[0].adjacent_cluster_ids) == 3)
        assert (len(sbu_breakdown.connectors[0].adjacent_connector_ids) == 0)
        assert (len(sbu_breakdown.connectors[0].adjacent_auxiliary_ids) == 0)
        assert (len(sbu_breakdown.connectors[0].atoms) == 18)

        assert (len(sbu_breakdown.auxiliaries) == 3)

    def test_small_mof(self):
        mof_abetae = get_mof('../MofIdentifier/mofsForTests/ABETAE_clean.cif')
        sbu_breakdown = mof_abetae.sbus()

        assert (len(sbu_breakdown.clusters) == 1)
        assert (sbu_breakdown.clusters[0].frequency == 20)
        assert (len(sbu_breakdown.clusters[0].adjacent_cluster_ids) == 0)
        assert (len(sbu_breakdown.clusters[0].adjacent_connector_ids) == 4)
        assert (len(sbu_breakdown.clusters[0].adjacent_auxiliary_ids) == 0)
        assert (len(sbu_breakdown.clusters[0].atoms) == 1)

        assert (len(sbu_breakdown.connectors) == 1)
        assert (sbu_breakdown.connectors[0].frequency == 16)
        assert (len(sbu_breakdown.connectors[0].adjacent_cluster_ids) == 5)
        assert (len(sbu_breakdown.connectors[0].adjacent_connector_ids) == 0)
        assert (len(sbu_breakdown.connectors[0].adjacent_auxiliary_ids) == 0)
        assert (len(sbu_breakdown.connectors[0].atoms) == 5)

    def test_notalladjacent_core(self):
        mof_akoheo = get_mof('../MofIdentifier/mofsForTests/AKOHEO_clean.cif')
        sbu_breakdown = mof_akoheo.sbus()

        assert (len(sbu_breakdown.clusters) == 2)
        iron_node = None
        big_node = None
        for cluster in sbu_breakdown.clusters:
            if len(cluster.atoms) == 1:
                iron_node = cluster
            elif len(cluster.atoms) == 31:
                big_node = cluster
        assert (iron_node is not None and big_node is not None)
        assert (iron_node.frequency == 4)
        assert (big_node.frequency == 2)
        assert (len(iron_node.adjacent_cluster_ids) == len(big_node.adjacent_cluster_ids) == 0)
        assert (len(iron_node.adjacent_connector_ids) == 5)
        assert (len(iron_node.adjacent_auxiliary_ids) == 1)
        assert (len(big_node.adjacent_connector_ids) == 8)
        assert (len(big_node.adjacent_auxiliary_ids) == 0)

        assert (len(sbu_breakdown.connectors) == 2)
        central_phosphate = None
        straight_phosphate = None
        for connector in sbu_breakdown.connectors:
            if len(connector.adjacent_cluster_ids) == 3:
                central_phosphate = connector
            elif len(connector.adjacent_cluster_ids) == 2:
                straight_phosphate = connector
        assert (central_phosphate is not None and straight_phosphate is not None)
        assert (central_phosphate.frequency == 4)
        assert (straight_phosphate.frequency == 12)
        assert (len(central_phosphate.adjacent_connector_ids) == len(straight_phosphate.adjacent_connector_ids) == 0)
        assert (len(central_phosphate.adjacent_auxiliary_ids) == len(straight_phosphate.adjacent_auxiliary_ids) == 0)

        assert (len(sbu_breakdown.auxiliaries) == 1)
        assert (sbu_breakdown.auxiliaries[0].frequency == 4)
        assert (len(sbu_breakdown.auxiliaries[0].adjacent_cluster_ids) == 1)
        assert (len(sbu_breakdown.auxiliaries[0].adjacent_connector_ids) == 0)
        assert (len(sbu_breakdown.auxiliaries[0].adjacent_auxiliary_ids) == 0)
        assert (len(sbu_breakdown.auxiliaries[0].atoms) == 2)

    def test_abnormal_fractional_coordinates(self):
        mof_ja_007 = get_mof('../MofIdentifier/mofsForTests/ja500330a_si_007_auto.cif')
        sbu_breakdown = mof_ja_007.sbus()

        self.assertEqual(len(sbu_breakdown.clusters), 1)
        self.assertEqual(sbu_breakdown.clusters[0].frequency, 16)
        self.assertEqual(len(sbu_breakdown.clusters[0].adjacent_cluster_ids), 0)
        self.assertEqual(len(sbu_breakdown.clusters[0].adjacent_connector_ids), 6)
        self.assertEqual(len(sbu_breakdown.clusters[0].adjacent_auxiliary_ids), 12)
        self.assertEqual(len(sbu_breakdown.clusters[0].atoms), 18)

        self.assertEqual(len(sbu_breakdown.connectors), 1)
        self.assertEqual(sbu_breakdown.connectors[0].frequency, 32)
        self.assertEqual(len(sbu_breakdown.connectors[0].adjacent_cluster_ids), 3)
        self.assertEqual(len(sbu_breakdown.connectors[0].adjacent_connector_ids), 0)
        self.assertEqual(len(sbu_breakdown.connectors[0].adjacent_auxiliary_ids), 0)
        self.assertEqual(len(sbu_breakdown.connectors[0].atoms), 18)

        self.assertEqual(len(sbu_breakdown.auxiliaries), 1)

    def test_single_metal_wide_unit_cell(self):
        mof_russaa = get_mof('../MofIdentifier/mofsForTests/RUSSAA_clean.cif')
        sbu_breakdown = mof_russaa.sbus()

        assert (len(sbu_breakdown.clusters) == 2)
        assert (len(sbu_breakdown.clusters[0].atoms) == 1)
        assert (len(sbu_breakdown.clusters[0].atoms) == 1)
        assert (len(sbu_breakdown.auxiliaries) == 0)
        assert (len(sbu_breakdown.connectors) == 3)
        assert (sbu_breakdown.connectors[0].frequency == 4)
        assert (sbu_breakdown.connectors[1].frequency == 4)
        assert (sbu_breakdown.connectors[2].frequency == 4)

    def test_infinite_band_connector(self):
        mof_24205 = get_mof('../MofIdentifier/mofsForTests/acscombsci.5b00188_24205_clean.cif')
        sbu_breakdown = mof_24205.sbus()

        assert (len(sbu_breakdown.clusters) == 1)
        assert (len(sbu_breakdown.auxiliaries) == 0)
        assert (len(sbu_breakdown.connectors) == 3)
        infinite_connector = [c for c in sbu_breakdown.connectors if len(c.atoms) == 23][0]

    def test_h_connections_in_xyz(self):
        mof_maxhoj = get_mof('../MofIdentifier/mofsForTests/MAXHOJ01_clean.cif')
        cif_connector = mof_maxhoj.sbus().connectors[0]
        xyz_connector = XyzReader.get_molecule('../MofIdentifier/ligands/test_resources/connector_1826.xyz')
        self.assertEqual(cif_connector, xyz_connector)

    def test_connector_across_unit_cell(self):
        mof_amoyor = get_mof('../MofIdentifier/mofsForTests/AMOYOR_clean.cif')
        for sbu in mof_amoyor:
            pass


class BreakLargeClustersTest(unittest.TestCase):
    def test_breaking_up_large_clusters(self):
        mof_dotyes = get_mof('../MofIdentifier/mofsForTests/DOTYES_clean.cif')
        sbu_breakdown = mof_dotyes.sbus()
        self.assertEqual(2, len(sbu_breakdown.clusters))
        large_cluster = [c for c in sbu_breakdown.clusters if len(c.atoms) == 57][0]
        small_cluster = [c for c in sbu_breakdown.clusters if len(c.atoms) == 1][0]
        self.assertEqual(8, large_cluster.frequency)
        self.assertEqual(12, small_cluster.frequency)
        self.assertEqual(21, len([atom for atom in large_cluster.atoms if atom.is_metal()]))

    def test_breaking_up_large_clusters_in_complex_mof(self):
        mof_yojman = get_mof(r'../MofIdentifier/mofsForTests/YOJMAN_clean.cif')
        sbu_breakdown = mof_yojman.sbus()
        self.assertGreater(9, len(sbu_breakdown.clusters))
        self.assertGreater(len(sbu_breakdown.clusters), 3)
        large_cluster = [c for c in sbu_breakdown.clusters if len(c.atoms) == 54][0]
        med_cluster = [c for c in sbu_breakdown.clusters if len(c.atoms) == 3][0]
        self.assertEqual(4, large_cluster.frequency)
        self.assertEqual(4, med_cluster.frequency)
        self.assertEqual(18, len([atom for atom in large_cluster.atoms if atom.is_metal()]))

    def test_breaking_up_different_clusters_when_they_are_connected_in_multiple_spots(self):
        mof_ocuvuf = get_mof(r'../MofIdentifier/mofsForTests/OCUVUF_clean.cif')
        sbu_breakdown = mof_ocuvuf.sbus()
        self.assertEqual(3, len(sbu_breakdown.clusters))
        large_cluster = [c for c in sbu_breakdown.clusters if len(c.atoms) == 59][0]
        self.assertEqual(8, large_cluster.frequency)

    def test_comparing_auxiliaries_with_connectors_to_add_bonds(self):
        mof_nopjuz = get_mof(r'../MofIdentifier/mofsForTests/NOPJUZ_clean.cif')
        sbu_breakdown = mof_nopjuz.sbus()
        self.assertEqual(0, len(sbu_breakdown.auxiliaries))


if __name__ == '__main__':
    unittest.main()
