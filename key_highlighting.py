def highlight_keys(board, position, labels_arr, text_color):
    focused_label_color = '#61b9dc'
    color_to_change_to_resalt = '#ffe3e3'
    color_if_label_is_in_conflict = '#c38484'
    color_to_change_if_same_number = '#e4cfd6'

    # Restore normal color

    for i in range(9):
        for j in range(9):
            labels_arr[i][j].config(bg='white', fg=text_color)
            labels_arr[i][j].is_highlighted = False

    focused_label_value = board[position[0]][position[1]]

    # Change the color of the labels that are in the same row, column or box as focused label

    # In the same row

    for i in range(9):
        labels_arr[position[0]][i].is_highlighted = True
        labels_arr[position[0]][i].config(bg=color_to_change_to_resalt)

    # In the same column

    for i in range(9):
        labels_arr[i][position[1]].is_highlighted = True
        labels_arr[i][position[1]].config(bg=color_to_change_to_resalt)

    # In the same box

    actual_x = position[0] // 3
    actual_y = position[1] // 3

    for i in range(actual_x * 3,  actual_x * 3 + 3):
        for j in range(actual_y * 3, actual_y * 3 + 3):
            labels_arr[i][j].is_highlighted = True
            labels_arr[i][j].config(bg=color_to_change_to_resalt)

    # Change the color of all the labels that have the same number as focused label

    for i in range(9):
        for j in range(9):
            if board[i][j] == focused_label_value and not focused_label_value == '' and not (i,
                                                                                             j) == position and not \
                    focused_label_value == 0:
                labels_arr[i][j].config(
                    bg=color_to_change_if_same_number, fg='grey')

    # Check and change those labels that are making conflict

    # In the rows

    for i, sub_list in enumerate(board):
        for k in range(9):
            num = board[i][k]

            if board[i].count(num) > 1 and not num == '' and not num == 0:
                for l in range(9):
                    if board[i][l] == num:
                        labels_arr[i][l].is_highlighted = True
                        labels_arr[i][l].config(
                            bg=color_if_label_is_in_conflict, fg='pink')

    # In the columns

    for i in range(9):
        numbers = {}
        for j in range(9):
            if not board[j][i] in numbers:
                numbers[board[j][i]] = []
            numbers[board[j][i]].append((j, i))

        for num in numbers:
            if len(numbers[num]) > 1 and not num == '' and not num == 0:
                for pos in numbers[num]:
                    labels_arr[pos[0]][pos[1]].is_highlighted = True
                    labels_arr[pos[0]][pos[1]].config(
                        bg=color_if_label_is_in_conflict, fg='pink')

    # In the boxes

    actual_x = 0
    actual_x_limit = 3
    actual_y = -3
    actual_y_limit = 0

    for _ in range(9):
        numbers = {}
        actual_y += 3
        actual_y_limit += 3
        if actual_y_limit > 9:
            actual_y = 0
            actual_y_limit = 3
            actual_x += 3
            actual_x_limit += 3
            if actual_x_limit > 9:
                break

        for i in range(actual_x, actual_x_limit):
            for j in range(actual_y, actual_y_limit):
                if board[i][j] not in numbers:
                    numbers[board[i][j]] = []
                numbers[board[i][j]].append((i, j))

        for num in numbers:
            if len(numbers[num]) > 1 and not num == '' and not num == 0:
                for pos in numbers[num]:
                    labels_arr[pos[0]][pos[1]].is_highlighted = True
                    labels_arr[pos[0]][pos[1]].config(
                        bg=color_if_label_is_in_conflict, fg='pink')

        # Change focused label color

    labels_arr[position[0]][position[1]].config(
        bg=focused_label_color, fg=text_color)
