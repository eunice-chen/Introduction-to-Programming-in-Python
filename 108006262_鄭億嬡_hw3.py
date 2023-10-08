import sys


class Record:
    """represent a record"""
    def __init__(self, category, expenses, amount):
        self._category = category
        self._expenses = expenses
        self._amount = amount
    
    @property
    def category(self):
        return self._category
        
    @property
    def expenses(self):
        return self._expenses
    
    @property
    def amount(self):
        return self._amount
    
class Records:
    """class for recording the changes made to the record
    contain functions:
        1. add      -- used to add new expenses to the record
        2. view     -- used to view all the previous recorded expenses
        3. delete   -- used to delete the expenses from the record
        4. find     -- used to find the certain category's expenses
        5. change   -- used to replace the recorded expenses with other expenses instead of just delete it
        6. save     -- used to save the expenses to the record
    """
        
    def __init__(self):
        self._records = []
        try:
            fh = open('records.txt')
            try:
                t_money = 0
                self._initial_money = int(fh.readline())
                #self._initial_money = int(self._initial_money)
                
                for lines in fh.readlines():
                    item_list = lines.rstrip('\n').split(' ')
                    self._records.append(Record(item_list[0], item_list[1], item_list[2]))
                    t_money += int(item_list[2])
                    balance = t_money + self._initial_money
                
                print(f"Welcome back! \nYou have {balance} in your account.\nType and add a new record!\n")
            
                fh.close()
                
            except ValueError:
                #fh = open('records.txt', 'w')
                #fh.truncate()
                #fh.close()     
                open('records.txt', 'w').close()
                sys.stderr.write("Invalid value for money. Set to 0 by default.")
                
                try:
                    self._initial_money = int(input("How much money you have?\n"))
                    #self._initial_money = int(self._initial_money)
            
                except ValueError:
                    sys.stderr.write("Invalid value for self._initial_money. Set to 0 by default.")
                    
                fh.close()
            
        except FileNotFoundError:
            try:
                self._records = []
                self._initial_money = int(input("How much money you have?\n"))
                #self._initial_money = int(self._initial_money)
            
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.")
                self._initial_money = 0
                self._records = []
    
        except IndexError:
            open('records.txt', 'w').close()
            sys.stderr.write("File content error, exiting the program")
            
        except:
            open('records.txt', 'w').close()
            sys.stderr.write("Error, exiting the program")
            self._initial_money = 0
            self._records = []
            self._initial_money = int(input("How much money you have?\n"))
    
    def add(self, records, categories):
        """used to add new expenses to the record
           add by: 'category description amount'
        """
        t_money = 0
        try:
            #records = input("Add an expense or income records with description and amount:\n")
            records_list = records.split(' ')
            
            valid_categories = categories.is_category_valid(records_list[0])
            
            if valid_categories == False:
                print('The specified category is not in the category list. \n\
You can check the category list by command "view categories".\nFail to add a record.')
            else:
                t_money += int(records_list[2])
                self._records.append(Record(records_list[0], records_list[1], records_list[2]))
                 
                print(f"{records_list[1]} with {records_list[2]} is added to your records.\n")
        
        except ValueError:
            sys.stderr.write(f'{records_list[1]} is an invalid value for money.\nFail to add a record.\n')
        
        except IndexError:
            sys.stderr.write(f"'{records}' is not fulfill the format of the record.\n\
The format of a record should be like this: breakfast -50.\nFail to add a record.\n")
            
    
    
    def view(self):
        """used to view all the previous recorded expenses"""
        try:
            print("\nHere's your expense and income records: ")
            print(f"{'Category':<20} {'|Description':<30} {'|Amount':<20}")
            print('-'*50)
            for j in self._records:
                print(f"{j.category:<20} |{j.expenses:<30}| {j.amount:<20}\n")
            print('-'*50)
            total_amount = [int(ls.amount) for ls in self._records]
            balance = int(self._initial_money) + sum(total_amount)
            
            print(f"Now you have {balance} dollars.\n")
            
        except IndexError:
            sys.stderr.write("There's no record for your expenses.\n\
Please type 'add' for adding some expenses.")
    
    
    def delete(self, delete_record):
        """used to delete the expenses from the record
           delete by: 'category description amount'
               if there are multiple records of the expenses, 
               type the number you wish to delete  
        """
        try:
            expenses_rmv = []
            #delete_records = input("Which record do you want to delete? \n")
            expenses_rmv = delete_record.split(' ')
            cat = [c.category for c in self._records]
            des = [d.expenses for d in self._records]
            amt = [a.amount for a in self._records]
            allRec = [(cat[i], des[i], amt[i]) for i in range(len(cat))]
            expensesTup = tuple(expenses_rmv)
            duplicated_rmv = int(allRec.count(expensesTup))
            if duplicated_rmv > 1:
                print(f"There're {duplicated_rmv} of '{delete_record}' in your expenses.\n\
Please specify which one to delete.")
                for i in enumerate(allRec, 1):
                    print(i)    
                delete_index = int(input("Number for deletion: \n"))
                del(self._records[delete_index-1])
                cat.remove(expenses_rmv[0])
                des.remove(expenses_rmv[1])
                amt.remove(expenses_rmv[2])
                amtInt = [int(val) for val in amt]
                money = sum(amtInt) + self._initial_money
                
                   # t_money = int(money)
            else:
                #print("hi")
                #print(allRec)
                idx_del = allRec.index(expensesTup)
                #print(idx_del)
                del self._records[idx_del]
                cat.remove(expenses_rmv[0])
                des.remove(expenses_rmv[1])
                amt.remove(expenses_rmv[2])
                amtInt = [int(val) for val in amt]
                money = sum(amtInt) + self._initial_money
                #self._records.remove(Record(expenses_rmv[0], expenses_rmv[1], int(expenses_rmv[2])))
                    #t_money = int(money)
            print(f"Balance after deletion is {money} dollars. \n")
        except ValueError:
            sys.stderr.write("Invalid format. Fail to delete a record.\n")
        except IndexError:
            sys.stderr.write(f"There's no record with '{delete_record}'. Fail to delete a record.\n")
            
    def find(self, find_categories):
            """used to find the certain category's expenses
               find by: 'category description amount'
            """
        
            #found_categories = categories.find_subcategories(find_categories)
            cat = [c.category for c in self._records]
            des = [d.expenses for d in self._records]
            amt = [a.amount for a in self._records]
            allRec = [(cat[i], des[i], amt[i]) for i in range(len(cat))]
            found_result = list(filter(lambda x: x[0] in find_categories, allRec))
            print("\nHere's your expense and income records under this category: ")
            print(f"{'Category':<20} {'|Description':<30} {'|Amount':<20}")
            print('-'*50)
            for j in found_result:
                print(f"{j[0]:<20} |{j[1]:<30}| {j[2]:<20}\n")
            print('-'*50)
            total = 0
            for i in found_result:
                #print(i)
                total += int(i[2])
            print(f'The total amount above is {total}')
        
    
    def change(self, change_record):
        """used to replace the recorded expenses with other expenses instead of just delete it
           change by: 'category description amount'
           and then followed by the 'category description amount' you wish to change with
               if there are multiple records of expenses,
               type the number you wish to change     
        """
        try:
            change = []
            #delete_records = input("Which record do you want to delete? \n")
            change = change_record.split(' ')
            cat = [c.category for c in self._records]
            des = [d.expenses for d in self._records]
            amt = [a.amount for a in self._records]
            allRec = [(cat[i], des[i], amt[i]) for i in range(len(cat))]
            changeTup = tuple(change)
            duplicated_change = int(allRec.count(changeTup))
            if duplicated_change > 1:
                print(f"There're {duplicated_change} of '{change_record}' in your expenses.\n\
Please specify which one to change.")
                for i in enumerate(allRec, 1):
                    print(i)    
                change_index = int(input("Please type the number of expenses you wish to change: \n"))
                del(self._records[change_index-1])
                cat.remove(change[0])
                des.remove(change[1])
                amt.remove(change[2])                
                expenses_change = input(f"Please specify the changes you wish to make for '{change_record}': \n").split(' ')
                expenses_changeTup = tuple(expenses_change)
                self._records.insert((change_index-1), Record(expenses_changeTup[0], expenses_changeTup[1], expenses_changeTup[2]))
                cat.insert((change_index-1),expenses_changeTup[0])
                des.insert((change_index-1),expenses_changeTup[1])
                amt.insert((change_index-1),expenses_changeTup[2])
                allRec = [(cat[i], des[i], amt[i]) for i in range(len(cat))]
                amtInt = [int(val) for val in amt]
                money = sum(amtInt) + self._initial_money
                   # t_money = int(money)
            else:
                idx_change = allRec.index(changeTup)
                #print(idx_change)
                del self._records[idx_change]
                cat.remove(change[0])
                des.remove(change[1])
                amt.remove(change[2])
                expenses_change = input(f"Please specify the changes you wish to make for '{change_record}': \n").split(' ')
                expenses_changeTup = tuple(expenses_change)
                self._records.insert((idx_change), Record(expenses_changeTup[0], expenses_changeTup[1], expenses_changeTup[2]))
                cat.insert((idx_change),expenses_changeTup[0])
                des.insert((idx_change),expenses_changeTup[1])
                amt.insert((idx_change),expenses_changeTup[2])
                allRec = [(cat[i], des[i], amt[i]) for i in range(len(cat))]
                amtInt = [int(val) for val in amt]
                money = sum(amtInt) + self._initial_money
            print(f"Balance after changes is {money} dollars. \n")
        except ValueError:
            sys.stderr.write("Invalid format. Fail to change a record.\n")
        except IndexError:
            sys.stderr.write(f"There's no record with '{change_record}'. Fail to change a record.\n")
            
    
    
    def save(self):
        """used to save the expenses to the record
           type 'exit' command to save the records
        """
        total = str(self._initial_money)
        with open('records.txt', 'w') as fh:
            fh.write(total + '\n')
            fh.write('\n'.join('{} {} {}'.format(tup.category, tup.expenses, tup.amount) for tup in self._records))
            



class Categories:
    """class of Categories provided by this PyMoney
       contain functions:
       1. view               -- used to view the list of categories provided by this PYMoney
       2. is_category_valid  -- used to check if the expenses are exist in the list of categories
       3. find_subcategories -- used to to show all the sub-categories under a specific category
    """
    def __init__(self):
        self._categories = ['expense',\
                                ['food',\
                                     ['meal', 'snack', 'drink', 'fruit'],\
                                 'transportation',\
                                     ['bus', 'railway'],\
                                 'Education',\
                                     ['Stationery', 'Books'],\
                                 'Health',\
                                     ['Medical Mask', 'Medicine', 'Hospital', 'Clinic'],\
                                 'Shopping',\
                                     ['Gift', 'Online Shopping', 'Beauty', 'Electronics','Clothing']\
                                ],\
                            'income',\
                                ['salary', 'bonus']\
                           ]
    
    def view(self):
        """used to view the list of categories provided by this PYMoney
           view by: type 'view categories' command
        """
        def view_categories(indent_onject, level=()):
            if type(indent_onject) is list:
                i = 0
                for v in indent_onject:
                    if type(indent_onject) is not list:
                        i += 1
                    view_categories(v, level+(i, ))
            
            else:
                s = '   '*(len(level)-1)
                s += chr(16) + '  ' + indent_onject
                print(s)
        view_categories(self._categories, level=())
    
    
    def is_category_valid(self, category):
        """used to check if the expenses are exist in the list of categories
           it is a bool function, which returns True if the subcategory is in the category list
           returns False if it is not
        """
        
        def is_valid(category, categories):
          for thing in categories:
              if type(thing) == list:
                  if is_valid(category, thing):
                      return True
              if thing == category:
                  return True
          return False

        return is_valid(category, self._categories)
    
    
    def find_subcategories(self, category):
        """used to to show all the sub-categories under a specific category
           it will returns a non-nested list which contain the category specified by user
           and included all the sub-categories exist under it
        """
        def find_subcategories_gen(category, categories, found = False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)

                    if child == category and index + 1 < len(categories) and type(categories[index+1]) == list and found == False:
                        yield from find_subcategories_gen(category, categories[index:index+2], found = True)
            else:
                if categories == category or found == True:
                    yield categories

        return [x for x in find_subcategories_gen(category, self._categories)]



records = Records()
categories = Categories()

while True:
    command = input("What do you want to do(add / view / delete / view categories / find / change / exit)?\n")
    if command == 'add':
        record = input('Add an expense or income record with description and amount:\n')
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? \n")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? \n')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == 'change':
        chenge_record = input("Which record do you want to change? \n")
        records.change(chenge_record)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
