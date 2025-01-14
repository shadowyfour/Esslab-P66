data = {
    'H': 32,
    'He': 46,
    'Li': 133,
    'Be': 102,
    'B': 85,
    'C': 76,
    'N': 71,
    'O': 71,  # 66?
    'F': 64,
    'Ne': 67,
    'Na': 166,
    'Mg': 141,
    'Al': 126,
    'Si': 116,
    'P': 111,
    'S': 105,
    'Cl': 102,
    'Ar': 106,
    'K': 203,
    'Ca': 176,
    'Sc': 170,
    'Ti': 160,
    'V': 153,
    'Cr': 139,
    'Mn': 150,
    'Fe': 142,
    'Co': 138,
    'Ni': 124,
    'Cu': 132,
    'Zn': 122,
    'Ga': 124,
    'Ge': 121,
    'As': 121,
    'Se': 120,
    'Br': 120,
    'Kr': 117,
    'Rb': 220,
    'Sr': 195,
    'Y': 190,
    'Zr': 175,
    'Nb': 164,
    'Mo': 154,
    'Tc': 147,
    'Ru': 146,
    'Rh': 142,
    'Pd': 139,
    'Ag': 145,
    'Cd': 144,
    'In': 142,
    'Sn': 140,
    'Sb': 140,
    'Te': 138,
    'I': 139,
    'Xe': 140,
    'Cs': 244,
    'Ba': 215,
    'La': 207,
    'Ce': 204,
    'Pr': 203,
    'Nd': 201,
    'Pm': 199,
    'Sm': 198,
    'Eu': 198,
    'Gd': 196,
    'Tb': 194,
    'Dy': 192,
    'Ho': 192,
    'Er': 189,
    'Tm': 190,
    'Yb': 187,
    'Lu': 187,
    'Hf': 175,
    'Ta': 170,
    'W': 162,
    'Re': 151,
    'Os': 144,
    'Ir': 141,
    'Pt': 136,
    'Au': 136,
    'Hg': 133,
    'Tl': 145,
    'Pb': 146,
    'Bi': 151,
    'Po': 145,
    'At': 150,
    'Rn': 150,
    'Fr': 260,
    'Ra': 221,
    'Ac': 215,
    'Th': 206,
    'Pa': 200,
    'U': 166,
    'Np': 190,
    'Pu': 187,
    'Am': 180,
    'Cm': 169,
    'Bk': 168,
    'Cf': 168,
    'Es': 165,
    'Fm': 167,
    'Md': 173,
    'No': 176,
    'Lr': 161,
    'Rf': 157,
    'Db': 149,
    'Sg': 143,
    'Bh': 141,
    'Hs': 134,
    'Mt': 129,
    'Ds': 128,
    'Rg': 121,
    'Cn': 122,
    'Uut': 136,
    'Nh': 136,
    'Uuq': 143,
    'Fl': 143,
    'Uup': 162,
    'Mc': 162,
    'Uuh': 175,
    'Lv': 175,
    'Uus': 165,
    'Ts': 165,
    'Uuo': 157,
    'Og': 157,
    '~': 110,
    '*': 170,
    '&': 170,
}
smallest_r = None
greatest_r = None


def lookup(symbol):
    try:
        return data[symbol] / 100
    except KeyError:
        return 1.60


def smallest_radius():
    global smallest_r
    if smallest_r is None:
        # all_but_smallest_data = data.copy()
        # del all_but_smallest_data['H']
        # del all_but_smallest_data['He']
        smallest_r = min(data.values()) / 100
    return smallest_r


def greatest_radius():
    global greatest_r
    if greatest_r is None:
        greatest_r = max(data.values()) / 100
    return greatest_r


if __name__ == '__main__':
    radius_1 = lookup('N')
    radius_2 = lookup('C')
    print((radius_1 + radius_2) * 1.10 + 0.05)
