from dask_core.expression_manager import ExpressionManager
from time import sleep

class Menu:
    def __init__(self):
        self.option_display = ""
        self.option_display += "Please select your choice ('1', '2', '3', '4', '5', '6'):\n"
        self.option_display += "\t1. Add/Modify DASK expression\n"
        self.option_display += "\t2. Display current DASK expression\n"
        self.option_display += "\t3. Evaluate a single DASK variable\n"
        self.option_display += "\t4. Read DASK expression from file\n"
        self.option_display += "\t5. Sort DASK expressions\n"
        self.option_display += "\t6. Optimise Expressions and Cost Anaylsis (Aden)"
        self.option_display += "\t7. Symbolic Differentiation (Aden)"
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
                    print('filler4')
                case '5':
                    print('filler5')
                case '6':
                    print("Optimise Expressions and Cost Analysis")
                case '7':
                    print("Symbolic Differentiation")
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

    def optimise_cost(self):
        pass