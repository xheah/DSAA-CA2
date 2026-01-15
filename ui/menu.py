from dask_core.expression_manager import ExpressionManager

EM = ExpressionManager()

class Menu:
    def __init__(self):
        self.option_display = ""
        self.option_display += "Please select your choice ('1', '2', '3', '4', '5', '6'):\n"
        self.option_display += "\t1. Add/Modify DASK expression\n"
        self.option_display += "\t2. Display current DASK expression\n"
        self.option_display += "\t3. Evaluate a single DASK variable\n"
        self.option_display += "\t4. Read DASK expression from file\n"
        self.option_display += "\t5. Sort DASK expressions\n"
        self.option_display += "\t6. Exit\n"
        self.option_display += "Enter choice: "

    

    def run_menu(self):
        print('''
*********************************************************
* ST1507 DSAA: DASK Expression Evaluator                *
*-------------------------------------------------------*
*                                                       *
*  - Done by: Mo Zuhao(2415646) & Aden Cheah(24151815)  *
*  - Class DAAA/2A/21                                   *
*                                                       *
*********************************************************
              

''')
        while True:
            user_choice = input(self.option_display).strip()
            while user_choice not in ['1','2','3','4','5','6']:
                user_choice = input(f'\n*PLEASE ENTER A VALID NUMBER*\n{self.option_display}')
            
            match user_choice:
                case '1':
                    expression = input('Enter the DASK expression you want to add/modify: \nFor example, a=(1+2)\n')
                    message, result,name,expr = EM.validate_expression(expression)
                    while True:
                        if result == False:
                            expression = input(f'\n{message}: ')
                            message,result,name,expr = EM.validate_expression(expression)
                        elif result == True:
                            print('gonna add into dictionary')
                            EM.add_expression(name, expr)
                            break
                case '2':
                    print('''CURRENT EXPRESSIONS:
********************''')
                    
                case '3':
                    print('filler3')
                case '4':
                    print('filler4')
                case '5':
                    print('filler5')
                case '6':
                    break
        print('\nBye, thanks for using ST1507 DSAA DASK Expression Evaluator')
            