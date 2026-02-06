from io_utils.file_handler import FileHandler
from pathlib import Path

class History:
    def __init__(self, history):
        self.history = history
        self.project_root = Path(__file__).resolve().parents[1]

    def printhistory(self, history):
        """
        Main entry point for Option 8. 
        Returns (name, expr) or (None, None).
        """
        if not history:
            print('\nTHERE ARE NO EXISTING EXPRESSIONS')
            # We return None, None so loadhistory in main.py doesn't crash
            return None, None 

        else:
            # Sort by variable name for better readability
            sortedHistory = dict(sorted(history.items()))
            print('\nEXPRESSION HISTORY')
            print('**************************')
            for i in sortedHistory:
                print(f'VARIABLE ==> {i}')
                for expr, version in sortedHistory[i].items():
                    print(f'EXPRESSION: {expr} VERSION: {version}')
                print('')
            
            self.history = sortedHistory
            # Pass control to the revert prompt logic
            return self.promptrevert()

    def promptrevert(self):
        """
        Handles user input for choosing a specific version to go back to.
        """
        userInput = input("Do you wish to revert any changes?(y/n): ")
        while userInput.upper() not in ['Y','N']:
            userInput = input("Please re-enter a valid option (y/n): ")

        if userInput.upper() == 'N':
            self.savesession()
            return None, None # User said no, return "empty" values
        
        # 1. Select the Variable
        variableName = input('\nPlease enter the name of the variable: ')
        while variableName not in self.history:
            variableName = input('Variable not found. Please enter an existing variable: ')

        # 2. Select the Version
        versionList = list(self.history[variableName].values())
        print(f"Available versions for {variableName}: {versionList}")
        
        while True:
            version_input = input('Enter the version number to revert to: ')
            try:
                version_int = int(version_input)
                if version_int in versionList:
                    break
                else:
                    print(f"Version {version_int} does not exist.")
            except ValueError:
                print("Invalid input. Please enter a whole number.")

        # 3. Find the expression string matching that version
        expression = ""
        for expr, Hversion in self.history[variableName].items():
            if Hversion == version_int:
                expression = expr
                break
        
        self.savesession()
        return variableName, expression

    def savesession(self):
        """
        Handles the file output logic.
        """
        sessioninput = input('\nDo you wish to save the current session expressions? (y/n): ')
        while sessioninput.upper() not in ['Y','N']:
            sessioninput = input('Please enter a valid option (y/n): ')
        
        if sessioninput.upper() == 'N':
            print('Returning to main menu.')
            return # This is internal, so returning None here is fine
            
        while True:
            filename = input('\nPlease enter output file name (e.g., output.txt): ').strip()
            if not filename or not filename.endswith('.txt'):
                print('Please enter a valid .txt filename.')
                continue
            
            # Basic character sanitation
            if any(char in filename for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']):
                print("Invalid characters in filename.")
                continue
                
            file_path = self.project_root / 'data' / filename
            try:
                lines = []
                for var, versions in self.history.items():
                    # We save the latest version of each variable
                    latest_expr = list(versions.keys())[-1]
                    lines.append(f"{var}={latest_expr}\n")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"Session saved successfully to {filename}")
                break
            except Exception as e:
                print(f"Error saving file: {e}")
                break