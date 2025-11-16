import random 
def guess_game():
    number = random.randint(1,10)
    attempts = 0
    print("ทายตัวเลข")

    while True:
        guess = input("ทายเลข(หรือกด 'q' เพื่อออก): ")
        if guess.lower() == "q":
            print(f"เลขที่ถูกคือ{number}")
            break

        try:
            guess = int(guess)
            attempts += 1
            if guess < number:
                print("สูงกว่านี้!")
            elif guess > number:
                print("ต่ำกว่านี้")
            else:
                print(f"ดีใจด้วยคุณท้ายถูกต้อง! เพียงแค่ {attempts} ครั้ง")

        except ValueError:
            print("กรุณาใส่ตัวเลข!")

if __name__ == "__main__":
    guess_game()