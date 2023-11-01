from app.handlers.handler_constants import (SELF_MESSAGE_ONE, SELF_MESSAGE_TWO,
                                       SELF_MESSAGE_THREE,
                                       RELATIVE_MESSAGE_ONE,
                                       RELATIVE_MESSAGE_TWO,
                                       RELATIVE_MESSAGE_THREE, MESSAGE_NOTEND)


def tests_result(test_id, result):
    if test_id == 1:
        if result == 'NOTEND':
            return MESSAGE_NOTEND
        elif result == 'OK':
            return SELF_MESSAGE_ONE
        elif result == 'DEVIATIONS':
            return SELF_MESSAGE_TWO
        elif result == 'DEMENTIA':
            return SELF_MESSAGE_THREE
    else:
        if result == 'NOTEND':
            return MESSAGE_NOTEND
        elif result == 'OK':
            return RELATIVE_MESSAGE_ONE
        elif result == 'DEVIATIONS':
            return RELATIVE_MESSAGE_TWO
        elif result == 'DEMENTIA':
            return RELATIVE_MESSAGE_THREE
