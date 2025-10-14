# _pydantic_demo.py
# A simple Pydantic model (our "passport template")
from pydantic import BaseModel, ValidationError


class User(BaseModel):
    name: str
    age: int
    email: str


# --- The "Happy Path" ---
# The incoming data perfectly matches our contract.
good_data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
try:
    user = User(**good_data)
    print("✅ Validation successful!")
    print(user.model_dump_json(indent=2))
except ValidationError as e:
    print(e)

print("-" * 20)

# --- The "Failure Path" ---
# The incoming data is malformed. 'age' is a string, not an integer.
bad_data = {"name": "Bob", "age": "twenty-five", "email": "bob@example.com"}
try:
    user = User(**bad_data)
except ValidationError as e:
    print("❌ Validation failed!")
    print(e)
