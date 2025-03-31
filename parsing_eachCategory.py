from parsing_functionDefinitions import *
import re

def parse_problemType(input_str: str):
    if_not_exist(input_str)

    list_str = input_str.strip().split()

    if len(list_str) != 1:
        raise ValueError("Wrong Entry.")
    else:
        only_word = list_str[0].lower()
        if only_word not in ["max", "min"]:
            raise ValueError("You can only enter values: ['max', 'min']..")
        else:
            problemType = only_word
            return problemType, problemType

def parse_objectiveFunction(input_str: str):
    """
    Solution

The goal is to parse an objective function string (e.g., "y1 + 2y2 - 4y3") into a list of coefficients where the variables are expected to be "y1" to "yn" consecutively, without gaps or duplicates, and return the coefficients in that order as a list. If the input violates these rules, a ValueError will be raised with an appropriate message.
Approach

    Validate Input:
        Ensure the input string is not empty or just whitespace.
    Preprocess the String:
        Remove all whitespace for consistent parsing.
        Add implicit coefficients (e.g., "1*" before "y1" or "-1*" before "-y2").
    Split into Terms:
        Divide the string into individual terms based on "+" and "-" operators, preserving the operators with each term.
    Parse Each Term:
        Extract the sign, coefficient, and variable from each term.
        Validate that:
            The coefficient is a non-zero number.
            The variable is exactly "y" followed by a positive integer (e.g., "y1", "y2").
            The integer index is at least 1 and has no leading zeros.
    Collect Coefficients:
        Use a dictionary to map variable indices (e.g., 1 for "y1") to their coefficients, checking for duplicates.
        After parsing, ensure the variables are consecutive from "y1" to "yn" (e.g., if "y3" is present, "y1" and "y2" must also be).
    Return the List:
        If all checks pass, return a list of coefficients in the order from "y1" to "yn".
    """
    if_not_exist(input_str)

    """
        Parse an objective function string into a list of coefficients for variables y1 to yn.

        Parameters:
        - input_str (str): The objective function, e.g., "0.3 * y1" or "y1 + 2*y2 - 4*y3"

        Returns:
        - list: Coefficients in order from y1 to yn.

        Raises:
        - ValueError: If the input is invalid or variables are not y1 to yn consecutively.
        """

    # Remove all whitespace
    input_str = input_str.replace(" ", "")

    # Split into terms based on '+' and '-' (keeping operators with terms)
    terms = re.split(r'(?=[+-])', input_str)
    if terms[0] == '':
        terms.pop(0)  # Remove empty first element if present

    # Dictionary to store index:coefficient mappings
    obj_dict = {}

    for term in terms:
        if not term:
            continue

        # Determine sign
        if term[0] == '-':
            sign = -1
            term = term[1:]
        elif term[0] == '+':
            sign = 1
            term = term[1:]
        else:
            sign = 1  # First term without a sign is positive

        # Parse coefficient and variable
        if '*' in term:
            parts = term.split('*', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid term format: {term}")
            coeff_str, var = parts
        else:
            # Implicit coefficient of 1
            coeff_str = '1'
            var = term

        # Validate coefficient
        try:
            coeff = float(coeff_str)
            if coeff == 0:
                raise ValueError(f"Zero coefficient is not allowed in term: {term}")
        except ValueError:
            raise ValueError(f"Invalid coefficient in term: {term}")

        # Validate variable name
        match = re.fullmatch(r"y(\d+)", var)
        if not match:
            raise ValueError(f"Invalid variable name: {var}. Must be y1, y2, etc.")

        index_str = match.group(1)
        if index_str.startswith('0') and index_str != '0':
            raise ValueError(f"Variable name cannot have leading zeros: {var}")

        try:
            index = int(index_str)
            if index < 1:
                raise ValueError(f"Variable index must be at least 1: {var}")
        except ValueError:
            raise ValueError(f"Invalid variable index: {var}")

        # Check for duplicate variables
        if index in obj_dict:
            raise ValueError(f"Duplicate variable: y{index}")

        # Store coefficient with applied sign
        obj_dict[index] = coeff * sign

    # Ensure there are terms to process
    if not obj_dict:
        raise ValueError("No valid terms found in the objective function.")

    # Verify variables start with y1 and are consecutive
    indices = set(obj_dict.keys())
    min_index = min(indices)
    if min_index != 1:
        raise ValueError("Variables must start with y1.")
    max_index = max(indices)
    if indices != set(range(1, max_index + 1)):
        raise ValueError("Variables must be y1 to yn without gaps or duplicates.")

    # Create the ordered list of coefficients
    coeff_list = [obj_dict[i] for i in range(1, max_index + 1)]

    # Generate the string representation
    terms = []
    for i, coeff in enumerate(coeff_list, start=1):
        abs_coeff = abs(coeff)
        coeff_str = str(int(abs_coeff)) if abs_coeff.is_integer() else str(abs_coeff)
        var = f"y{i}"
        if coeff > 0:
            terms.append(f"{coeff_str}*{var}")
        else:
            terms.append(f"-{coeff_str}*{var}")

    # Construct the final string
    temp_str = " + ".join(terms)
    obj_str = temp_str.replace(" + -", " - ")

    return obj_str, coeff_list

def parse_singleConstraint(constraint_str, var_list):
    """
    Parse a single constraint string into coefficients, inequality type, and RHS value.

    Parameters:
    - constraint_str (str): E.g., "2*y1 + 3*y3 <= 5"
    - var_list (list): List of variables from objective, e.g., ['y1', 'y2', 'y3']

    Returns:
    - tuple: (coeff_list, inequality, rhs_value)
             - coeff_list: Coefficients in order of var_list (0 if variable absent)
             - inequality: One of '<=', '>=', '='
             - rhs_value: Float value of the right-hand side

    Raises:
    - ValueError: If the constraint is malformed
    """
    if not constraint_str or not constraint_str.strip():
        raise ValueError("Constraint cannot be empty.")

    # Find and split on inequality sign
    match = re.search(r'(<=|>=|=)', constraint_str)
    if not match:
        raise ValueError("No inequality sign found in constraint (use <=, >=, or =).")
    inequality = match.group(0)
    left, rhs = constraint_str.split(inequality, 1)
    left = left.strip()
    rhs = rhs.strip()

    # Parse RHS
    try:
        rhs_value = float(rhs)
    except ValueError:
        raise ValueError(f"Invalid RHS value '{rhs}': must be a number.")

    # Parse left side (similar to parse_objectiveFunction but allows missing variables)
    left = left.replace(" ", "")
    terms = re.split(r'(?=[+-])', left)
    if terms[0] == '':
        terms.pop(0)  # Remove empty first term if present

    obj_dict = {}  # Maps variable index (1-based) to coefficient
    for term in terms:
        if not term:
            continue
        sign = 1 if term[0] not in ['+', '-'] else (-1 if term[0] == '-' else 1)
        term = term.lstrip('+-')
        if '*' in term:
            parts = term.split('*', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid term format: {term}")
            coeff_str, var = parts
        else:
            coeff_str = '1'
            var = term

        # Parse coefficient
        try:
            coeff = float(coeff_str)
            if coeff == 0:
                raise ValueError(f"Zero coefficient is not allowed in term: {term}")
        except ValueError:
            raise ValueError(f"Invalid coefficient in term: {term}")

        # Parse variable
        match = re.fullmatch(r"y(\d+)", var)
        if not match:
            raise ValueError(f"Invalid variable name: {var}. Must be y1, y2, etc.")
        index_str = match.group(1)
        if index_str.startswith('0') and index_str != '0':
            raise ValueError(f"Variable name cannot have leading zeros: {var}")
        try:
            index = int(index_str)
            if index < 1 or index > len(var_list):
                raise ValueError(f"Variable index out of range: {var}")
        except ValueError:
            raise ValueError(f"Invalid variable index: {var}")
        if index in obj_dict:
            raise ValueError(f"Duplicate variable in constraint: y{index}")
        obj_dict[index] = coeff * sign

    # Build coefficient list, defaulting to 0 for missing variables
    coeff_list = [obj_dict.get(i, 0) for i in range(1, len(var_list) + 1)]
    return coeff_list, inequality, rhs_value

def parse_constraints(var_list, history):
    constraints = []
    constraint_strings = []
    prompt = parse_types_promptStrings["Constraints"]  # Access prompt directly or pass it
    while True:
        display_history(history, prompt)
        constraint_str = input().strip()
        if constraint_str.lower() == 'done':
            break
        try:
            coeffs, inequality, rhs = parse_singleConstraint(constraint_str, var_list)
            constraints.append((coeffs, inequality, rhs))
            constraint_strings.append(constraint_str)
        except ValueError as e:
            if not check_wrong_expression(e):
                break
    valid_inputString = "\n\t".join(constraint_strings)
    return valid_inputString, constraints

def parse_varTypes(var_list, history):
    """
    Parse variable types for each variable in var_list by prompting the user.

    Parameters:
    - var_list (list): List of variable names, e.g., ['y1', 'y2']
    - history (list): Command prompt history to display previous inputs
    - parse_string (str): The prompt string for "Variable Types (Sign)"

    Returns:
    - tuple: (valid_inputString, var_types)
             - valid_inputString: String for history, e.g., "y1: non-negative, y2: free"
             - var_types: List of variable types, e.g., ['non-negative', 'free']
    """
    allowed_types = ["non-positive", "free", "non-negative"]
    var_types = []

    for var in var_list:
        while True:
            try:
                # Construct the current prompt with types entered so far
                types_so_far = "\n".join([f"{v}: {t}" for v, t in zip(var_list[:len(var_types)], var_types)])
                current_prompt = parse_types_promptStrings["Variable Types (Sign)"]
                if types_so_far:
                    current_prompt += "\n" + types_so_far
                current_prompt += f"\nEnter type for {var}: "

                # Display history and get user input
                display_history(history, current_prompt)
                usr_input = input().strip().lower()

                # Validate the input
                if usr_input not in allowed_types:
                    raise ValueError(f"Invalid type '{usr_input}'. Please enter 'non-positive', 'free', or 'non-negative'.")

                # If valid, append the type and move to the next variable
                var_types.append(usr_input)
                break

            except ValueError as e:
                # Call check_wrong_expression with the error message
                if check_wrong_expression(str(e)):
                    continue  # Retry input for the current variable
                else:
                    break  # This line is technically unreachable due to exit(0) in check_wrong_expression

    # Create the string representation for history
    valid_inputString = "\n\t".join(f"{v}: {t}" for v, t in zip(var_list, var_types))
    #valid_inputString = ", ".join([f"{v}: {t}" for v, t in zip(var_list, var_types)])
    return valid_inputString, var_types