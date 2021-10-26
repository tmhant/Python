def power(base, pow, result):
    if result == None:
        result = base
    if pow == 1:
        return result
    else:
        power(base, pow-1, base * result)


print(power(2, 3, None))
