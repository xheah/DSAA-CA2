from dask_core.expression_manager import ExpressionManager
from time import sleep
from io_utils.file_handler import FileHandler
from dask_core.parse_tree import ParseTree
from features.cost_analysis import CostAnalyser
import re
from features.differentiation import differentiate, UnsupportedOperatorError


class Menu:
    def __init__(self):
        self.option_display = ""
        self.option_display += "Please select your choice ('1', '2', '3', '4', '5', '6'):\n"
        self.option_display += "\t1. Add/Modify DASK expression\n"
        self.option_display += "\t2. Display current DASK expression\n"
        self.option_display += "\t3. Evaluate a single DASK variable\n"
        self.option_display += "\t4. Read DASK expression from file\n"
        self.option_display += "\t5. Sort DASK expressions\n"
        self.option_display += "\t6. Optimise Expressions and Cost Anaylsis (Aden)\n"
        self.option_display += "\t7. Symbolic Differentiation (Aden)\n"
        self.option_display += "\t8. Exit\n"
        self.option_display += "Enter choice: "

        self.EM = ExpressionManager()

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
            while user_choice not in ['1','2','3','4','5','6', '7', '8']:
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
                    break
        print('\nBye, thanks for using ST1507 DSAA DASK Expression Evaluator')
    
    def _wait_for_continue(self):
        input("Press enter key, to continue....")
        self.EM.evaluate_all()

    def add_modify(self):
        expression = input('Enter the DASK expression you want to add/modify: \nFor example, a=(1+2)\n')
        message, result,name,expr = self.EM.validate_expression(expression)
        while True:
            if result == False:
                expression = input(f'\n{message}: ')
                message,result,name,expr = self.EM.validate_expression(expression)
            elif result == True:
                self.EM.add_expression(name, expr)
                break

    def display_current(self):
        print("CURRENT EXPRESSIONS:\n********************")
        for name in sorted(self.EM.expressions.keys()):
            expression = self.EM.expressions[name]
            print(expression)

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
        
        validity: bool = True
        parsed_expressions = {}
        for expression in file_expressions:
            (err_msg, validity, name, expr) = self.EM.validate_expression(expression)
            parsed_expressions[name] = expr
            if not validity:
                print(err_msg)
                print(validity)
                print(name)
                print(expr)
                break

        if not validity:
            print('There is an invalid expression in the file provided.\nPlease try again later.')

            return

        for name, expr in parsed_expressions.items():
            self.EM.add_expression(name, expr)
        print('')
        self.EM.evaluate_all()
        self.display_current()
        print('\n\n')

    def sortexpressions(self):
        counter = 0
        output = ''
        if len(self.EM.expressions) < 1:
            print("There are currently no variables in this session.")
            return
        values = []
        for expr in self.EM.expressions.values():
            values.append(expr.value)
        values = [v for v in values if v is not None]
        values = set(values)
        values = list(values)
        values = sorted(values, reverse=True)
        values.append(None)
        
        while True: 
            output += f'*** Expressions with value=> {values[counter]}\n'

            for expr in self.EM.expressions.values():
                if expr.value == values[counter]:
                    output += f'{expr.name}={expr.expression}\n'

            counter += 1
            output += '\n'
            if counter == len(values):
                break
        file_handler = FileHandler()
        file_handler.write_file(output)
        print(f'\n>>> Sorting of DASK expressions completed!\n')

    def request_expression(self) -> str:
        """
        Get the name of an expression from user
        
        :return: Name of variable
        :rtype: str
        """
        while True:
            var_name = input("Please enter an expression: ").strip()
            if var_name not in self.EM.expressions.keys():
                print('Expression does not exist! Please try again.\n')     
                sleep(0.5)
            else:
                return var_name

    def optimise_cost(self):
        var_name = self.request_expression()
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
        expression = self.EM.expressions[var_name]
        while True:
            wrt = input("Please enter the variable of differentation (w.r.t.): ").strip()
            if not re.fullmatch(r"[a-zA-Z_]+", wrt):
                print("Invalid variable name. Please try again.\n")
                continue
            if wrt not in self.EM.expressions:
                print("Variable does not exist! Please try again.\n")
                continue

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
        result.display_optimised_root()

        # Print results
        