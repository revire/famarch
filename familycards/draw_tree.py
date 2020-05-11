import pygraphviz as pgv



def get_list_of_children(FamilyMember):
    bonds = {}
    for fm in FamilyMember:
        print(fm)
        for parent in fm.get_list_of_parents():
            if parent not in bonds.keys():
                bonds[parent] = []
            else:
                bonds[parent].append(fm)
    print(bonds)
    return bonds



def make_graph(family):
    a = pgv.AGraph(directed=True, strict=True)
    print('making graphs')
    for parent in family:
        if parent is not None:
            for child in family[parent]:
                if child is not None:
                    print(f'parent: {parent}, child: {child}')
                    a.add_edge(f'{parent}', f'{child}')
    pic_name = 'here.png'
    a.layout()
    a.draw(f'static/{pic_name}')
    print(pic_name)
    return pic_name


def get_pic_name(FamilyMember):
    bonds = get_list_of_children(FamilyMember)
    pic_name = make_graph(bonds)
    return pic_name
