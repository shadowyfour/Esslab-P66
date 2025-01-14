from collections import deque
from enum import Enum

from MofIdentifier.Molecules import Molecule
from MofIdentifier.SubGraphMatching import SubGraphMatcher
from MofIdentifier.bondTools import Distances
from MofIdentifier.fileIO import XyzWriter


class SBUCollection:
    def __init__(self, clusters, connectors, auxiliaries):
        self.clusters = clusters
        self.num_cluster_atoms = sum(len(sbu.atoms) * sbu.frequency for sbu in clusters)
        self.connectors = connectors
        self.num_connector_atoms = sum(len(sbu.atoms) * sbu.frequency for sbu in connectors)
        self.auxiliaries = auxiliaries
        self.num_auxiliary_atoms = sum(len(sbu.atoms) * sbu.frequency for sbu in auxiliaries)
        try:
            self.avg_node_connectivity = sum(len(sbu.adjacent_connector_ids) * sbu.frequency for sbu in clusters) / \
                sum(sbu.frequency for sbu in clusters)
        except ZeroDivisionError:
            self.avg_node_connectivity = float('inf')
        try:
            self.avg_conn_connectivity = sum(len(sbu.adjacent_cluster_ids) * sbu.frequency for sbu in connectors) / \
                sum(sbu.frequency for sbu in connectors)
        except ZeroDivisionError:
            self.avg_conn_connectivity = float('inf')

    def __str__(self):
        string = ""
        if len(self.clusters) > 0:
            string += "Clusters:"
            for cluster in self.clusters:
                string += "\n" + cluster.__str__()
            string += "\n"
        if len(self.connectors) > 0:
            string += "Connectors:"
            for connector in self.connectors:
                string += "\n" + connector.__str__()
            string += "\n"
        if len(self.auxiliaries) > 0:
            string += "Auxiliaries:"
            for auxiliary in self.auxiliaries:
                string += "\n" + auxiliary.__str__()
            string += "\n"
        return string

    def all(self):
        return self.clusters + self.connectors + self.auxiliaries

    def nodes_with_auxiliaries(self):
        clusters = dict()
        node_by_id = dict()
        for node in self.clusters:
            node_by_id[node.sbu_id] = node
            clusters[node] = []
        for aux in self.auxiliaries:
            for node_id in aux.adjacent_cluster_ids:
                node = node_by_id[node_id]
                clusters[node].append(aux)
        return clusters.items()

    def __add__(self, other):
        return SBUCollection(self.clusters + other.clusters, self.connectors
                             + other.connectors, self.auxiliaries + other.auxiliaries)

    @classmethod
    def empty(cls):
        return cls([], [], [])


class UnitType(Enum):
    CLUSTER = 1
    CONNECTOR = 2
    AUXILIARY = 3

    def __str__(self):
        return "cluster" if self == UnitType.CLUSTER else "connector" if self == UnitType.CONNECTOR else "auxiliary"


class changeableSBU(Molecule.Molecule):
    def __init__(self, sbu_id, unit_type, atoms, frequency=1, adjacent_cluster_ids=None, file_content=''):
        super().__init__('No Filepath/Unlabeled', atoms)
        # Right now, SBUs are constructed with atoms as sets; a refactor to lists wouldn't break much though
        if adjacent_cluster_ids is None:
            adjacent_cluster_ids = set()
        # file_content will get set to something other than '' as part of SBUIdentifier.run_algorithm(),
        # which also creates the changeableSBU to start
        self.file_content = file_content
        self.sbu_id = sbu_id
        self.adjacent_cluster_ids = adjacent_cluster_ids
        self.adjacent_connector_ids = set(())
        self.adjacent_auxiliary_ids = set(())
        self.type = unit_type
        self.frequency = frequency
        self.hash = sum(hash(atom) for atom in atoms)
        if self.frequency == float('inf'):
            self.should_use_weak_comparison = True

    def connections(self):
        return len(self.adjacent_auxiliary_ids) + len(self.adjacent_cluster_ids) + len(self.adjacent_connector_ids)

    def add_atom(self, atom):
        self.atoms.add(atom)
        if atom.type_symbol in self.elementsPresent:
            self.elementsPresent[atom.type_symbol] += 1
        else:
            self.elementsPresent[atom.type_symbol] = 1

    def normalize_atoms(self, mof):
        atoms = []
        for atom in self.atoms:
            while not atom.is_in_unit_cell():
                atom = atom.original
            atoms.append(atom)
        atoms.sort()
        starting_atom = atoms[0]  # Get an atom, any atom # Mark
        visited = {starting_atom}
        queue = deque([starting_atom])
        while queue:
            atom = queue.popleft()
            for neighbor in (n for n in atom.bondedAtoms if n in atoms and n not in visited):
                d = Distances.distance(atom, neighbor)
                if not Distances.is_bond_distance(d, atom, neighbor):
                    da = db = dc = 0
                    if neighbor.a - atom.a > 0.5:
                        da -= 1.0
                    elif neighbor.a - atom.a < -0.5:
                        da += 1.0
                    if neighbor.b - atom.b > 0.5:
                        db -= 1.0
                    elif neighbor.b - atom.b < -0.5:
                        db += 1.0
                    if neighbor.c - atom.c > 0.5:
                        dc -= 1.0
                    elif neighbor.c - atom.c < -0.5:
                        dc += 1.0
                    neighbor_in_right_place = neighbor.copy_to_relative_position(da, db, dc, mof.angles,
                                                                                 mof.fractional_lengths, mof.unit_volume)
                else:
                    neighbor_in_right_place = neighbor
                visited.add(neighbor_in_right_place)
                queue.append(neighbor_in_right_place)
        self.atoms = visited
        self.elementsPresent = dict()
        for atom in atoms:
            if atom.type_symbol in self.elementsPresent:
                self.elementsPresent[atom.type_symbol] += 1
            else:
                self.elementsPresent[atom.type_symbol] = 1
        self.file_content = XyzWriter.atoms_to_xyz_string(self.atoms, '')

    def __str__(self):
        unit = str(self.type)
        return "{freq}x {label}: {atoms}({atom_n} atom {unittype}) each bonded to {cluster} clusters, {connector} " \
               "connectors, and {aux} auxiliary groups".format(label=self.label, freq=self.frequency,
                                                               atoms=self.atoms_string(), atom_n=len(self.atoms),
                                                               unittype=unit, cluster=len(self.adjacent_cluster_ids),
                                                               connector=len(self.adjacent_connector_ids),
                                                               aux=len(self.adjacent_auxiliary_ids))

    def __hash__(self):
        return self.hash

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __eq__(self, other):
        is_isomorphic = SubGraphMatcher.match(self, other)
        if isinstance(other, changeableSBU):
            return is_isomorphic and len(self.adjacent_connector_ids) == len(other.adjacent_connector_ids) \
                and len(self.adjacent_cluster_ids) == len(other.adjacent_cluster_ids) \
                and len(self.adjacent_auxiliary_ids) == len(other.adjacent_auxiliary_ids)
        else:
            return is_isomorphic

    def graph_equals(self, other):
        return len(self.atoms) == len(other.atoms) and SubGraphMatcher.match(self, other)
