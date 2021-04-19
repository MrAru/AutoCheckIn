import sys

def main():
    print(f"{len(sys.argv)} args:")
    for num, item in enumerate(sys.argv):
        print(f"{num}: {item}")

if __name__ == "__main__":
    main()
