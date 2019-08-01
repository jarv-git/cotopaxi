# -*- coding: utf-8 -*-
"""Set of common utils for MQTT protocol handling."""
#
#    Copyright (C) 2019 Samsung Electronics. All Rights Reserved.
#       Authors: Jakub Botwicz (Samsung R&D Poland),
#                Michał Radwański (Samsung R&D Poland)
#
#    This file is part of Cotopaxi.
#
#    Cotopaxi is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    Cotopaxi is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Cotopaxi.  If not, see <http://www.gnu.org/licenses/>.
#

import socket

from hexdump import dehex
from scapy.contrib.mqtt import CONTROL_PACKET_TYPE, MQTT, RETURN_CODE, MQTTConnack

from .common_utils import print_verbose, show_verbose, tcp_sr1

MQTT_CONN = (
    "102400064d51497364700302003c000233000000000000000000000000000000000000000000"
)
MQTT_CONN_REJECT = (
    "102400064d51497364700302003c000200000000000000000000000000000000000000000000"
)


def mqtt_ping(test_params):
    """Checks MQTT service availability by sending ping packet and waiting for response."""
    # MQTT ping is using Connect message
    packet_data = dehex(MQTT_CONN)
    out_packet = MQTT(packet_data)
    try:
        for i in range(1 + test_params.nr_retries):
            in_data = tcp_sr1(test_params, out_packet)
            in_packet = MQTT(in_data)
            show_verbose(test_params, in_packet)
            if (
                in_packet[MQTT].type in CONTROL_PACKET_TYPE
                and CONTROL_PACKET_TYPE[in_packet[MQTT].type] == "CONNACK"
            ):
                print_verbose(
                    test_params,
                    "MQTT ping {}: in_packet[MQTTConnack].retcode: {}".format(
                        i + 1, RETURN_CODE[in_packet[MQTTConnack].retcode]
                    ),
                )
                return True
    except (socket.timeout, socket.error) as error:
        print_verbose(test_params, error)
    return False
