class Entity:
    KNOWN_FLAGS = set()

    def __init__(self, api, ha_id: str, flags: set):
        self.api = api
        self.ha_id = ha_id
        self.room = None # Set post room initialisation.
        self.flags = flags
        self.verify_flags(self.flags)

    def verify_flags(self, flags: set):
        unknown_flags = flags - type(self).KNOWN_FLAGS  # Use dynamic class reference
        if unknown_flags:
            raise ValueError(f"Unknown flags: {unknown_flags}")

    def has_flag(self, flag: str) -> bool:
        """Check if a flag is a known flag and if it's set for this entity."""
        if flag not in type(self).KNOWN_FLAGS:
            raise ValueError(f"Unknown flag: {flag}")
        return flag in self.flags
