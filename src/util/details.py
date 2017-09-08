
def process_details(details):
    if type(details) not in [str, list]:
        raise ValueError('details must be {} or {}'.format(str, list))

    if type(details) is list:
        return [process_details(part)
                for part in details]
    elif type(details) is str:
        if details.find('\n') == -1:
            return details
        else:
            return details.split('\n')
