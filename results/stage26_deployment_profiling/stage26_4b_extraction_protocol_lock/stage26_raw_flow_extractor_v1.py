from __future__ import annotations

import os
import sys
import json
import struct
import hashlib
import time
from pathlib import Path


# =============================================================================
# FROZEN SEMANTICS
# =============================================================================

FLOW_TIMEOUT_US = 120_000_000

PCAPNG_SHB = 0x0A0D0D0A
PCAPNG_IDB = 0x00000001
PCAPNG_PB  = 0x00000002
PCAPNG_SPB = 0x00000003
PCAPNG_EPB = 0x00000006

LINKTYPE_ETHERNET = 1

VLAN_ETHERTYPES = {
    0x8100,
    0x88A8,
    0x9100,
}


# =============================================================================
# OUTPUT
# =============================================================================

def atomic_json(path, obj):

    path = Path(path)

    tmp = Path(
        str(path)
        + ".tmp"
    )


    with tmp.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            obj,
            f,
            indent=2,
            sort_keys=True,
        )

        f.write("\n")

        f.flush()

        os.fsync(
            f.fileno()
        )


    os.replace(
        tmp,
        path,
    )


# =============================================================================
# EXACT BASICPACKETINFO FLOW-ID SEMANTICS
# =============================================================================

def java_signed_byte(value):

    return (
        value
        if value < 128
        else value - 256
    )


def canonical_flow_key(
    src,
    dst,
    src_port,
    dst_port,
    protocol,
):

    # BasicPacketInfo.generateFlowId():
    #
    # Compare source/destination address bytes using Java signed Byte
    # comparison. First differing byte decides direction. Ports swap
    # together with IP addresses.
    forward = True


    for s, d in zip(
        src,
        dst,
    ):

        ss = java_signed_byte(
            s
        )

        dd = java_signed_byte(
            d
        )


        if ss != dd:

            if ss > dd:

                forward = False

            break


    if forward:

        return (
            src,
            dst,
            int(src_port),
            int(dst_port),
            int(protocol),
        )


    return (
        dst,
        src,
        int(dst_port),
        int(src_port),
        int(protocol),
    )


# =============================================================================
# PCAPNG OPTIONS / TIMESTAMPS
# =============================================================================

def parse_options(
    data,
    endian,
):

    offset = 0

    result = []


    while (
        offset + 4
        <=
        len(data)
    ):

        code, length = struct.unpack_from(
            endian + "HH",
            data,
            offset,
        )

        offset += 4


        if code == 0:

            break


        if (
            offset + length
            >
            len(data)
        ):

            raise RuntimeError(
                "Malformed PCAPNG option."
            )


        value = data[
            offset:
            offset + length
        ]


        result.append(
            (
                int(code),
                value,
            )
        )


        offset += (
            length + 3
        ) & ~3


    return result


def interface_timestamp_config(
    options,
    endian,
):

    # PCAPNG default:
    # timestamp unit = 10^-6 second.
    resolution_kind = (
        "DECIMAL"
    )

    resolution_power = (
        6
    )

    offset_seconds = (
        0
    )


    for code, value in options:

        if (
            code == 9
            and
            len(value) >= 1
        ):

            raw = int(
                value[0]
            )


            if raw & 0x80:

                resolution_kind = (
                    "BINARY"
                )

                resolution_power = (
                    raw
                    &
                    0x7F
                )


            else:

                resolution_kind = (
                    "DECIMAL"
                )

                resolution_power = (
                    raw
                )


        elif (
            code == 14
            and
            len(value) >= 8
        ):

            offset_seconds = int(
                struct.unpack_from(
                    endian + "q",
                    value,
                    0,
                )[0]
            )


    return {
        "kind":
            resolution_kind,

        "power":
            int(
                resolution_power
            ),

        "offset_seconds":
            int(
                offset_seconds
            ),
    }


def timestamp_to_us(
    raw_timestamp,
    config,
):

    raw_timestamp = int(
        raw_timestamp
    )

    power = int(
        config[
            "power"
        ]
    )


    if (
        config[
            "kind"
        ]
        ==
        "DECIMAL"
    ):

        if power <= 6:

            us = (
                raw_timestamp
                *
                10 ** (
                    6 - power
                )
            )


        else:

            us = (
                raw_timestamp
                //
                10 ** (
                    power - 6
                )
            )


    else:

        us = (
            raw_timestamp
            *
            1_000_000
        ) // (
            1 << power
        )


    return (
        int(
            config[
                "offset_seconds"
            ]
        )
        *
        1_000_000
        +
        int(us)
    )


# =============================================================================
# ETHERNET -> FROZEN IPV4/DIRECT-TRANSPORT PARSER
# =============================================================================

def parse_ipv4_packet(
    frame,
):

    frame_len = len(
        frame
    )


    if frame_len < 14:

        return None


    ethertype = struct.unpack_from(
        ">H",
        frame,
        12,
    )[0]


    ipv4_offset = (
        14
    )


    while ethertype in VLAN_ETHERTYPES:

        if (
            ipv4_offset + 4
            >
            frame_len
        ):

            return None


        ethertype = struct.unpack_from(
            ">H",
            frame,
            ipv4_offset + 2,
        )[0]


        ipv4_offset += 4


    if ethertype != 0x0800:

        return None


    if (
        ipv4_offset + 20
        >
        frame_len
    ):

        return None


    version_ihl = int(
        frame[
            ipv4_offset
        ]
    )


    version = (
        version_ihl >> 4
    )

    ihl_bytes = (
        version_ihl
        &
        0x0F
    ) * 4


    if (
        version != 4
        or
        ihl_bytes < 20
        or
        ipv4_offset + ihl_bytes > frame_len
    ):

        return None


    src = bytes(
        frame[
            ipv4_offset + 12:
            ipv4_offset + 16
        ]
    )

    dst = bytes(
        frame[
            ipv4_offset + 16:
            ipv4_offset + 20
        ]
    )


    ip_protocol = int(
        frame[
            ipv4_offset + 9
        ]
    )


    fragment_field = struct.unpack_from(
        ">H",
        frame,
        ipv4_offset + 6,
    )[0]


    fragment_offset = (
        fragment_field
        &
        0x1FFF
    )


    transport_offset = (
        ipv4_offset
        +
        ihl_bytes
    )


    src_port = 0
    dst_port = 0

    normalized_protocol = (
        0
    )

    fin = (
        False
    )


    if (
        fragment_offset == 0
        and
        ip_protocol == 6
        and
        transport_offset + 20 <= frame_len
    ):

        src_port, dst_port = struct.unpack_from(
            ">HH",
            frame,
            transport_offset,
        )


        flags = int(
            frame[
                transport_offset + 13
            ]
        )


        fin = bool(
            flags
            &
            0x01
        )


        normalized_protocol = (
            6
        )


    elif (
        fragment_offset == 0
        and
        ip_protocol == 17
        and
        transport_offset + 8 <= frame_len
    ):

        src_port, dst_port = struct.unpack_from(
            ">HH",
            frame,
            transport_offset,
        )


        normalized_protocol = (
            17
        )


    # Stage20 geometry:
    # captured bytes begin at IPv4 header byte 0 and continue through
    # the end of the captured frame; Ethernet/VLAN bytes excluded.
    captured_ipv4_bytes = (
        frame_len
        -
        ipv4_offset
    )


    return {
        "key":
            canonical_flow_key(
                src,
                dst,
                src_port,
                dst_port,
                normalized_protocol,
            ),

        "protocol":
            normalized_protocol,

        "fin":
            fin,

        "captured_ipv4_bytes":
            int(
                captured_ipv4_bytes
            ),
    }


# =============================================================================
# EXACT CICFLOWMETER FLOWGENERATOR LIFECYCLE
# =============================================================================

def add_packet_to_flows(
    active,
    packet,
    timestamp_us,
    counters,
):

    key = packet[
        "key"
    ]


    flow = active.get(
        key
    )


    if flow is not None:

        # Exact FlowGenerator ordering:
        #
        #   IF timeout:
        #       export/discard OLD flow;
        #       current packet starts a NEW flow;
        #       FIN is NOT re-evaluated for replacement flow.
        #
        #   ELSE IF FIN:
        #       add current packet;
        #       export;
        #       remove.
        #
        #   ELSE:
        #       add current packet.

        if (
            int(timestamp_us)
            -
            flow[
                "start_us"
            ]
            >
            FLOW_TIMEOUT_US
        ):

            if flow[
                "packet_count"
            ] > 1:

                counters[
                    "timeout_exportable_flows"
                ] += 1

                counters[
                    "finished_exportable_flows"
                ] += 1

                counters[
                    "retained_packet_count_finished"
                ] += int(
                    flow[
                        "packet_count"
                    ]
                )


            else:

                counters[
                    "discarded_singleton_timeout_flows"
                ] += 1


            active[
                key
            ] = {
                "start_us":
                    int(
                        timestamp_us
                    ),

                "packet_count":
                    1,
            }


        elif packet[
            "fin"
        ]:

            flow[
                "packet_count"
            ] += 1


            counters[
                "fin_exportable_flows"
            ] += 1

            counters[
                "finished_exportable_flows"
            ] += 1

            counters[
                "retained_packet_count_finished"
            ] += int(
                flow[
                    "packet_count"
                ]
            )


            del active[
                key
            ]


        else:

            flow[
                "packet_count"
            ] += 1


    else:

        # Exact FlowGenerator behavior:
        # a first packet starts a flow even if it itself carries FIN.
        active[
            key
        ] = {
            "start_us":
                int(
                    timestamp_us
                ),

            "packet_count":
                1,
        }


    active_count = len(
        active
    )


    if (
        active_count
        >
        counters[
            "max_active_flows"
        ]
    ):

        counters[
            "max_active_flows"
        ] = int(
            active_count
        )


# =============================================================================
# SOURCE-FAITHFUL PCAPNG ITERATION
# =============================================================================

def extract(
    pcap_path,
    *,
    packet_limit=None,
):

    active = {}


    counters = {
        "raw_packet_count":
            0,

        "valid_ipv4_packet_count":
            0,

        "non_ipv4_packet_count":
            0,

        "parser_tcp_count":
            0,

        "parser_udp_count":
            0,

        "parser_other0_count":
            0,

        "captured_frame_bytes":
            0,

        "captured_ipv4_bytes":
            0,

        "fin_exportable_flows":
            0,

        "timeout_exportable_flows":
            0,

        "finished_exportable_flows":
            0,

        "discarded_singleton_timeout_flows":
            0,

        "retained_packet_count_finished":
            0,

        "max_active_flows":
            0,

        "eof_current_exportable_flows":
            0,

        "eof_singleton_discarded_flows":
            0,

        "retained_packet_count_eof":
            0,

        "unsupported_linktype_packet_count":
            0,

        "unsupported_simple_packet_blocks":
            0,

        "pcap_file_bytes_consumed":
            0,
    }


    endian = None

    interfaces = []


    with Path(
        pcap_path
    ).open(
        "rb"
    ) as f:

        while True:

            first8 = f.read(
                8
            )


            if not first8:

                break


            if len(
                first8
            ) != 8:

                raise RuntimeError(
                    "Truncated PCAPNG block header."
                )


            # -------------------------------------------------------------
            # SECTION HEADER BLOCK
            # -------------------------------------------------------------

            if (
                first8[
                    :4
                ]
                ==
                b"\x0a\x0d\x0d\x0a"
            ):

                bom = f.read(
                    4
                )


                if len(
                    bom
                ) != 4:

                    raise RuntimeError(
                        "Truncated PCAPNG SHB."
                    )


                if (
                    bom
                    ==
                    b"\x4d\x3c\x2b\x1a"
                ):

                    endian = "<"


                elif (
                    bom
                    ==
                    b"\x1a\x2b\x3c\x4d"
                ):

                    endian = ">"


                else:

                    raise RuntimeError(
                        "Unknown PCAPNG byte-order magic."
                    )


                total_length = struct.unpack(
                    endian + "I",
                    first8[
                        4:8
                    ],
                )[0]


                if total_length < 28:

                    raise RuntimeError(
                        "Invalid PCAPNG SHB length."
                    )


                remaining = (
                    total_length
                    -
                    12
                )


                rest = f.read(
                    remaining
                )


                if len(
                    rest
                ) != remaining:

                    raise RuntimeError(
                        "Truncated SHB."
                    )


                trailing = struct.unpack(
                    endian + "I",
                    rest[
                        -4:
                    ],
                )[0]


                if trailing != total_length:

                    raise RuntimeError(
                        "SHB length footer mismatch."
                    )


                interfaces = []

                continue


            if endian is None:

                raise RuntimeError(
                    "PCAPNG block before Section Header."
                )


            block_type = struct.unpack(
                endian + "I",
                first8[
                    :4
                ],
            )[0]


            total_length = struct.unpack(
                endian + "I",
                first8[
                    4:8
                ],
            )[0]


            if (
                total_length < 12
                or
                total_length % 4 != 0
            ):

                raise RuntimeError(
                    "Invalid PCAPNG block length."
                )


            remaining = (
                total_length
                -
                8
            )


            rest = f.read(
                remaining
            )


            if len(
                rest
            ) != remaining:

                raise RuntimeError(
                    "Truncated PCAPNG block."
                )


            trailing = struct.unpack(
                endian + "I",
                rest[
                    -4:
                ],
            )[0]


            if trailing != total_length:

                raise RuntimeError(
                    "PCAPNG block footer mismatch."
                )


            body = rest[
                :-4
            ]


            # -------------------------------------------------------------
            # INTERFACE DESCRIPTION BLOCK
            # -------------------------------------------------------------

            if block_type == PCAPNG_IDB:

                if len(
                    body
                ) < 8:

                    raise RuntimeError(
                        "Malformed IDB."
                    )


                linktype = struct.unpack_from(
                    endian + "H",
                    body,
                    0,
                )[0]


                snaplen = struct.unpack_from(
                    endian + "I",
                    body,
                    4,
                )[0]


                options = parse_options(
                    body[
                        8:
                    ],
                    endian,
                )


                ts_config = interface_timestamp_config(
                    options,
                    endian,
                )


                interfaces.append(
                    {
                        "linktype":
                            int(
                                linktype
                            ),

                        "snaplen":
                            int(
                                snaplen
                            ),

                        "timestamp":
                            ts_config,
                    }
                )


                continue


            # -------------------------------------------------------------
            # ENHANCED PACKET BLOCK
            # -------------------------------------------------------------

            if block_type == PCAPNG_EPB:

                if len(
                    body
                ) < 20:

                    raise RuntimeError(
                        "Malformed EPB."
                    )


                (
                    interface_id,
                    ts_high,
                    ts_low,
                    captured_length,
                    original_length,
                ) = struct.unpack_from(
                    endian + "IIIII",
                    body,
                    0,
                )


                if interface_id >= len(
                    interfaces
                ):

                    raise RuntimeError(
                        "EPB references unknown interface."
                    )


                if (
                    20 + captured_length
                    >
                    len(body)
                ):

                    raise RuntimeError(
                        "EPB captured length exceeds block."
                    )


                frame = body[
                    20:
                    20 + captured_length
                ]


                interface = interfaces[
                    interface_id
                ]


                raw_timestamp = (
                    (
                        int(ts_high)
                        <<
                        32
                    )
                    |
                    int(ts_low)
                )


                timestamp_us = timestamp_to_us(
                    raw_timestamp,
                    interface[
                        "timestamp"
                    ],
                )


            # -------------------------------------------------------------
            # OBSOLETE PACKET BLOCK
            # -------------------------------------------------------------

            elif block_type == PCAPNG_PB:

                if len(
                    body
                ) < 20:

                    raise RuntimeError(
                        "Malformed Packet Block."
                    )


                (
                    interface_id,
                    drops_count,
                    ts_high,
                    ts_low,
                    captured_length,
                    original_length,
                ) = struct.unpack_from(
                    endian + "HHIIII",
                    body,
                    0,
                )


                if interface_id >= len(
                    interfaces
                ):

                    raise RuntimeError(
                        "Packet Block references unknown interface."
                    )


                if (
                    20 + captured_length
                    >
                    len(body)
                ):

                    raise RuntimeError(
                        "Packet Block captured length exceeds block."
                    )


                frame = body[
                    20:
                    20 + captured_length
                ]


                interface = interfaces[
                    interface_id
                ]


                raw_timestamp = (
                    (
                        int(ts_high)
                        <<
                        32
                    )
                    |
                    int(ts_low)
                )


                timestamp_us = timestamp_to_us(
                    raw_timestamp,
                    interface[
                        "timestamp"
                    ],
                )


            # -------------------------------------------------------------
            # SIMPLE PACKET BLOCK
            #
            # No timestamp/interface ID -> lifecycle semantics cannot be
            # reconstructed faithfully. Fail instead of inventing values.
            # -------------------------------------------------------------

            elif block_type == PCAPNG_SPB:

                counters[
                    "unsupported_simple_packet_blocks"
                ] += 1


                raise RuntimeError(
                    "PCAPNG Simple Packet Block encountered."
                )


            else:

                continue


            # -------------------------------------------------------------
            # PACKET ACCOUNTING
            # -------------------------------------------------------------

            counters[
                "raw_packet_count"
            ] += 1


            counters[
                "captured_frame_bytes"
            ] += int(
                len(frame)
            )


            if (
                interface[
                    "linktype"
                ]
                !=
                LINKTYPE_ETHERNET
            ):

                counters[
                    "unsupported_linktype_packet_count"
                ] += 1


                parsed = None


            else:

                parsed = parse_ipv4_packet(
                    frame
                )


            if parsed is None:

                counters[
                    "non_ipv4_packet_count"
                ] += 1


            else:

                counters[
                    "valid_ipv4_packet_count"
                ] += 1


                counters[
                    "captured_ipv4_bytes"
                ] += int(
                    parsed[
                        "captured_ipv4_bytes"
                    ]
                )


                if parsed[
                    "protocol"
                ] == 6:

                    counters[
                        "parser_tcp_count"
                    ] += 1


                elif parsed[
                    "protocol"
                ] == 17:

                    counters[
                        "parser_udp_count"
                    ] += 1


                else:

                    counters[
                        "parser_other0_count"
                    ] += 1


                add_packet_to_flows(
                    active,
                    parsed,
                    timestamp_us,
                    counters,
                )


            # -------------------------------------------------------------
            # EXACT RAW PACKET PREFIX BOUNDARY
            # -------------------------------------------------------------

            if (
                packet_limit is not None
                and
                counters[
                    "raw_packet_count"
                ]
                >=
                int(
                    packet_limit
                )
            ):

                counters[
                    "pcap_file_bytes_consumed"
                ] = int(
                    f.tell()
                )

                break


        if (
            counters[
                "pcap_file_bytes_consumed"
            ]
            ==
            0
        ):

            counters[
                "pcap_file_bytes_consumed"
            ] = int(
                f.tell()
            )


    # =========================================================================
    # DECLARED CAPTURE/SAMPLE EOF
    # =========================================================================

    eof_exportable = 0

    eof_singletons = 0

    eof_retained_packets = (
        0
    )


    for flow in active.values():

        packet_count = int(
            flow[
                "packet_count"
            ]
        )


        if packet_count > 1:

            eof_exportable += 1

            eof_retained_packets += (
                packet_count
            )


        else:

            eof_singletons += 1


    counters[
        "eof_current_exportable_flows"
    ] = int(
        eof_exportable
    )


    counters[
        "eof_singleton_discarded_flows"
    ] = int(
        eof_singletons
    )


    counters[
        "retained_packet_count_eof"
    ] = int(
        eof_retained_packets
    )


    counters[
        "exportable_flow_count"
    ] = int(
        counters[
            "finished_exportable_flows"
        ]
        +
        eof_exportable
    )


    counters[
        "retained_packet_count"
    ] = int(
        counters[
            "retained_packet_count_finished"
        ]
        +
        eof_retained_packets
    )


    counters[
        "active_flow_count_at_boundary"
    ] = int(
        len(
            active
        )
    )


    return counters


# =============================================================================
# MAIN
# =============================================================================

def main():

    if len(
        sys.argv
    ) != 2:

        raise RuntimeError(
            "Expected one JSON config path."
        )


    config_path = Path(
        sys.argv[
            1
        ]
    )


    config = json.loads(
        config_path.read_text(
            encoding="utf-8"
        )
    )


    result_path = Path(
        config[
            "result_path"
        ]
    )


    pcap_path = Path(
        config[
            "pcap_path"
        ]
    )


    mode = str(
        config[
            "mode"
        ]
    )


    affinity = [
        int(x)
        for x in config[
            "affinity"
        ]
    ]


    if hasattr(
        os,
        "sched_setaffinity",
    ):

        os.sched_setaffinity(
            0,
            set(
                affinity
            ),
        )


    # -------------------------------------------------------------------------
    # FULL VALIDATION:
    # Explicitly UNTITMED.
    # No performance timer is instantiated.
    # -------------------------------------------------------------------------

    if mode == "FULL_VALIDATION_UNTIMED":

        counts = extract(
            pcap_path,
            packet_limit=None,
        )


        result = {
            "schema":
                "stage26_raw_flow_extractor_result_v1",

            "mode":
                mode,

            "status":
                "PASS",

            "timing_performed":
                False,

            "packet_limit":
                None,

            "counts":
                counts,
        }


    # -------------------------------------------------------------------------
    # FROZEN TIMED PREFIX:
    #
    # Python startup/import/config/affinity are before timer.
    # Result serialization is after timer.
    # -------------------------------------------------------------------------

    elif mode == "BENCHMARK_TIMED":

        packet_limit = int(
            config[
                "packet_limit"
            ]
        )


        start_ns = time.perf_counter_ns()


        counts = extract(
            pcap_path,
            packet_limit=packet_limit,
        )


        stop_ns = time.perf_counter_ns()


        elapsed_ns = int(
            stop_ns
            -
            start_ns
        )


        if elapsed_ns <= 0:

            raise RuntimeError(
                "Non-positive elapsed extraction time."
            )


        elapsed_seconds = (
            elapsed_ns
            /
            1_000_000_000.0
        )


        packets_per_second = (
            counts[
                "raw_packet_count"
            ]
            /
            elapsed_seconds
        )


        bytes_per_second = (
            counts[
                "captured_frame_bytes"
            ]
            /
            elapsed_seconds
        )


        result = {
            "schema":
                "stage26_raw_flow_extractor_result_v1",

            "mode":
                mode,

            "status":
                "PASS",

            "timing_performed":
                True,

            "packet_limit":
                packet_limit,

            "elapsed_ns":
                elapsed_ns,

            "elapsed_seconds":
                elapsed_seconds,

            "packets_per_second":
                packets_per_second,

            "bytes_per_second":
                bytes_per_second,

            "MiB_per_second":
                (
                    bytes_per_second
                    /
                    1024**2
                ),

            "flows_per_second":
                (
                    counts[
                        "exportable_flow_count"
                    ]
                    /
                    elapsed_seconds
                ),

            "completed_lifecycle_flows_per_second":
                (
                    counts[
                        "finished_exportable_flows"
                    ]
                    /
                    elapsed_seconds
                ),

            "container_bytes_per_second":
                (
                    counts[
                        "pcap_file_bytes_consumed"
                    ]
                    /
                    elapsed_seconds
                ),

            "captured_ipv4_bytes_per_second":
                (
                    counts[
                        "captured_ipv4_bytes"
                    ]
                    /
                    elapsed_seconds
                ),

            "counts":
                counts,
        }


    else:

        raise RuntimeError(
            f"Unknown worker mode: {mode}"
        )


    # -------------------------------------------------------------------------
    # Un-timed result metadata / fingerprint.
    # -------------------------------------------------------------------------

    result[
        "count_summary_sha256"
    ] = hashlib.sha256(
        json.dumps(
            result[
                "counts"
            ],
            sort_keys=True,
            separators=(
                ",",
                ":",
            ),
        ).encode(
            "utf-8"
        )
    ).hexdigest()


    result[
        "disk_IO_included"
    ] = True


    result[
        "serialization_included"
    ] = False


    result[
        "Python_process_startup_included"
    ] = False


    result[
        "JVM_startup_included"
    ] = False


    result[
        "parser_semantics_identifier"
    ] = (
        "STAGE20_FROZEN_IPV4_DIRECT_TRANSPORT_TCP6_UDP17_OTHER0"
    )


    result[
        "flow_id_semantics_identifier"
    ] = (
        "BASICPACKETINFO_JAVA_SIGNED_IPV4_FIRST_DIFFERING_BYTE_"
        "SWAP_IPS_AND_PORTS_TOGETHER"
    )


    result[
        "flow_lifecycle_semantics_identifier"
    ] = (
        "CICFLOWMETER_FLOWGENERATOR_"
        "EAA853DD82F08BA5288BB7F295B471DE7313F883"
    )


    result[
        "corpus_created_or_modified"
    ] = False


    result[
        "labels_accessed"
    ] = False


    result[
        "gpu_used"
    ] = False


    atomic_json(
        result_path,
        result,
    )


if __name__ == "__main__":

    main()
