import os
import sys

if sys.platform == 'win32':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

def hello_screen():
    l1 = f"This program is designed for the Homework 1 of the course Optimization Techniques in Eng"
    l2 = f"given by Prof. Dr. Melike Nikbay. Student ID: 511231173. The program is aimed to:"
    l3 = f"\t- Define a linear optimization problem, directly taking inputs from the command prompt"
    l4 = f"\t- Transform it into the standard form, explaining step by step"
    l5 = f"\t- Solve with the simplex algorithm, by using tableau's"
    l6 = f"Directly using in a terminal is highly recommended for the command prompt interactions!\n\n"

    history = [l1, l2, l3, l4, l5, l6]
    return history

def display_history(history, current_prompt=""):
    clear()
    for line in history:
        print(line)
    if current_prompt:
        print(current_prompt, end='', flush=True)

def check_wrong_expression(error_message):
    wrong_key = False
    while True:
        if not wrong_key:
            choice = input(f"{error_message}. Would you like to try again? [Y/N]: ").strip().lower()
        else:
            choice = input(f"Only [Y/N] keys are available at this point. Would you like to try again? [Y/N]: ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print(f"\nOkay then, see ya!")
            exit(0)
        else:
            wrong_key = True
            continue

def if_not_exist(input_str):
    if not input_str or not input_str.strip():
        raise ValueError(f"You did not enter anything..")


parse_types_promptStrings = {
    "Problem Type":
        f"Enter the type of the problem, this entry can be either 'max' or 'min'."
        f"\nType of the problem:\n\t",
    "Objective Function":
        f"Enter the objective function, this entry can be in a form like 'c1 * y1 + c2 * y2 + ...'\n"
        f", where c1, c2, ... coefficients should be doubles and y1, y2, ... should stay as it is.\n"
        f"Proper Examples: \ty1 + 2*y2 - 4*y3,\t1.2* y1 - 0.3*y2 +1 * y3\n"
        f"Improper Example:\t1.3y1- 0 * y2 + 3.6 * y_3 -> * must be used, 0 coefficient is invalid\n"
        f"and variable cannot be used with an underscore (_)."
        f"\nObjective Function:\n\t",
    "Constraints":
        f"Enter the constraints as much as you want, you can use the same form as in the objective\n"
        f"function. You are not supposed to enter the variables with coefficient zero (0). If you\n"
        f"are done entering constraints, just type 'done' and press enter."
        f"\nConstraints:\n\t",
    "Variable Types (Sign)":
        f"Enter the variable types , only 3 valid input is presented: 'non-positive', 'free', or \n"
        f"'non-negative'. The prompt will automatically ask you for every variable you entered in\n"
        f"the objective function."
        f"\nVariable Types:\n\t",
}


"""
def conversion_to_lp_form(problem):
    leq_indices = [i for i, rel in enumerate(problem.relations) if rel == '<=']
    geq_indices = [i for i, rel in enumerate(problem.relations) if rel == '>=']
    eq_indices = [i for i, rel in enumerate(problem.relations) if rel == '=']
    m_leq = len(leq_indices)
    m_geq = len(geq_indices)
    m_eq = len(eq_indices)

    # Number of structural variables (original variables adjusted for free variables)
    n_structural = sum(1 if var_type == 'nonnegative' else 2 for var_type in problem.var_types)

    new_A = []
    for i in range(problem.num_constraints):
        structural_coeffs = []
        for j in range(problem.num_n):
            if problem.var_types[j] == 'nonnegative':
                structural_coeffs.append(problem.matrixA[i][j])
            elif problem.var_types[j] == 'free':
                structural_coeffs.append(problem.matrixA[i][j]) # x_j+
                structural_coeffs.append(-problem.matrixA[i][j]) # x_j-

        row_i = structural_coeffs + [0] * (m_leq + 2 * m_geq + m_eq)

        if problem.relations[i] == '<=':
            p = leq_indices.index(i)
            row_i[n_structural + p] = 1 # slack variable
        elif problem.relations[i] == '>=':
            p = geq_indices.index(i)
            row_i[n_structural + m_leq + p] = -1 # surplus variable
            row_i[n_structural + m_leq + m_geq + p] = 1  # artificial variable
        elif problem.relations[i] == '=':
            p = eq_indices.index(i)
            row_i[n_structural + m_leq + 2 * m_geq + p] = 1 # artificial variable
        new_A.append(row_i)

    new_b = problem.vectorB[:]

    c = [-coeff for coeff in problem.c_i] if problem.problem_type == 'max' else problem.c_i[:]
    new_c = []

    for j in range(problem.num_n):
        if problem.var_types[j] == 'nonnegative':
            new_c.append(c[j])
        elif problem.var_types[j] == 'free':
            new_c.append(c[j])
            new_c.append(-c[j])
    new_c += [0] * (m_leq + 2 * m_geq + m_eq)

    artificial_start = n_structural + m_leq + m_geq
    artificial_end_geq = artificial_start + m_geq
    artificial_end = artificial_end_geq + m_eq
    artificial_indices = list(range(artificial_start, artificial_end_geq)) + list(range(artificial_end_geq, artificial_end))

    return new_A, new_b, new_c, artificial_indices
"""