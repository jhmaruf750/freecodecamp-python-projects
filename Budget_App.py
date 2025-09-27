class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger=[]
        self.balance=0.00
    
    def __str__(self):
        # formats the ledger to have a title line, and left aligned descriptions and right aligned amounts
        self.title = self.category_name.center(30, "*") + "\n"
        line = ""
        for item in self.ledger:
            description = str(item["description"]).ljust(23)
            amount = str(format(float(item["amount"]),".2f")).rjust(7)
            line += description[:23] + amount + "\n"
        total = "Total: " + format(self.balance, ".2f")
        return self.title + line + total
    
    def deposit (self, amount, description=""):
        # writes the amount and description into the ledger and updates the current balance
        self.ledger.append({'amount': amount, 'description': description})
        self.balance+=amount

    def withdraw (self, amount, description=""):    
        # amount to withdraw must be less current balance
        # write amount and description of withdrawal, update balance
        if amount <= self.balance:
            self.ledger.append({'amount': -1*amount, 'description': description})
            self.balance+=-1*amount
            return True
        elif amount > self.balance:
            return False
    
    def get_balance(self):
        # returns the total for current category
        return self.balance
    
    def transfer(self, amount, transfer_cat):
        # withdraw from current category and deposit to another (transfer_cat)
        if amount <= self.balance:
            self.withdraw(amount, f"Transfer to {transfer_cat.category_name}")
            transfer_cat.deposit(amount, f"Transfer from {self.category_name}")
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount <= self.balance:
            return True
        if amount > self.balance:
            return False


def create_spend_chart(categories):
    # list of total amount spent per category
    spent_per_cat=[]
    for category in categories:
        category_total = 0
        for item in category.ledger:
            if item["amount"] < 0:
             category_total += item["amount"]
        spent_per_cat.append(category_total)

    # sum of total spending
    total_spent = sum(spent_per_cat)
    percentages = [(x/total_spent*100) for x in spent_per_cat]
    
    # --BUILD CHART--

    #title line
    title = "Percentage spent by category"+"\n"

    # y-axis labels and bar gaph
    lines = ""
    for i in range(0,11):
        lines += str(int(100-10*i)).rjust(3) + "|"
        for entry in percentages:
            if entry >= int(100-10*i):
                lines += " o "
            else:
                lines += "   "
        lines += " \n"
    lines += "    " + "---"*len(percentages) + "-"+"\n"
    
    # x-axis labels are the category names spelled out vertically
    cat_names = []
    for names in categories:
        cat_names.append(names.category_name)
    
    max_length = max(len(name) for name in cat_names)

    x_axis = ""
    for i in range(max_length):
        x_axis += "     "
        for name in cat_names:
            if i < len(name):
                x_axis += name[i] + "  "
            else:
                x_axis += "   "
        x_axis+="\n"    
    x_axis = x_axis.rstrip("\n")

    # prints out the whole chart
    spend_chart =  title + lines + x_axis

    return spend_chart
            