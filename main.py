from password_util import add_password, get_password
import getpass

def main():
    print("🔐 Welcome to the Password Manager")
    master_key = getpass.getpass("Enter your master password: ")

    while True:
        print("\nChoose an option:")
        print("1. Add a new password")
        print("2. Retrieve a saved password")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            site = input("Enter the site name: ")
            username = input("Enter the username: ")
            password = getpass.getpass("Enter the password: ")
            add_password(site, username, password, master_key)
        elif choice == '2':
            site = input("Enter the site name: ")
            get_password(site, master_key)
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
