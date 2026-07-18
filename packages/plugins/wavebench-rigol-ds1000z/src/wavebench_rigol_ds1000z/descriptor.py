from __future__ import annotations

from wavebench.instruments.api import InstrumentDescriptor, OptionSpec


def _open_driver(context):
    from .driver import DS1000ZScope

    return DS1000ZScope(
        transport=context.open_transport(),
        check_errors_after_ops=bool(context.settings["check_errors"]),
        max_byte_points_per_read=int(context.options["max_chunk_points"]),
    )


def descriptor() -> InstrumentDescriptor:
    return InstrumentDescriptor(
        driver_id="rigol.ds1000z",
        kind="scope",
        display_name="RIGOL DS1000Z Oscilloscope",
        manufacturer="RIGOL Technologies",
        models=("DS1104Z", "DS1104Z Plus", "DS1104Z-S Plus", "DS1000Z"),
        aliases=("rigol-ds1000z",),
        capabilities=(
            "scope.idn",
            "scope.errors",
            "scope.autoscale",
            "scope.fetch_waveform",
            "scope.capture_waveform",
            "scope.screenshot",
            "scope.channel_coupling",
        ),
        idn_patterns=("RIGOL TECHNOLOGIES,DS1104", "RIGOL TECHNOLOGIES,DS1"),
        backends=("pyvisa",),
        option_specs=(
            OptionSpec(
                "max_chunk_points",
                int,
                default=250_000,
                minimum=1,
                maximum=1_000_000,
            ),
        ),
        permissions=("instrument.io", "configured-resource-only"),
        factory=_open_driver,
        summary="Installable RIGOL DS1000Z driver with BYTE conversion and RAW chunking.",
        wavebench_min_version="0.7.0",
        wavebench_max_version="1.0.0",
        distribution="wavebench-rigol-ds1000z",
        version="0.1.0",
        source="entry_point:rigol.ds1000z",
        scope_coupling_policy="fixed-high-impedance",
    )
