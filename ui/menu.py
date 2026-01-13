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
        while True:
            user_choice = input(self.option_display)
            