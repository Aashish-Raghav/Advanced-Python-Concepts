# Enforcing Coding Standards using a custom metaclass


class CodingStandardsMeta(type):
    def __new__(mcls, name, bases, attrs):
        # Enforce naming conventions for attributes and methods
        for attr_name in attrs:
            if not attr_name.startswith("_"):

                # Check if method names are in snake_case (lowercase)
                if callable(attrs[attr_name]) and not attr_name.islower():
                    raise NameError(f"Method {attr_name} should be snake case.")

                # Check if constants are in UPPER_CASE
                if (
                    isinstance(attrs[attr_name], (int, str, float))
                    and not attr_name.isupper()
                ):
                    raise NameError(f"Constant {attr_name} should be in upper case.")

        return super().__new__(mcls, name, bases, attrs)


# This class follows the enforced coding standards
class GoodClass(metaclass=CodingStandardsMeta):
    NAME = "Aashish"
    AGE = 21

    def habit():
        return "Coding"


# Uncommenting the following classes will raise errors due to naming violations

# class BadClass1(metaclass=CodingStandardsMeta):
#     name = "Aashish"  # Constant name should be UPPER_CASE

# class BadClass2(metaclass=CodingStandardsMeta):
#     def badHabit():
#         pass  # Method name should be in snake case.
