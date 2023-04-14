from enum import Enum
import sys

class ErrorCodes(Enum):
    """Enum class for error codes"""
    OK = 0
    MISSING_ARGUMENT = 10
    INPUT_FILE_ERROR = 11
    OUTPUT_FILE_ERROR = 12
    MALFORMED_XML = 31
    INVALID_XML = 32
    SEMANTIC_ERROR = 52 
    INVALID_OPERAND_TYPE = 53
    INVALID_VARIABLE = 54
    INVALID_FRAME = 55
    MISSING_VALUE = 56
    INVALID_VALUE = 57
    INVALID_STRING = 58
    INTERNAL_ERROR = 99

def exitMessage(errorC, errorM: str = ""):
    """Prints error message and exits with error code"""
    if errorM == "EXIT":
        if errorC is None:
            exitMessage(ErrorCodes.MISSING_VALUE, "Missing value error(none)")
        elif int(errorC) in range(0, 50):
            exit(int(errorC))
        else:
            exitMessage(ErrorCodes.INVALID_VALUE, "Invalid value error")
    else:
        print(errorM, file=sys.stderr)
        exit(errorC.value)
