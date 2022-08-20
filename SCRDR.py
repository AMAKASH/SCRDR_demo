from KnowledgeBase import Rule, KnowledgeBase
import pandas
import os
import re
import pickle

global kb_file_name, output_path
# kb_file_name = "saved_kb_final.kb"
kb_file_name = "saved_kb.kb"
output_path = 'conclusions.csv'


def clear_output():
    os.system('cls')


def import_kb():
    with open(kb_file_name, 'rb') as file:
        return pickle.load(file)


def save_kb(kb, path=None):
    if not path:
        path = kb_file_name
    with open(path, 'wb') as file:
        pickle.dump(kb, file)


def initialise_output_path(features):
    with open(output_path, 'w') as f:
        to_append = str(f"{','.join(features)}, conclusion\n")
        f.write(to_append)


def append_to_output(case):
    with open(output_path, 'a') as f:
        to_append = str(f"{','.join(map(str,case))}\n")
        f.write(to_append)


def get_rules_from_user(kb):
    relations = '==|<=|>=|<|>'
    conditions = input()
    if conditions == 'exit':
        print("Exiting Program...............")
        os._exit(0)

    split_conditions = conditions.split(' --> ')
    conclusion = split_conditions[1].strip()
    conditions = split_conditions[0].strip().split(' AND ')
    conditions_dictionary = {}
    for condition in conditions:
        split_condition = re.split(relations, condition)
        if split_condition[0] not in kb.features:
            print(f"Error: {split_condition[0]} is not a feature..")
            return False, False
        relation = condition[len(split_condition[0]): condition.index(split_condition[1])]
        conditions_dictionary[split_condition[0]] = (relation, split_condition[1])
    # print(conditions_dictionary)
    if input(f"Do you want to add {conditions_dictionary} --> {conclusion} to kb?(y/n):") != 'y':
        return False, False
    return conditions_dictionary, conclusion


def add_major_rule(kb, case):
    print("No Rule Found for the following case:")
    print(case.to_frame().T.to_string())
    print('Please Write a rule for this case Below:')
    try:
        conditions, conclusion = get_rules_from_user(kb)
    except:
        print("The Rule Was not Added")
        return
    if not conditions:
        print("The Rule Was not Added")
        return
    new_rule = Rule(conditions, list(case), conclusion)
    save_kb(kb, 'saved_kb_bkp.kb')
    kb.add_rule(new_rule)
    clear_output()
    print("New Rule Added")
    save_kb(kb)


def add_refinement_rule(kb, case, parent):
    print(f"Incorrect Conclusion Found for the following case from Rule {parent}:")
    print(case.to_frame().T.to_string())
    print('Please Write a refinement rule for this case Below:')
    try:
        conditions, conclusion = get_rules_from_user(kb)
    except:
        print("The Rule Was not Added")
        return
    if not conditions:
        print("The Rule Was not Added")
        return
    refinement_rule = Rule(conditions, list(case), conclusion, is_refinement=True, parent=parent)
    kb.add_rule(refinement_rule)
    clear_output()
    save_kb(kb, 'saved_kb_bkp.kb')
    print("New Refinement Rule Added")
    save_kb(kb)


def main():
    dataset = pandas.read_csv('animal_dataset.csv')
    features = list(dataset.columns)
    initialise_output_path(features)
    if os.path.exists(kb_file_name):
        kb = import_kb()
        Rule.rule_no = kb.rules[-1].rule_no
    else:
        kb = KnowledgeBase(features)
    no_of_rows = dataset.shape[0]
    dataset['conclusion'] = ""
    kb.printRules()
    itr = 0
    while itr < no_of_rows:
        case = dataset.iloc[itr]
        evaluation = kb.eval_case(list(case))
        # print(case)
        # print(f"{itr}. Evaluation:", evaluation)
        if not evaluation:
            add_major_rule(kb, case)
            kb.printRules()
            continue

        if case['target'] != evaluation[0]:
            dataset.loc[itr, 'conclusion'] = evaluation[0]
            case = dataset.iloc[itr]
            add_refinement_rule(kb, case, evaluation[1])
            kb.printRules()
            continue
        dataset.loc[itr, 'conclusion'] = evaluation[0]
        append_to_output(list(dataset.iloc[itr]))
        itr += 1

    print(dataset.to_string())


if __name__ == "__main__":
    main()
