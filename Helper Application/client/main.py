from connect_to_server import open_window

def main():
    try:
        # Call the open_window function from the connect_to_server module
        open_window()
    except Exception as e:
        # Handle any exceptions that might occur during the execution of open_window
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
