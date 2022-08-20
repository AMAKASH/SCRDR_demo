from KnowledgeBase import Rule, KnowledgeBase
import rule_builder
import pandas


def main():
    kb = rule_builder.get_kb()
    kb.printRules()
    print("Evaluating Cases: Result In order: (Conclusion, rule, [Evaluated Rules], [Fired Rules])........\n")
    df = pandas.read_csv('animal_dataset.csv')

    for i in range(df.shape[0]):
        row = list(df.loc[i])
        print(i + 1, end=". ")
        print(row, end="   --->")
        evaluation = kb.eval_case(row)
        print(evaluation)
        if not evaluation:
            print("No Rule Fired For The above Case")
            break
        if row[-1] != evaluation[0]:
            print("Target not Matched")
            break


if __name__ == "__main__":
    main()
