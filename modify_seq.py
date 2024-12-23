#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 20:22:55 2024

@author: misha
"""

import MDAnalysis as mda
import argparse
import random

types = ['1', '2']

def modify_seq(u, prob = 0., nsplit = None):

    atomtypes = u.atoms.types

    new_seq = []

    npoly = len(u.atoms)

    for i in range(npoly):
        r = random.random()
        if r < prob:
            new_seq.append(types[1])
        else:
            new_seq.append(types[0])

    u.atoms.types = new_seq

    #Remove bonds
    if nsplit is not None:
        atom_molecule_tags = [int(i*nsplit/npoly)+1 for i in range(npoly)]
        prev_tag = atom_molecule_tags[:-1]
        prev_ix = u.atoms.ix[:-1]
        next_tag = atom_molecule_tags[1:]
        next_ix = u.atoms.ix[1:]
        diff_tags = [next_tag != prev_tag for prev_tag, next_tag
                     in zip(prev_tag, next_tag)]
        indices = [i for i, to_cut in enumerate(diff_tags) if to_cut]
        prev_atom_ix = [prev_ix[ix] for ix in indices]
        next_atom_ix = [next_ix[ix] for ix in indices]
        #Remove angles
        bonds_to_delete = list(zip(prev_atom_ix, next_atom_ix))
        u.delete_bonds(bonds_to_delete)
        for bond_atoms in bonds_to_delete:
            for angle in u.angles:
                atom_in_angle_count = 0
                for i in range(3):
                    atom_ix = angle.atoms[i].ix
                    if atom_ix in bond_atoms:
                        atom_in_angle_count += 1
                if atom_in_angle_count >= 2:
                    u.delete_angles([angle])
        u.trajectory.ts.data['molecule_tag'] = atom_molecule_tags

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Modify some atoms' types from 1 to 2")

    parser.add_argument("input", type = str, help = "input filename")

    parser.add_argument("output", type = str, help = "output filename")

    parser.add_argument("--prob", type = float, help = "probability of atom type change")

    parser.add_argument("--split-equal", metavar = "M", nargs = 1, type = int, 
                        default = None, help = "split into M equal chains")

    args = parser.parse_args()

    prob = args.prob

    nsplit = args.split_equal[0]

    # Read configuration

    u = mda.Universe(args.input)

    modify_seq(u, prob = prob, nsplit = nsplit)

    u.atoms.write(args.output)