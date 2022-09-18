import pickle
from KnowledgeBase import Rule, KnowledgeBase

global kb_file_name, kb
kb_file_name = "saved_kb.kb"


def load_kb(path=None):
    global kb
    if not path:
        path = kb_file_name
    with open(path, 'rb') as file:
        kb = pickle.load(file)
        Rule.rule_no = kb.rules[-1].rule_no


def save_kb(path=None):
    global kb_file_name, kb
    if not path:
        path = kb_file_name
    with open(path, 'wb') as file:
        pickle.dump(kb, file)


def editRules():
    global kb
    kb = KnowledgeBase([])
    load_kb()
    kb.printRules()

    rule = kb.get_rule(16)
    rule.conditions.pop('S18')
    kb.printRules()
    save_kb()


def viewRules():
    global kb
    kb = KnowledgeBase([])
    load_kb()
    kb.printRules()
    print("Rules as Inputs:")
    for rule in kb.rules:
        condition = list(rule.conditions.keys())
        tobePrinted = str(
            f"{condition[0]}{rule.conditions[condition[0]][0]}{rule.conditions[condition[0]][1]}")
        for condition in list(rule.conditions.keys())[1:]:
            tobePrinted += f" AND {condition}{rule.conditions[condition][0]}{rule.conditions[condition][1]}"
        tobePrinted += f" --> {rule.conclusion}"
        print(tobePrinted)


if __name__ == '__main__':
    viewRules()
    #editRules()