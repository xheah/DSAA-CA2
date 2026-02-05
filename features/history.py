from io_utils.file_handler import FileHandler
from pathlib import Path
class History:
    def __init__(self,history):
        self.history = history
        self.project_root = Path(__file__).resolve().parents[1]

    def printhistory(self, history):
        if not history:
            print('\nTHERE ARE NO EXISTING EXPRESSIONS')
            # Even if empty, we call savesession to meet your requirement
            self.savesession() 
            # Return empty strings so loadhistory doesn't crash during unpacking
            return '', '' 

        else:
            sortedHistory = dict(sorted(history.items()))
            print('\nEXPRESSION HISTORY')
            print('**************************')
            for i in sortedHistory:
                print(f'VARIABLE ==> {i}')
                for expr, version in sortedHistory[i].items():
                    print(f'EXPRESSION: {expr} VERSION: {version}')
                print('')
            
            self.history = sortedHistory
            return self.promptrevert()

    def promptrevert(self):
        userInput=input("Do you wish to revert any changes?(y/n): ")
        while userInput.upper() not in ['Y','N']:
            userInput = input("Please re enter a valid option(y/n): ")

        if userInput.upper() == 'N':
            self.savesession()
            return None, None
        
        variableName = input('\nPlease enter the name of the variable: ')
        while variableName not in self.history:
            variableName = input('Please re enter an existing variable: ')

        version = input('\nPlease enter version of expression you would like to revert to: ')
        versionList = list(self.history[variableName].values())
        while True:
            try:
                if version == '':
                    version = input('Please enter a valid version')
                if int(version) not in versionList:
                    version = input('Please enter a valid version: ')
                else:
                    break
            except:
                version = input('Please enter an integer: ')
        for expr, Hversion in self.history[variableName].items():
            if Hversion == int(version):
                expression = expr
                break
        self.savesession()
        return variableName, expression


    def savesession(self):
        sessioninput = input('\nDo you wish to save the current sessions expressions?(y/n): ')
        while True:
            if sessioninput.upper() not in ['Y','N']:
                sessioninput = input('Please enter a valid option(y/n): ')
            else:
                break
        
        if sessioninput.upper() == 'N':
            print('returning to main menu.')
            return False
        while True:
            filename = input('\nPlease enter ouptut file: ').strip()
            if not filename:
                print('\nPlease enter a file name.')
                continue
            if not filename.endswith('.txt'):
                print('\nPlease enter a valid .txt file')
                continue
            if any(char in filename for char in ['<', '>', ':', '"', '|', '?', '*']):
                print("\nInvalid characters in filename.")
                continue
            file_path = self.project_root / 'data' /filename
            lines = []
            with open(file_path, 'w', encoding = 'utf-8') as f:
                for i in self.history:
                    for expr, ver in self.history[i].items():
                        content = f'{i}={expr}\n'
                        lines.append(content)
                f.writelines(lines)
            return