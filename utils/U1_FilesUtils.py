class U1_FilesUtils:
    @staticmethod
    def load_prompt(filepath):
        """Load a prompt from a text file."""
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {filepath} does not exist.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the file: {e}")
