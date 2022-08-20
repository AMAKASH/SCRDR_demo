from KnowledgeBase import KnowledgeBase, Rule


def get_kb():
    initializing_rule = Rule({'milk': ("==", 1)},
                             ['aardvark', '1', '0', '0', '1', '0', '0',
                                 '1', '1', '0', '4', '0', 'mammal'],
                             "mammal")

    kb = KnowledgeBase(
        ['name', 'hair', 'feathers', 'eggs', 'milk', 'airborne', 'aquatic', 'backbone', 'breathes', 'fins',
         'no of legs', 'tail', 'target'], initializing_rule)

    kb.add_rule(Rule({'aquatic': ("==", 1)}, [], 'fish'))
    kb.add_rule(Rule({'backbone': ("==", 0),
                     'fins': ("==", 0)}, [], 'mollusc', is_refinement=True, parent=2))

    kb.add_rule(Rule({'feathers': ("==", 1)
                      }, [], 'bird', is_refinement=True, parent=2))

    kb.add_rule(Rule({'milk': ("==", 0),
                     'breathes': ("==", 1)}, [], 'amphibian', is_refinement=True, parent=2))
    #
    kb.add_rule(Rule({'backbone': ("==", 1),
                     'fins': ("==", 0)}, [], 'reptile', is_refinement=True, parent=2))
    kb.add_rule(Rule({'feathers': ("==", 1)}, [], 'bird'))
    kb.add_rule(Rule({'backbone': ("==", 0), 'breathes': (
        "==", 0), 'no of legs': ("==", 0)}, [], 'mollusc'))
    kb.add_rule(Rule({'backbone': ("==", 0), 'breathes': (
        "==", 1), 'eggs': ("==", 1)}, [], 'insect'))
    kb.add_rule(Rule({'no of legs': ("==", 0)}, [],
                'mollusc', is_refinement=True, parent=9))
    kb.add_rule(Rule({'backbone': ("==", 1), 'breathes': (
        "==", 1), 'tail': ("==", 1)}, [], 'reptile'))
    kb.add_rule(Rule({'backbone': ("==", 0), 'breathes': (
        "==", 1), 'no of legs': (">=", 4)}, [], 'mollusc'))

    return kb
