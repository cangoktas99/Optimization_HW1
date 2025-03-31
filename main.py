from parsing_eachCategory import *
from classDefinition import LPProblem

def main():
    clear()
    history = hello_screen()
    valid_inputs = {}

    for parse_type, parse_string in parse_types_promptStrings.items():
        if parse_type in ["Constraints", "Variable Types (Sign)"]:
            input_func = {
                "Constraints": parse_constraints,
                "Variable Types (Sign)": parse_varTypes,
            }[parse_type]
            if "Objective Function" not in valid_inputs:
                raise ValueError(f"Objective function must be parsed before {parse_type.lower()}.")
            var_list = [f"y{i + 1}" for i in range(len(valid_inputs["Objective Function"]))]
            valid_inputString, valid_input = input_func(var_list, history)
            history.append(parse_string + valid_inputString + "\n\n")
            valid_inputs[parse_type] = valid_input
            display_history(history)
            continue
        else:
            input_func = {
                "Problem Type": parse_problemType,
                "Objective Function": parse_objectiveFunction,
            }[parse_type]
            while True:
                prompt = parse_string
                display_history(history, prompt)
                usr_input = input().strip()
                try:
                    valid_inputString, valid_input = input_func(usr_input)
                    history.append(prompt + valid_inputString + "\n\n")
                    valid_inputs[parse_type] = valid_input
                    break
                except ValueError as e:
                    if not check_wrong_expression(e):
                        break
    problemType = valid_inputs["Problem Type"]
    objCoeffs = valid_inputs["Objective Function"]
    constraints = valid_inputs["Constraints"]
    varTypes = valid_inputs["Variable Types (Sign)"]

    print("\n\n")

    problem = LPProblem(problemType, objCoeffs, constraints, varTypes)
    print(problem)


if __name__ == "__main__":
    main()