import pygraphviz as pgv
#
#
#

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




def get_parents_dict():
    bonds = {}
    for family_member in FamilyMember.objects.all():
        print(family_member)
        print(family_member.parents)
        for parent in family_member.get_list_of_parents():
            if parent not in bonds.keys():
                bonds[parent] = [family_member]
            else:
                bonds[parent].append(family_member)
    print(bonds)
    return bonds



def get_partners_dict():
    bonds = {}
    for family_member in FamilyMember.objects.all():
        print(family_member)
        print(family_member.partners)
        for partner in family_member.get_list_of_partners():
            if partner not in bonds.keys():
                bonds[partner] = [family_member]
            else:
                bonds[partner].append(family_member)
    print(bonds)
    return bonds


def make_graph(parents, partners):
    a = pgv.AGraph(directed=True, strict=True)
    a.edge_attr.update(len='2.0')
    print('making graphs, parents')
    for parent in parents:
        if parent is not None:
            for child in parents[parent]:
                if child is not None:
                    print(f'parent: {parent}, child: {child}')
                    a.add_edge(f'{parent}', f'{child}')

    print('making graphs, parents')
    for partner in partners:
        if partner is not None:
            for other_partner in partners[partner]:
                if other_partner is not None:
                    print(f'parent: {partner}, child: {other_partner}')
                    a.add_edge(f'{partner}', f'{other_partner}', directed=False)



    pic_name = 'here.png'
    a.layout()
    a.draw(f'static/{pic_name}')
    print(pic_name)
    return pic_name


def get_pic_name(FamilyMember):
    parents_dict = get_parents_dict()
    partners_dict = get_partners_dict()
    pic_name = make_graph(parents_dict, partners_dict)
    return pic_name


