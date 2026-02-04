import sys
from dask_core.expression_manager import ExpressionManager
from time import sleep
from io_utils.file_handler import FileHandler
from dask_core.parse_tree import ParseTree
from features.cost_analysis import CostAnalyser
import re
from features.differentiation import differentiate, UnsupportedOperatorError
from dask_core.evaluator import Evaluator
from dask_core.history import History


class Menu:
    def __init__(self):
        self.option_display = ""
        self.option_display += "Please select your choice ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):\n"
        self.option_display += "\t1. Add/Modify DASK expression\n"
        self.option_display += "\t2. Display current DASK expression\n"
        self.option_display += "\t3. Evaluate a single DASK variable\n"
        self.option_display += "\t4. Read DASK expression from file\n"
        self.option_display += "\t5. Sort DASK expressions\n"
        self.option_display += "\t6. Optimise Expressions and Cost Anaylsis (Aden)\n"
        self.option_display += "\t7. Symbolic Differentiation (Aden)\n"
        self.option_display += "\t8. Expression History (Zuhao)\n"
        self.option_display += "\t9. Evaluation without parantheses (Zuhao)\n"
        self.option_display += "\t10. Exit\n"
        self.option_display += "Enter choice: "

        self.EM = ExpressionManager()
        self.animation_delay = 0.5
        self.history = ''

        self.title_screen = '''
*********************************************************
* ST1507 DSAA: DASK Expression Evaluator                *
*-------------------------------------------------------*
*                                                       *
*  - Done by: Mo Zuhao(2415646) & Aden Cheah(24151815)  *
*  - Class DAAA/2A/21                                   *
*                                                       *
*********************************************************
              

'''

    

    def run_menu(self):
        print(self.title_screen)
        while True:
            user_choice = input(self.option_display).strip()
            while user_choice not in ['1','2','3','4','5','6','7','8','9','10']:
                user_choice = input(f'\n*PLEASE ENTER A VALID NUMBER*\n{self.option_display}')
            
            match user_choice:
                case '1':
                    self.add_modify()
                    self._wait_for_continue()
                case '2':
                    self.display_current()
                    self._wait_for_continue()
                case '3':
                    self.display_n_evaluate_single()
                    self._wait_for_continue()
                case '4':
                    self.read_from_file()
                    self.display_current()
                    self._wait_for_continue()
                case '5':
                    self.sortexpressions()
                    self._wait_for_continue()
                    pass
                case '6':
                    self.optimise_cost()
                    self._wait_for_continue()
                case '7':
                    self.differentiate_expression()
                    self._wait_for_continue()
                case '8':
                    self.loadhistory()
                    self._wait_for_continue
                case '9':
                    self.evaluatenoparanthesis()
                    self._wait_for_continue()
                case '10':
                    break
        print('\nBye, thanks for using ST1507 DSAA DASK Expression Evaluator')
    
    def _wait_for_continue(self):
        input("\nPress enter key, to continue....")
        self.EM.evaluate_all()

    def add_modify(self):
        expression = input('Enter the DASK expression you want to add/modify: \nFor example, a=(1+2)\n')
        message, result,name,expr = self.EM.validate_expression(expression)
        while True:
            if result == False:
                expression = input(f'\n{message}: ')
                message,result,name,expr = self.EM.validate_expression(expression)
            elif result == True:
                try:
                    # Parse once to catch constant division by zero before storing
                    self.EM.parser.parse(expr)
                except ZeroDivisionError:
                    expression = input("\nDivision by zero detected. Please enter a new expression: ")
                    message, result, name, expr = self.EM.validate_expression(expression)
                    continue
                self.EM.add_expression(name, expr)
                break

    def display_current(self):
        print("\nCURRENT EXPRESSIONS:\n********************")
        for name in sorted(self.EM.expressions.keys()):
            expression = self.EM.expressions[name]
            print(expression)
        print('')

        sleep(0.5)

    def display_n_evaluate_single(self):
        while True: 
            var_name = input("Please enter the variable you want to evaluate:\n")
            if len(self.EM.expressions) < 1:
                print("There are currently no variables in this session.")
                return
            if var_name not in self.EM.expressions.keys():
                print("Variable not found!", end='\n\n')
                sleep(0.5)
                continue
            else:
                print('')
                break
        expr = self.EM.expressions[var_name]
        print('Expression Tree:')
        expr_tree = expr.parse_tree
        expr_tree.printInOrder()
        expr_value = expr.evaluate(context=self.EM.expressions)
        print(f'Value for variable "{var_name}" is {expr_value}', end='\n\n')

    def read_from_file(self):
        file_handler = FileHandler()
        file_contents = file_handler.read_file()
        file_expressions = file_contents.split('\n')
        
        validity = True
        # Use a list to keep every version in order
        parsed_expressions = [] 

        for expression in file_expressions:
            if not expression.strip(): continue # Skip empty lines
            
            (err_msg, is_valid, name, expr) = self.EM.validate_expression(expression)
            
            if not is_valid:
                print(err_msg)
                validity = False
                break
            
            try:
                self.EM.parser.parse(expr)
                # Store as a pair so we don't lose duplicates
                parsed_expressions.append((name, expr)) 
            except ZeroDivisionError:
                print(f"Division by zero in: {expression}")
                validity = False
                break

        if not validity:
            print('Invalid expression in file. Aborting load.')
            return

        # Now add_expression will trigger the history logic for EVERY line
        for name, expr in parsed_expressions:
            self.EM.add_expression(name, expr)

        self.EM.evaluate_all()
        # ... rest of your code


    def sortexpressions(self):
        if len(self.EM.expressions) < 1:
            print("There are currently no variables in this session.")
            return
        output = ''
        grouped = {}
        for expr in self.EM.expressions.values():
            grouped.setdefault(expr.value, []).append(expr)

        values = [v for v in grouped.keys() if v is not None]
        values = sorted(values, reverse=True)
        if None in grouped:
            values.append(None)

        for value in values:
            output += f'*** Expressions with value=> {value}\n'
            for expr in sorted(grouped[value], key=lambda e: e.name):
                output += f'{expr.name}={expr.expression}\n'
            output += '\n'
        file_handler = FileHandler()
        file_handler.write_file(output)
        print(f'\n>>> Sorting of DASK expressions completed!')

    def request_expression(self) -> str:
        """
        Get the name of an expression from user
        
        :return: Name of variable
        :rtype: str
        """
        if len(self.EM.expressions) < 1:
            print("There are currently no variables in this session.")
            return ""
        while True:
            var_name = input("Please enter an expression: ").strip()
            if var_name not in self.EM.expressions.keys():
                print('Expression does not exist! Please try again.\n')     
                sleep(0.5)
            else:
                return var_name

    def optimise_cost(self):
        var_name = self.request_expression()
        if not var_name:
            return
        self.EM.optimise_expression(var_name)
        print(f"Optimising {var_name}...\n")
        sleep(0.5)
        self.print_cost_analysis_report(var_name)
        
    
    def print_cost_analysis_report(self, var_name: str = None):
        if var_name is None:
            while True:
                var_name = input("Please enter a variable to view its cost analysis:\n")
                if var_name not in self.EM.expressions.keys():
                    print("Variable does not exist! Please try again.\n")
                    continue
                break
        var = self.EM.expressions[var_name]
        cost_analyser = CostAnalyser(var.parse_tree)
        statistics = cost_analyser.statistics

        metrics = [
            ("Total nodes", "total_nodes"),
            ("Operator nodes", "operator_nodes"),
            ("Leaf nodes", "leaf_nodes"),
            ("Tree height", "tree_height"),
            ("Weighted op cost", "weighted_op_cost"),
        ]

        def saved_percent(original, optimised):
            if original == 0:
                return 0.0
            return (original - optimised) / original * 100

        def bar(percent, width=20):
            filled = int(round((percent / 100) * width))
            filled = max(0, min(width, filled))
            return "|" + ("#" * filled) + ("-" * (width - filled)) + "|"

        lines = []
        lines.append("=" * 60)
        lines.append("  COST ANALYSIS REPORT  (Optimisation Impact)")
        lines.append("-" * 60)
        lines.append(f"  Variable   : {var_name}")
        lines.append("  Status     : Optimised successfully")
        lines.append("=" * 60)
        lines.append("")
        lines.append("METRICS (Original vs Optimised)")
        lines.append("-" * 75)
        lines.append("Metric                 Original   Optimised   Change        Saved%   Visual")
        lines.append("-" * 75)

        biggest_label = ""
        biggest_saved = -1.0

        for label, key in metrics:
            original = statistics.get(f"original_{key}") or 0
            optimised = statistics.get(f"optimised_{key}") or 0
            change = optimised - original
            saved = saved_percent(original, optimised)
            if saved > biggest_saved:
                biggest_saved = saved
                biggest_label = label
            lines.append(
                f"{label:<22} {original:>9} {optimised:>11} {change:>9}   {saved:>6.1f}%   {bar(saved)}"
            )

        lines.append("-" * 75)
        # print trees here
        lines.append("")
        lines.append("SUMMARY")
        lines.append("-" * 60)
        lines.append(f"* Biggest reduction : {biggest_label} ({biggest_saved:.1f}%)")
        total_orig = statistics.get("original_total_nodes", 0)
        total_opt = statistics.get("optimised_total_nodes", 0)
        cost_orig = statistics.get("original_weighted_op_cost", 0)
        cost_opt = statistics.get("optimised_weighted_op_cost", 0)
        lines.append(
            f"* Overall saving    : {saved_percent(total_orig, total_opt):.1f}% fewer nodes, "
            f"{saved_percent(cost_orig, cost_opt):.1f}% less op-cost"
        )
        lines.append("=" * 60)
        lines.append("Legend: Visual bar shows % saved (more filled = more reduction)")
        print("\n".join(lines))

    def differentiate_expression(self):
        var_name = self.request_expression()
        if not var_name:
            return
        expression = self.EM.expressions[var_name]
        while True:
            wrt = input("Please enter the variable of differentation (w.r.t.): ").strip()
            if not re.fullmatch(r"[a-zA-Z_]+", wrt):
                print("Invalid variable name. Please try again.\n")
                continue
            if wrt not in self.EM.expressions:
                print("Variable does not exist! Please try again.\n")
                continue
            wrt_expression = self.EM.expressions[wrt]
            count = expression.parse_tree.count_x_variable(wrt)
            if count == 0:
                print("0")
                return

            # Differentiate
            try:
                root = expression.parse_tree.optimised_root
                if root is None:
                    root = expression.parse_tree.original_root
                result: ParseTree | None = differentiate(root, wrt)
                if result is None:
                    print("Differentiation could not be completed for this expression.\n")
                    return
                break
            except UnsupportedOperatorError:
                print("Unsupported operator for differentiation. Please enter a different variable.\n")
                continue
            except ValueError:
                print("A non-leaf in the ParseTree is not an operator. Please enter a different variable.\n")
                continue
        self._loading_animation("Differentiating")

        # Store differentiated expression as a new variable
        expr_str = result.to_expression("optimised")
        if not expr_str:
            print("Differentiation produced an empty expression.\n")
            return
        new_name = f"d{var_name}_d{wrt}"
        self.EM.add_expression(new_name, expr_str)
        print(f"Stored derivative as {new_name}={expr_str}")
        self.EM.evaluate_all()


        self._loading_animation("Optimising")
        print('Success!')
        sleep(0.5)
        print()
        # printing portion
        line = "="*60
        dash = '-'*60
        print(line)
        print("SYMBOLIC DIFFERENTIATION RESULTS")
        print(dash)
        print(f"Original Variable            : {var_name}")
        print(f"Differentiated w.r.t.        : {wrt}")
        print(f"Status                       : Completed & Optimised")
        print(line)
        print()

        print("Dependent Variable's Optimised Expression (Parse Tree)")
        print(dash)
        expression.parse_tree.display_optimised_root()
        print()
        print(expression.expression)
        print(dash)
        print(f"Differentiated Variable: {new_name} (Parse Tree before Optimisation)")
        print(dash)
        result.printInOrder()
        print()
        print(result.to_expression('original'))
        print(dash)
        print(f"Differentiated Variable: {new_name} (Parse Tree after Optimisation)")
        print(dash)
        result.display_optimised_root()
        print()
        print(result.to_expression('optimised'))
        print(line)
        
    def _loading_animation(self, label: str):
        frames = ["", ".", "..", "..."]
        i = 0
        while i < 9:
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r\033[K{label}{frame}")
            sys.stdout.flush()

            i += 1
            sleep(self.animation_delay)
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
        print()
    
    
    def loadhistory(self):
        history = History(self.EM.history)
        name, expr = history.printhistory(history.history)
        if name == '' and expr == '':
            return
        else:
            self.EM.add_expression(name,expr)
            self.EM.evaluate_all()
            return


    def evaluatenoparanthesis(self):
        expression = input('Enter the DASK expression you wish to evaluate: \nFor example, a=1+2\n')
        message, result,name,expr = self.EM.validation(expression)
        while True:
            if result == False:
                expression = input(f'\n{message}: ')
                message,result,name,expr = self.EM.validation(expression)
            elif result == True:
                try:
                    tree = self.EM.parser.parses(expr)
                    if type(tree) == int:
                        print(f'"{expression} ==> {expr}')
                    print()
                except ZeroDivisionError:
                    expression = input("\nDivision by zero detected. Please enter a new expression: ")
                    message, result, name, expr = self.EM.validation(expression)
                    continue
                evaluator = Evaluator()
                result = tree.evaluate(evaluator, context=self.EM.expressions)
                if type(result) == int:
                    result = round(result,3)
                print(f'"{expression}" ==> {name}={result}\n')
                break
