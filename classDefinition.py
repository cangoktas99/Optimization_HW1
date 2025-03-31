class LPProblem:
    def __init__(self, problem_type, obj_coeffs, constraints, var_types):
        # Validate problem_type
        if problem_type not in ['max', 'min']:
            raise ValueError("problem_type must be 'max' or 'min'")

        # Ensure the number of objective coefficients matches the number of variable types
        if len(obj_coeffs) != len(var_types):
            raise ValueError("Length of obj_coeffs must match length of var_types")
        self.n_vars = len(obj_coeffs)

        # Validate variable types
        valid_var_types = ['non-positive', 'free', 'non-negative']
        for var_type in var_types:
            if var_type not in valid_var_types:
                raise ValueError(f"Invalid var_type: {var_type}")

        # Validate constraints
        valid_inequalities = ['<=', '>=', '=']
        for constraint in constraints:
            if len(constraint) != 3:
                raise ValueError("Each constraint must be a tuple of (coeffs, inequality, rhs)")
            coeffs, inequality, rhs = constraint
            if len(coeffs) != self.n_vars:
                raise ValueError("Constraint coefficients must match the number of variables")
            if inequality not in valid_inequalities:
                raise ValueError(f"Invalid inequality: {inequality}")

        # Store the attributes
        self.problem_type = problem_type
        self.obj_coeffs = obj_coeffs
        self.constraints = constraints
        self.var_types = var_types
        self.var_names = [f'y{i+1}' for i in range(self.n_vars)]

    def __str__(self):
        # Initialize the string representation
        s = f"So, your optimization problem is: \n"
        s += "Objective Function:\n"

        # Construct the objective function string with proper sign handling
        obj_terms = [f"{c}*{v}" if c >= 0 else f"- {-c}*{v}"
                     for c, v in zip(self.obj_coeffs, self.var_names)]
        obj_str = " + ".join(obj_terms).replace(" + -", " - ")
        s += f"{'Maximize z =' if self.problem_type == 'max' else 'Minimize f ='} {obj_str}\n"

        # Add constraints
        s += "Subject to:\n"
        for constraint in self.constraints:
            coeffs, inequality, rhs = constraint
            constraint_terms = [f"{c}*{v}" if c >= 0 else f"- {-c}*{v}"
                               for c, v in zip(coeffs, self.var_names)]
            constraint_str = " + ".join(constraint_terms).replace(" + -", " - ")
            s += f"{constraint_str} {inequality} {rhs}\n"

        # Add variable types
        s += "Variable Types:\n"
        for v, t in zip(self.var_names, self.var_types):
            if t == 'free':
                means_str = "is unrestricted in sign"
            elif t == 'non-negative':
                means_str = ">= 0"
            else:
                means_str = "<= 0"
            s += f"{v} {means_str}\n"

        return s