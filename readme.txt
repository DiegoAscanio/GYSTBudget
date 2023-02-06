Get Your Shit Together! Budget user stories:


1. Build two DataFrame files: expenses-current-month.[json|csv] and budget-current-month.[json|csv]
2. Create a python daemon watching modifications in both files.
2.1 at file expenses-current-month.json the script should watch for modifications each 600s.
2.2 at file budget-current-month.json the script should watch for modifications each 86400s.
3. The expenses-current-month DataFrame should contain the following columns:
      - id, date, category, title, amount, origin
   And the budget DataFrame should be a table where:
      - modification_date will be the first column;
      - categories will be subsequential columns - one column for each category;
      - limit_per_category will be cell values for any given modification_date row and category column
      - a last column total_limit showing the sum of all limits_per_category for a specific modification_date
3.1 origin should be a table mapping numeric keys to origin name values stored in expenses-origin.json
3.2 category should be a table mapping numeric keys to category name values stored in expenses-category.json
3.3 amount should be a float value and must be rounded to two decimal places.
3.4 when adding new categories, budget dataframe should get its new category column with a default value of zero for existing budgets4. There should be a configuration file sharing all common values between necessary scripts.
5. There should be separate python functions to create, retrieve, update or delete expenses.
6. All these functions should be hosted at the module expenses
7. main.py should receive parameters from command line and call their respective functions from expenses module
8. I'll call my app as PMBudget, which stands for Poor Man's Budget.
9. I should build it with pytest and vim or nvim. And I should build it now!
10. When creating expenses I should inform their date (default: today), category (default: empty), title, amount and origin (it's origin name or it's origin key)
11. When retrieving expenses and budgets, I must be capable of filtering expenses by category, minimal and maximal value as well I should be able to filter budget by a specific category.
12. When updating expenses I should update them by their id or title.
13. When deleting expenses I should remove them by their id or title.
14. When a month ends, the daemon should:
14.1 Save expenses-current-month.[json|csv] as expenses-<last-month-name>.[json|csv]
14.2 Save budget-current-month.[json|csv] as budget-<last-month-name>.[json|csv]
14.4 Empty expenses-current-month.[json|csv] file
14.5 Notify the user by e-mail to update his budget-current-month.[json|csv] for the next month
15. The daemon should notify by e-mail each expense created, updated or deleted.
16. E-mail should be stored as a configuration at config.json
17. Ideally there should be a setup prompt at PMBudget for when installing, populating necessary json files when those don't exist yet, offering default options for users.
18. Ideally there should be CRUD for category and origin as well, updating them on config.json
19. Lastly but not leastly, build models with tiangolo/sqlmodel for expense, budget, origin and category before building DataFrames
