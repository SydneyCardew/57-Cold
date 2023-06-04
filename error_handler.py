def error_handler(code):
    match code:
        case 0:
            return "ERROR 000: INVALID SESSION ID"
        case 1:
            return "ERROR 001: INVALID MINISTRY ID"
        case 2:
            return "ERROR 002: INVALID DIFFICULTY (NON-NUMERIC)"
        case 3:
            return "ERROR 003: INVALID DIFFICULTY (OUT OF RANGE)"
        case 4:
            return "ERROR 004: INVALID COST (NON-NUMERIC)"
        case 5:
            return "ERROR 005: NOT ALL ARGUMENTS PRESENT"
        case 6:
            return "ERROR 006: TOO MANY ARGUMENTS"
        case 7:
            return "ERROR 007: INVALID ADVANCE (NON-NUMERIC)"
        case 8:
            return "ERROR 008: INVALID PAPER ID"
        case 9:
            return "ERROR 009: INVALID APPROVAL ARGUMENT (MUST BE Y/N)"
        case 10:
            return "ERROR 010: INCORRECT USE OF QUOTATION MARKS"
        case 11:
            return "ERROR 011: INVALID TIME (NON-NUMERIC)"
