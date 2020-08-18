import pygraphviz as pgv
from .models import FamilyMember


def get_list_of_parents(family_member, FamilyMember, parents = {}):
    print(family_member, family_member.parents)
    if len(family_member.parents)!=['']:
        for parent in family_member.parents:
            p = None
            if FamilyMember.objects.filter(full_name=parent):
                p = FamilyMember.objects.filter(full_name=parent)[0]
                parents[p] = {}
                get_list_of_parents(p, FamilyMember, parents[p])
        if parents: return parents

    else:
        return parents
    print(parents)
    return parents


def get_parents_dict(bond):
    bonds = {}
    relatives = []
    for family_member in FamilyMember.objects.all():
        if bond == 'parents':
            relatives = family_member.get_list_of_parents()
        elif bond == 'partners':
            relatives = family_member.get_list_of_partners()
        for relative in relatives:
            if relative not in bonds.keys():
                bonds[relative] = [family_member]
            else:
                bonds[relative].append(family_member)
    return bonds

def make_graph(parents, partners):
    a = pgv.AGraph(directed=True, strict=True)
    a.node_attr['shape']='box'
    a.edge_attr.update(len='2.0')
    print('Creating parents graph:')
    for parent in parents:
        if parent is not None:
            for child in parents[parent]:
                if child is not None:
                    print(f'Parent: {parent}, Child: {child}')
                    a.add_edge(f'{parent}', f'{child}')

    print('Creating partners graph:')
    for partner in partners:
        if partner is not None:
            for other_partner in partners[partner]:
                if other_partner is not None:
                    print(f'Partner: {partner}, Another Partner: {other_partner}')
                    a.add_edge(f'{partner}', f'{other_partner}', directed=False)
    if a is None:
        print('Nothing to add')
    else:
        a.layout()
        a.draw('static/family_graph.png')
        print('The family_graph.png is created')


def generate_tree():
    if len(FamilyMember.objects.all()) > 0:
        parents_dict = get_parents_dict('parents')
        partners_dict = get_parents_dict('partners')
        make_graph(parents_dict, partners_dict)
    else:
        print('Nothing to add')
    return 'family_graph.png'
