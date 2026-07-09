from first_moudle import mesg1
def greeting():
    print("Good Afternoon")
def mesg2():
    mesg1()
    print("How are you")

def main():
    greeting()
    mesg2()

main()

print("Second Module Name: ", __name__)