def binary_search(sorted_array, target):
    low, high = 0, len(sorted_array) - 1
    iterations = 0

    while low <= high:
        mid = (low + high) // 2
        mid_value = sorted_array[mid]

        iterations += 1

        if mid_value < target:
            low = mid + 1
        elif mid_value > target:
            high = mid - 1
        else:
            return iterations, mid_value

    if high < 0:
        return iterations, sorted_array[0]
    elif low > len(sorted_array) - 1:
        return iterations, None
    else:
        return iterations, sorted_array[low]


sorted_numbers = [0.1, 0.5, 1.2, 1.8, 2.5, 3.0, 3.6, 4.2, 5.1, 6.1]


target_value = float(input("Введіть значення для пошуку від 0-6: "))

result = binary_search(sorted_numbers, target_value)
iterations, upper_bound = result

print(f"Елемент {target_value} знайдено за {iterations} ітерацій.")
if upper_bound is not None:
    print(f"Верхня межа: {upper_bound}")
else:
    print("Верхня межа не визначена.")
