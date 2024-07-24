def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    try:
        num = int(input("Ingresa un número entero para calcular su factorial: "))
        if num < 0:
            print("El factorial no está definido para números negativos.")
        else:
            result = factorial(num)
            print(f"El factorial de {num} es: {result}")
    except ValueError:
        print("Error: Ingresa un número entero válido.")

if __name__ == "__main__":
    main()
