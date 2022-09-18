from KnowledgeBase import Rule, KnowledgeBase
import pandas
import os
import re
import pickle

global kb_file_name, output_path, kb, relational_regex
# kb_file_name = "saved_kb_final.kb"
kb_file_name = "saved_kb.kb"
output_path = 'conclusion/conclusions.csv'
relational_regex = '==|<=|>=|<|>'


def clear_output():
    os.system('cls')


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


def initialise_output_path(features):
    with open(output_path, 'w') as f:
        to_append = str(f"{','.join(features)}, conclusion,"
                        # f" rules Evaluated, rules Fired\n"
                        )
        f.write(to_append)


def append_to_output(case):
    with open(output_path, 'a') as f:
        to_append = str(f"{','.join(map(str, case))}\n")
        f.write(to_append)


def get_user_inputs():
    global kb
    user_input = input()
    if user_input.strip() == 'exit':
        print("Exiting Program...............")
        os._exit(0)
    elif user_input.strip() == 'undo':
        load_kb('saved_kb_bkp.kb')
        return False, False

    user_input = user_input.split('-->')
    conclusion = user_input[1].strip()
    conditions = user_input[0].strip().split(' AND ')
    conditions_dictionary = {}
    for condition in conditions:
        split_condition = re.split(relational_regex, condition)
        if split_condition[0].strip() not in kb.features:
            print(f"Error: {split_condition[0]} is not a feature..")
            return False, False
        relation = condition[len(split_condition[0]): len(split_condition[0])+2]
        conditions_dictionary[split_condition[0]] = (relation, split_condition[1])
    # print(conditions_dictionary)
    if input(f"Do you want to add {conditions_dictionary} --> {conclusion} to kb?(y/n):") != 'y':
        return False, False
    return conditions_dictionary, conclusion


def add_rule(case, parent=None):
    if parent:
        print(f"Incorrect Conclusion Found for the following case from Rule {parent}:")
        print(case.to_frame().T.to_string())
        print('Please Write a refinement rule for this case Below:')
    else:
        print("No Rule Found for the following case:")
        print(case.to_frame().T.to_string())
        print('Please Write a rule for this case Below:')

    try:
        conditions, conclusion = get_user_inputs()
    except:
        print("The Rule Was not Added")
        return
    if not conditions:
        print("The Rule Was not Added")
        return

    if parent:
        new_rule = Rule(conditions, list(case), conclusion, is_refinement=True, parent=parent)
    else:
        new_rule = Rule(conditions, list(case), conclusion)

    save_kb('saved_kb_bkp.kb')
    kb.add_rule(new_rule)
    clear_output()
    print("New Rule Added")
    save_kb()


def print_original_columns(msg, col):
    print(msg)
    age_group = col[1].replace('\n', '\n\t\t')
    print('\t', f"=> {age_group}")
    for i, col_name in enumerate(col[2:-1]):
        if '\n' in col_name:
            col_name = col_name.replace('\n', '\n\t\t')
        print('\t', f"{i + 1}. {col_name}")
    print('\n')


def main():
    global kb
    dataset = pandas.read_csv('datasets/rdr_dm5_dataset.csv')
    original_columns = list(dataset.columns)
    rename_dict = {original_columns[1]: 'age_group'}
    for i, name in enumerate(original_columns[2:-1]):
        rename_dict[name] = f'S{i + 1}'
    # print(rename_dict)
    dataset.rename(columns=rename_dict, inplace=True)
    features = list(dataset.columns)
    # print(features)
    initialise_output_path(features)
    if os.path.exists(kb_file_name):
        load_kb()
        Rule.rule_no = kb.rules[-1].rule_no
    else:
        kb = KnowledgeBase(features)

    no_of_rows = dataset.shape[0]
    dataset['conclusion'] = ""
    # dataset['rules_evaluated'] = ""
    # dataset['rules_fired'] = ""
    kb.printRules()
    print_original_columns('List of Symptoms(S) corresponding to the table below:', original_columns)
    itr = 0
    evaluation = None
    while itr < no_of_rows:
        case = dataset.iloc[itr]
        try:
            evaluation = kb.eval_case(list(case))
        except ValueError:
            load_kb('saved_kb_bkp.kb')
        # print(case.to_frame().T.to_string())
        # print(f"{itr}. Evaluation:", evaluation)

        if not evaluation:
            print(dataset.head(itr + 1).to_string())
            add_rule(case)
            kb.printRules()
            print_original_columns('List of Symptoms(S) corresponding to the table below:', original_columns)
            continue
        if case['target'] != evaluation[0]:
            dataset.loc[itr, 'conclusion'] = evaluation[0]
            print(dataset.head(itr + 1).to_string())
            #dataset.loc[itr, 'rules_evaluated'] = "->".join(map(str, evaluation[2]))
            #dataset.loc[itr, 'rules_fired'] = "->".join(map(str, evaluation[3]))
            case = dataset.iloc[itr]
            add_rule(case, evaluation[1])
            kb.printRules()
            print_original_columns('List of Symptoms(S) corresponding to the table below:', original_columns)
            continue
        dataset.loc[itr, 'conclusion'] = evaluation[0]
        # dataset.loc[itr, 'rules_evaluated'] = "->".join(map(str, evaluation[2]))
        # dataset.loc[itr, 'rules_fired'] = "->".join(map(str, evaluation[3]))
        append_to_output(list(dataset.iloc[itr]))
        itr += 1

    # print_original_columns('List of Symptoms corresponding to the table below:', original_columns)
    print(dataset.to_string())


if __name__ == "__main__":
    main()
