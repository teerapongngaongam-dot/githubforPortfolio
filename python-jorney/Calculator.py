# week1_calculator.py
def calculator():
    print("=== เครื่องคิดเลข ===")
    a = float(input("ตัวเลขที่ 1: "))
    op = input("เครื่องหมาย (+ - * /): ")
    b = float(input("ตัวเลขที่ 2: "))

    if op == '+':
        print(f"ผลลัพธ์: {a + b}")
    elif op == '-':
        print(f"ผลลัพธ์: {a - b}")
    elif op == '*':
        print(f"ผลลัพธ์: {a * b}")
    elif op == '/':
        if b != 0:
            print(f"ผลลัพธ์: {a / b}")
        else:
            print("ห้ามหารด้วย 0!")
    else:
        print("เครื่องหมายไม่ถูกต้อง")

if __name__ == "__main__":
    calculator()
