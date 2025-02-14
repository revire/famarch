import pygraphviz as pgv
from .models import FamilyMember

def make_family_tree():
    graph = pgv.AGraph(
        strict=False,
        directed=True,
        rankdir='TB',
        splines='ortho',
        bgcolor='white'
    )

    graph.node_attr.update(
        shape='rectangle',
        style='filled',
        fillcolor='lightblue',
        fontname='Helvetica',
        fontsize='12.0',
        margin='0.1'
    )

    graph.edge_attr.update(
        color='black',
        penwidth='1.0'
    )

    for member in FamilyMember.objects.all():
        graph.add_node(member.full_name)

    for member in FamilyMember.objects.all():
        for parent in member.parents:
            if parent and FamilyMember.objects.filter(full_name=parent).exists():
                # Draw edge from parent to child
                graph.add_edge(parent, member.full_name)

    # Add partner relationships (using different edge style)
    for member in FamilyMember.objects.all():
        for partner in member.partners:
            if partner and FamilyMember.objects.filter(full_name=partner).exists():
                # Use undirected edges for partners with a different style
                graph.add_edge(member.full_name, partner, dir='none', color='blue', style='dashed')

    graph.layout(prog='dot')
    graph.draw("static/family_graph.png")
    return "family_graph.png"


def generate_tree():
    if FamilyMember.objects.exists():
        return make_family_tree()
    else:
        print("No family members to create tree")
        return None