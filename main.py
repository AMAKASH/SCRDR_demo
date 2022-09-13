from KnowledgeBase import Rule, KnowledgeBase
import pandas
import pickle
import os

# global kb_file_name, output_path, kb
# kb_file_name = "saved_kb_final.kb"
kb_file_name = "saved_kb.kb"
output_path = 'conclusion/conclusions.csv'


def load_kb(path=None):
    global kb
    if not path:
        path = kb_file_name
    with open(path, 'rb') as file:
        kb = pickle.load(file)
        Rule.rule_no = kb.rules[-1].rule_no


def initialise_output_path(features):
    with open(output_path, 'w') as f:
        to_append = str(f"{','.join(features)}, conclusion, rules Evaluated, rules Fired\n")
        f.write(to_append)


def print_original_columns(msg, col):
    print(msg)
    age_group = col[1].replace('\n', '\n\t\t')
    print('\t', f"=> {age_group}")
    for i, col_name in enumerate(col[2:-1]):
        if '\n' in col_name:
            col_name = col_name.replace('\n', '\n\t\t')
        print('\t', f"{i + 1}. {col_name}")
    print('\n')


def append_to_output(case):
    with open(output_path, 'a') as f:
        to_append = str(f"{','.join(map(str, case))}\n")
        f.write(to_append)


def main():
    global kb
    dataset = pandas.read_csv('datasets/test_case.csv')
    original_columns = list(dataset.columns)
    rename_dict = {original_columns[1]: 'age_group'}
    for i, name in enumerate(original_columns[2:-1]):
        rename_dict[name] = f'symptom{i + 1}'
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
    dataset['rules_evaluated'] = ""
    dataset['rules_fired'] = ""
    kb.printRules()
    print_original_columns('List of Symptoms corresponding to the table below:', original_columns)
    itr = 0
    evaluation = None
    while itr < no_of_rows:
        case = dataset.iloc[itr]
        try:
            evaluation = kb.eval_case(list(case))
        except ValueError:
            load_kb('saved_kb_bkp.kb')
        # print(case)
        # print(f"{itr}. Evaluation:", evaluation)
        dataset.loc[itr, 'conclusion'] = evaluation[0]
        dataset.loc[itr, 'rules_evaluated'] = "->".join(map(str, evaluation[2]))
        dataset.loc[itr, 'rules_fired'] = "->".join(map(str, evaluation[3]))
        append_to_output(list(dataset.iloc[itr]))
        itr += 1

    # print_original_columns('List of Symptoms corresponding to the table below:', original_columns)
    print(dataset.to_string())


if __name__ == "__main__":
    main()
