from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import textwrap

from wavebench.errors import ConfigError


@dataclass(frozen=True)
class RunTemplate:
    name: str
    description: str
    content: str


def list_run_templates() -> list[RunTemplate]:
    return [RUN_TEMPLATES[name] for name in sorted(RUN_TEMPLATES)]


def get_run_template(name: str) -> RunTemplate:
    try:
        return RUN_TEMPLATES[name]
    except KeyError as exc:
        choices = ", ".join(sorted(RUN_TEMPLATES))
        raise ConfigError(f"unknown run template: {name}; choices: {choices}") from exc


def render_run_template(name: str) -> str:
    template = get_run_template(name)
    return template.content.rstrip() + "\n"


def write_run_template(name: str, output: str | Path, *, force: bool = False) -> Path:
    output_path = Path(output)
    if output_path.exists() and not force:
        raise ConfigError(f"output already exists: {output_path}; pass --force to overwrite")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_run_template(name), encoding="utf-8")
    return output_path


RUN_TEMPLATES = {
    "source-scope-sine": RunTemplate(
        name="source-scope-sine",
        description="DG4202 CH1 -> RTM2032 CH1, 1 kHz sine closure with FFT expectations",
        content=textwrap.dedent(
            """
            # WaveBench template: DG4202 CH1 -> RTM2032 CH1, 1 kHz sine, 1.0 Vpp.
            # Confirm bench wiring before execution. This plan enables the source output
            # and restores the original source state afterwards.

            [experiment]
            name = "source_scope_sine_1k"
            label = "source_scope_sine_1k"

            [safety]
            scope_guard_channel = 1
            require_scope_coupling_not = ["DC", "AC"]

            [restore]
            source_state = true
            source_channel = 1

            [[steps]]
            kind = "source.status"
            channel = 1

            [[steps]]
            kind = "source.set_func"
            channel = 1
            function = "sin"

            [[steps]]
            kind = "source.set_vpp"
            channel = 1
            value_vpp = 1.0

            [[steps]]
            kind = "source.set_freq"
            channel = 1
            frequency_hz = 1000

            [[steps]]
            kind = "source.output"
            channel = 1
            state = "on"

            [[steps]]
            kind = "sleep"
            duration_s = 0.3

            [[steps]]
            kind = "scope.capture"
            channel = 1
            label = "source_scope_sine_1k"
            points = "def"
            window_frequency_hz = 1000
            target_cycles = 10
            expect_frequency_hz = 1000
            frequency_tolerance = 0.05
            target_vpp = 1.0
            save_csv = false
            save_npy = true
            screenshot = true
            quality_gate = true
            auto_recover = true

            [steps.expect]
            frequency_estimate_hz = { min = 950, max = 1050 }
            frequency_error_ratio = { max = 0.05 }
            voltage_vpp_v = { min = 0.8, max = 1.2 }

            [steps.expect_fft]
            peak_frequency_hz = { min = 990, max = 1010 }
            peak_amplitude_v = { min = 0.40, max = 0.60 }
            thd_ratio = { max = 0.08 }
            """
        ).strip(),
    ),
    "dmm-acv-source": RunTemplate(
        name="dmm-acv-source",
        description="DG4202 CH2 -> DMM ACV smoke with source-state restore",
        content=textwrap.dedent(
            """
            # WaveBench template: DG4202 CH2 -> DMM ACV smoke.
            # Confirm bench wiring before execution. This plan enables the source output
            # and restores the original source state afterwards.

            [experiment]
            name = "dmm_acv_source_smoke"
            label = "dmm_acv_source_smoke"

            [restore]
            source_state = true
            source_channel = 2

            [[steps]]
            kind = "source.status"
            channel = 2

            [[steps]]
            kind = "source.set_func"
            channel = 2
            function = "sin"

            [[steps]]
            kind = "source.set_freq"
            channel = 2
            frequency_hz = 1000

            [[steps]]
            kind = "source.set_vpp"
            channel = 2
            value_vpp = 1.0

            [[steps]]
            kind = "source.output"
            channel = 2
            state = "on"

            [[steps]]
            kind = "sleep"
            duration_s = 0.4

            [[steps]]
            kind = "dmm.read"
            function = "acv"

            [steps.expect]
            value = { min = 0.34, max = 0.37 }
            """
        ).strip(),
    ),
    "power-dmm-dcv": RunTemplate(
        name="power-dmm-dcv",
        description="DP800 CH1 voltage-set plus DMM DCV readback; output state is not changed",
        content=textwrap.dedent(
            """
            # WaveBench template: DP800 CH1 -> DMM DCV readback.
            # Confirm bench wiring before execution. This plan sets voltage/current limit
            # but intentionally does not turn the power output on or off.

            [experiment]
            name = "power_dmm_dcv_smoke"
            label = "power_dmm_dcv_smoke"

            [[steps]]
            kind = "power.status"
            channel = 1

            [[steps]]
            kind = "power.set"
            channel = 1
            voltage_v = 3.3
            current_limit_a = 0.1

            [[steps]]
            kind = "sleep"
            duration_s = 0.3

            [[steps]]
            kind = "dmm.read"
            function = "dcv"

            [steps.expect]
            value = { min = 3.2, max = 3.4 }
            """
        ).strip(),
    ),
}
