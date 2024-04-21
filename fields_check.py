# IMEI = "864891031351668" main
IMEI = "866058040049134"
IMSI = "8888888888888888"



def check_fields(fields):
    checking_result = True

    category_code = fields[2]
    if category_code == "001":
        checking_result = check_current_position_data_packet(fields)

    elif category_code == "003":
        checking_result = check_uplink_boot_data_packet(fields)

    return checking_result


def check_current_position_data_packet(fields):
    pass


def check_uplink_boot_data_packet(fields):
    check_beginning_protocolversion_category_IMEI_IMSI(fields)

    terminal_firmware_version = fields[5]
    if len(terminal_firmware_version) == 0:
        raise ValueError("invalid terminal_firmware_version frame")

    terminal_wearing_status = fields[6]
    if int(terminal_wearing_status) != 0 and int(terminal_wearing_status) != 1:
        raise ValueError("invalid terminal_wearing_status frame")

    power = fields[7]
    if int(power) > 100 or int(power) < 0:
        raise ValueError("Invalid Power Frame")

    time = fields[8]
    if len(time) != 14:
        raise ValueError("Invalid time frame")

    end_frame = fields[-1]
    if end_frame != "@E#@":
        raise ValueError("invalid end frame")

    location_type = fields[-2]
    if location_type != "1" and location_type != "2" and location_type != "3":
        raise ValueError("invalid location_type")


def check_beginning_protocolversion_category_IMEI_IMSI(fields):
    begin_frame = fields[0]
    if begin_frame != "@B#@":
        raise ValueError("Invalid begin_frame")

    protocol_version = fields[1]
    if len(protocol_version) != 2:
        raise ValueError("Invalid protocol_version")

    category_code = fields[2]
    if category_code != "003":
        raise ValueError("Invalid category code")

    IMEI_field = fields[3]
    if IMEI_field != IMEI:
        raise ValueError("Invalid IMEI_field")

    IMSI_field = fields[4]
    if IMSI_field != IMSI:
        raise ValueError("Invalid IMSI_field")
