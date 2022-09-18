class Rule:
    rule_no = 0

    def __init__(self, conditions: dict, cornerstone: list, conclusion: str, if_false=None, if_true=None,
                 is_refinement=False, parent: int = None) -> None:
        self.parent = parent
        self.is_refinement = is_refinement
        self.rule_no = Rule.rule_no + 1
        self.conditions = conditions
        self.cornerstone = cornerstone
        self.conclusion = conclusion
        self.if_true = if_true
        self.if_false = if_false
        Rule.rule_no += 1

    def __repr__(self):
        tobe_returned = f"Rule No: {self.rule_no}, conditions: {self.conditions}, \n\t\tconclusion: {self.conclusion},"
        if self.is_refinement:
            tobe_returned += f" parent: {self.parent},"
        # tobe_returned += f"\n\t cornerstone: {self.cornerstone}"
        return tobe_returned


class KnowledgeBase:
    def __init__(self, features: list, rule: Rule = None) -> None:
        self.rules = []
        if rule:
            self.rules = [rule]
        self.last_major_rule = rule
        self.features = features

    def add_rule(self, rule: Rule):
        if rule.is_refinement:
            parent = self.get_rule(rule.parent)
            if parent.if_true is None:
                parent.if_true = rule
            else:
                ref_rule = parent.if_true
                while ref_rule.if_false:
                    ref_rule = ref_rule.if_false
                ref_rule.if_false = rule
        else:
            if self.last_major_rule:
                self.last_major_rule.if_false = rule
            self.last_major_rule = rule

        self.rules.append(rule)

    def get_rule(self, rule_no) -> Rule | bool:
        for r in self.rules:
            if r.rule_no == rule_no:
                return r
        return False

    def eval_case(self, case: list) -> tuple | bool:
        rules_fired = []
        rules_evaluated = []
        if len(self.rules) <= 0:
            current_rule = None
        else:
            current_rule = self.rules[0]
        current_conclusion = None
        conclusion_rule = 0
        while current_rule:
            rules_evaluated.append(current_rule.rule_no)
            satisfied = True
            condition_keys = current_rule.conditions.keys()
            for key in condition_keys:
                feature_index = self.features.index(key)
                op, val = current_rule.conditions[key]
                if not eval(f"{case[feature_index]} {op} {val}"):
                    # print(f"{case[feature_index]} {op} {val}")
                    satisfied = False
                    break
            if satisfied:
                rules_fired.append(current_rule.rule_no)
                current_conclusion = current_rule.conclusion
                conclusion_rule = current_rule.rule_no
                current_rule = current_rule.if_true
            else:
                # print(current_rule.if_false)
                current_rule = current_rule.if_false

        if current_conclusion:
            return current_conclusion, conclusion_rule, rules_evaluated, rules_fired
        else:
            return False

    def printRules(self):
        print("The following rules are available for this kb:")
        for i, r in enumerate(self.rules):
            print(f"{i + 1}. {r}")
        print("\n            -End of Rules- \n\n")


