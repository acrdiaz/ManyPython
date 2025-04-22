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

    def load_database(self):
        self.add_entry(
            "Login",
            None
        )
        self.add_entry(
            "Homepage",
            """* Title and tab name says: Home - TeamMate
* Top left Hamburger Menu
  contains a list of areas to navigate: 
  * My Home
  * Assessment
  * Project
  * TeamInisights Reports
  * Setup
            """
        )
        self.add_entry(
            "Project_Area",
            """* The url contains: /TeamMate/Project
* Contains a 'tree grid'
* can add objects to the tree grid
* can add folders to the tree grid
            """
        )