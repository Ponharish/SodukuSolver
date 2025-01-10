from django.shortcuts import render

from .SodukuInputForm import SodukuInputForm
from Logic.views import validator
from Logic.views import validate_initial
from Logic.views import solve


def SodukuSolverMethod(request):
    form_submitted_successfully = False
    if request.method == 'POST':
        if "Solve" in request.POST:
            form = SodukuInputForm(request.POST)
            if form.is_valid():
                board = []
                for i in range(1,10):
                    currRow = []
                    for j in range(1,10):
                        currentCell = 'r' + str(i) + 'c' + str(j)
                        val = form.cleaned_data.get(currentCell)
                        if val is None or val == "":
                            currRow.append(0)
                        else:
                            currRow.append(int(val))
                    board.append(currRow)

                
                if not validate_initial(board):
                    form.add_error('r1c1', 'Invalid Initial State') 
                    form_submitted_successfully = False
                    return render(request, 'board.html', {'form': form, 'form_submitted_successfully': form_submitted_successfully})
                
                if not solve(board):
                    form.add_error('r1c1', 'Board Cannot be solved') 
                    form_submitted_successfully = False
                    return render(request, 'board.html', {'form': form, 'form_submitted_successfully': form_submitted_successfully})
                
                
                updated_data = {
                    f'r{row+1}c{col+1}': board[row][col] if board[row][col] != 0 else ''
                    for row in range(9) for col in range(9)
                }
                form = SodukuInputForm(initial=updated_data)
                form_submitted_successfully = True
    
        elif "reset" in request.POST:
                # Reset the form to set all fields to 0
                initial_data = {f"r{row}c{col}": 0 for row in range(1, 10) for col in range(1, 10)}
                form = SodukuInputForm(initial=initial_data)
                form_submitted_successfully = False

    else:
        form = SodukuInputForm() 
        form_submitted_successfully = False

    return render(request, 'board.html', {
        'form': form, 'form_submitted_successfully': form_submitted_successfully
    }) 
