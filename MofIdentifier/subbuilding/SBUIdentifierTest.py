import unittest

from MofIdentifier.fileIO.CifReader import get_mof
from MofIdentifier.subbuilding.SBUIdentifier import split


class SBUIdentifierTest(unittest.TestCase):
    def test_simple_mof(self):
        mof_abavij = get_mof('../mofsForTests/ABAVIJ_clean.cif')
        sbu_breakdown = split(mof_abavij)

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
        mof_808 = get_mof('../mofsForTests/smod7-pos-1.cif')
        sbu_breakdown = split(mof_808)

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
        mof_abetae = get_mof('../mofsForTests/ABETAE_clean.cif')
        sbu_breakdown = split(mof_abetae)

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
        mof_akoheo = get_mof('../mofsForTests/AKOHEO_clean.cif')
        sbu_breakdown = split(mof_akoheo)

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
        mof_ja_007 = get_mof('../mofsForTests/ja500330a_si_007_auto.cif')
        sbu_breakdown = split(mof_ja_007)

        assert (len(sbu_breakdown.clusters) == 1)
        assert (sbu_breakdown.clusters[0].frequency == 16)
        assert (len(sbu_breakdown.clusters[0].adjacent_cluster_ids) == 0)
        assert (len(sbu_breakdown.clusters[0].adjacent_connector_ids) == 6)
        assert (len(sbu_breakdown.clusters[0].adjacent_auxiliary_ids) == 12)
        assert (len(sbu_breakdown.clusters[0].atoms) == 18)

        assert (len(sbu_breakdown.connectors) == 1)
        assert (sbu_breakdown.connectors[0].frequency == 32)
        assert (len(sbu_breakdown.connectors[0].adjacent_cluster_ids) == 3)
        assert (len(sbu_breakdown.connectors[0].adjacent_connector_ids) == 0)
        assert (len(sbu_breakdown.connectors[0].adjacent_auxiliary_ids) == 0)
        assert (len(sbu_breakdown.connectors[0].atoms) == 18)

        assert (len(sbu_breakdown.auxiliaries) == 1)


if __name__ == '__main__':
    unittest.main()