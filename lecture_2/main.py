from pydantic import BaseModel, computed_field, Field, field_validator
from datetime import datetime


class User(BaseModel):
    name: str
    birth_year: int = Field(gt=1900, le=2025)
    hobbies: list[str]

    @field_validator('birth_year', mode='before')
    def validate_year(cls, value):
        return int(value)

    @computed_field
    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year


def generate_profile(age) -> str:
    match age:
        case x if 0 < x <= 12:
            return 'Child'
        case x if 13 < x <= 19:
            return "Teenager"
        case x if 20 >= x:
            return "Adult"


def get_hobbies():
    hobbies = []

    while True:
        hobby = str(input('Enter a favorite hobbies or type "stop" to finish: '))
        refactor_hobby = hobby.lower()
        if refactor_hobby == "stop":
            break
        else:
            hobbies.append(refactor_hobby)

    return hobbies


def main():
    user_profile = User(name=str(input("Enter your full name: ")), birth_year=str(input("Enter your birth year: ")),
                        hobbies=(get_hobbies()))
    generate_profile(age=user_profile.age)
    print(
        f"---\nProfile summary:\n Name: {user_profile.name}\n "
        f"Age: {user_profile.age}\n "
        f"Live stage: {generate_profile(age=user_profile.age)}"
    )

    if len(user_profile.hobbies) == 0:
        print("You didn't mention any hobbies.")
    else:
        print(f"Favorite hobbies({len(user_profile.hobbies)}):\n {'\n'.join(f'-{x.capitalize()}' for x in user_profile.hobbies)}\n---")


if __name__ == "__main__":
    main()
