# import pygraphviz as pgv
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






#
#
# def make_graph(family):
#     a = pgv.AGraph(directed=True, strict=True)
#     print('making graphs')
#     for parent in family:
#         if parent is not None:
#             for child in family[parent]:
#                 if child is not None:
#                     print(f'parent: {parent}, child: {child}')
#                     a.add_edge(f'{parent}', f'{child}')
#     pic_name = 'here.png'
#     a.layout()
#     a.draw(f'static/{pic_name}')
#     print(pic_name)
#     return pic_name
#
#
def get_pic_name(FamilyMember):
    pass
    # bonds = get_list_of_children(FamilyMember)
    # pic_name = make_graph(bonds)
    # return pic_name


