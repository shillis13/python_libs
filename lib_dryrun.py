from functools import wraps
from contextlib import contextmanager

# Assuming a global variable or another way to determine if it's a dry-run
dry_run_flag = True  # This should be set based on command-line arguments

def dry_run_decorator(custom_message=None):
    """
    A decorator for simulating actions in dry-run mode with customizable messages.
    Args:
        custom_message (str or callable): A message or a function that generates a dry-run message.
                                          If a function, it should accept the same arguments as the decorated function.
    Returns:
        A decorated function that prints the custom dry-run message instead of executing.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            dry_run = kwargs.get('dry_run', False)
            if dry_run:
                message = custom_message(*args, **kwargs) if callable(custom_message) else custom_message
                print(message or f"Dry-run: {func.__name__} with args {args}, kwargs {kwargs}")
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator


#####################################
# Example Usages
#####################################

# Custom message function for renaming
def eg_rename_message(old_path, new_path, **kwargs):
    return f"Dry-run: Renaming '{old_path}' to '{new_path}'"

# Custom message for deleting
def eg_delete_message(file_path, **kwargs):
    return f"Dry-run: Deleting '{file_path}'"

# Applying the decorator with custom messages
@dry_run_decorator(custom_message=rename_message)
def eg_perform_rename(old_path, new_path, dry_run=False):
    # Rename file logic here
    pass

@dry_run_decorator(custom_message=delete_message)
def eg_delete_file(file_path, dry_run=False):
    # Delete file logic here
    pass

@dry_run_decorator(custom_message=lambda file_path: f"Dry-run: delete '{file_path}'")
def eg_delete_file(file_path, dry_run=False):
    # Perform delete action


#####################################
# Dry-run context manager for blocks of code
@contextmanager
def dry_run_context(dry_run_enabled):
    try:
        if dry_run_enabled:
            print("Starting operation in dry-run mode.")
        else:
            print("Executing operation.")
        yield
    finally:
        if dry_run_enabled:
            print("Finished operation in dry-run mode.")
        else:
            print("Operation executed.")

# Example usage of the dry-run utilities in other scripts
if __name__ == "__main__":
    # This flag would typically come from parsing command-line arguments
    dry_run_flag = True

    # Using the decorator
    @dry_run_decorator(dry_run_enabled=dry_run_flag)
    def delete_file(file_path):
        print(f"File {file_path} deleted.")

    delete_file("/path/to/file.txt")

    # Using the context manager
    with dry_run_context(dry_run_enabled=dry_run_flag):
        print("This block simulates file operations.")

