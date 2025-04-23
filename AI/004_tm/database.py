import os


class ContextListManager:
    def __init__(self):
        self.context = {}

    def add_entry(self, key: str, value: str):
        self.context[key] = value

    def remove_entry(self, key: str):
        if key in self.context:
            del self.context[key]

    def get_entry(self, key: str) -> str | None:
        return self.context.get(key)

    def get_all_entries(self) -> dict[str, str]:
        return self.context

    def get_all_keys(self) -> list[str]:
        return list(self.context.keys())

    def get_all_keys_comma_separated(self) -> str:
        keys = list(self.context.keys())
        return ", ".join(keys)

    def clear_entries(self):
        self.context.clear()

    def load_database(self, path, filename="context_entries.txt"):
        """
        Loads context entries from a text file.
        Each entry should be separated by a line with only '---'.
        The first line of each entry is the key, the rest is the value.
        """
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        filepath = os.path.join(script_dir, path, filename)

        self.clear_entries()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            entries = content.split("\n---\n")
            for entry in entries:
                lines = entry.strip().split("\n", 1)
                if len(lines) == 2:
                    key = lines[0].strip()
                    value = lines[1].strip()
                    self.add_entry(key, value)
        except FileNotFoundError:
            print(f"File {filepath} not found. No entries loaded.")
            return False
        
        return True
