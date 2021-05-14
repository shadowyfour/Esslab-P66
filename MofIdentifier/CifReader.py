from CifFile import ReadCif

from MOF import MOF
from MofIdentifier.MofBondCreator import MofBondCreator
from atom import Atom


def get_mof(filename):
    mof = read_cif(filename)
    bond_creator = MofBondCreator(mof)
    bond_creator.connect_atoms()
    return mof


def read_cif(filename):
    cf = ReadCif(filename)
    cb = cf.first_block()
    label = filename
    try:
        symmetry = cb['_symmetry_cell_setting']
    except KeyError:
        symmetry = None
    length_a = float(cb['_cell_length_a'])
    length_b = float(cb['_cell_length_b'])
    length_c = float(cb['_cell_length_c'])
    angle_alpha = float(cb['_cell_angle_alpha'])
    angle_beta = float(cb['_cell_angle_beta'])
    angle_gamma = float(cb['_cell_angle_gamma'])

    mof = MOF(label, symmetry, length_a, length_b, length_c, angle_alpha, angle_beta, angle_gamma)

    atom_data_loop = cb.GetLoop('_atom_site_label')
    atoms = list(())
    for atomData in atom_data_loop:
        atom = Atom.from_fractional(atomData._atom_site_label,
                                    atomData._atom_site_type_symbol,
                                    float(atomData._atom_site_fract_x),
                                    float(atomData._atom_site_fract_y),
                                    float(atomData._atom_site_fract_z), mof)
        atoms.append(atom)
    mof.set_atoms(atoms)
    return mof


if __name__ == '__main__':
    # uses https://pypi.org/project/PyCifRW/4.3/#description to read CIF files
    MOF_808 = read_cif('smod7-pos-1.cif')
    print(MOF_808)
    print(*MOF_808.elementsPresent)
