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
    kb=KnowledgeBase([])
    load_kb()
    kb.printRules()

    rule = kb.get_rule(17)
    print(rule.cornerstone.index('Persistent Depressive Disorder\r\n'))
    rule.cornerstone[23] = 'Persistent Depressive Disorder'
    kb.printRules()
    save_kb()

if __name__ == '__main__':
    editRules()
