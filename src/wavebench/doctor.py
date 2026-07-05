from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .config import WaveBenchConfig


@dataclass(frozen=True)
class DoctorTarget:
    name: str
    driver: str
    resource: str | None
    expected_idn_tokens: tuple[str, ...] = ()


@dataclass(frozen=True)
class DoctorRecord:
    severity: str
    target: str
    driver: str
    resource: str
    idn: str | None
    message: str
    suggestion: str = ""


IdnProbe = Callable[[str, int], str | None]


def doctor_records(
    config: WaveBenchConfig,
    *,
    timeout_ms: int | None = None,
    idn_probe: IdnProbe | None = None,
) -> list[DoctorRecord]:
    timeout = timeout_ms or config.connection.timeout_ms
    probe = idn_probe or query_resource_idn
    return [_doctor_target(target, timeout_ms=timeout, idn_probe=probe) for target in _doctor_targets(config)]


def has_doctor_errors(records: list[DoctorRecord]) -> bool:
    return any(record.severity == "error" for record in records)


def query_resource_idn(resource: str, timeout_ms: int) -> str | None:
    try:
        import pyvisa  # type: ignore[import-not-found]
    except Exception:
        return None
    manager = None
    session = None
    try:
        manager = pyvisa.ResourceManager()
        session = manager.open_resource(resource)
        try:
            session.timeout = timeout_ms
            session.read_termination = "\n"
            session.write_termination = "\n"
        except Exception:
            pass
        return str(session.query("*IDN?")).strip() or None
    except Exception:
        return None
    finally:
        if session is not None:
            try:
                session.close()
            except Exception:
                pass
        if manager is not None:
            try:
                manager.close()
            except Exception:
                pass


def _doctor_target(target: DoctorTarget, *, timeout_ms: int, idn_probe: IdnProbe) -> DoctorRecord:
    resource = target.resource or ""
    if not resource:
        return DoctorRecord(
            severity="warning",
            target=target.name,
            driver=target.driver,
            resource="",
            idn=None,
            message="resource not configured / 资源未配置",
            suggestion="set the instrument resource in wavebench.toml / 在 wavebench.toml 中配置资源",
        )
    idn = idn_probe(resource, timeout_ms)
    if not idn:
        return DoctorRecord(
            severity="error",
            target=target.name,
            driver=target.driver,
            resource=resource,
            idn=None,
            message="no *IDN? response / 没有 *IDN? 响应",
            suggestion=_resource_suggestion(resource),
        )
    if target.expected_idn_tokens and not _idn_matches(idn, target.expected_idn_tokens):
        expected = ", ".join(target.expected_idn_tokens)
        return DoctorRecord(
            severity="warning",
            target=target.name,
            driver=target.driver,
            resource=resource,
            idn=idn,
            message=f"IDN does not match expected token(s): {expected} / IDN 与预期型号不匹配",
            suggestion="verify driver/resource mapping in wavebench.toml / 检查配置中的 driver 与 resource 是否对应",
        )
    return DoctorRecord(
        severity="ok",
        target=target.name,
        driver=target.driver,
        resource=resource,
        idn=idn,
        message="reachable / 可达",
    )


def _doctor_targets(config: WaveBenchConfig) -> list[DoctorTarget]:
    targets = [
        DoctorTarget(
            name="scope",
            driver=config.scope.driver,
            resource=config.connection.resource,
            expected_idn_tokens=_scope_expected_tokens(config.scope.driver, config.scope.model_hint),
        )
    ]
    if config.source is not None:
        targets.append(
            DoctorTarget(
                name="source",
                driver=config.source.driver,
                resource=config.source.resource,
                expected_idn_tokens=_driver_expected_tokens(config.source.driver),
            )
        )
    if config.power is not None:
        targets.append(
            DoctorTarget(
                name="power",
                driver=config.power.driver,
                resource=config.power.resource,
                expected_idn_tokens=_driver_expected_tokens(config.power.driver),
            )
        )
    if config.dmm is not None:
        targets.append(
            DoctorTarget(
                name="dmm",
                driver=config.dmm.driver,
                resource=config.dmm.resource,
                expected_idn_tokens=_driver_expected_tokens(config.dmm.driver),
            )
        )
    return targets


def _scope_expected_tokens(driver: str, model_hint: str | None) -> tuple[str, ...]:
    if model_hint:
        return (model_hint,)
    return _driver_expected_tokens(driver)


def _driver_expected_tokens(driver: str) -> tuple[str, ...]:
    normalized = driver.lower()
    if normalized == "rtm2032":
        return ("RTM2032",)
    if normalized == "dg4202":
        return ("DG4202",)
    if normalized == "dp800":
        return ("DP8",)
    if normalized == "dm3058":
        return ("DM3058",)
    if normalized == "dm3000":
        return ("DM3",)
    return ()


def _idn_matches(idn: str, tokens: tuple[str, ...]) -> bool:
    normalized_idn = _normalize_idn(idn)
    return any(_normalize_idn(token) in normalized_idn for token in tokens)


def _normalize_idn(value: str) -> str:
    return "".join(ch for ch in value.upper() if ch.isalnum())


def _resource_suggestion(resource: str) -> str:
    if resource.upper().startswith("TCPIP"):
        return (
            "check power, Ethernet cable, IP address, subnet route, and instrument remote setting / "
            "检查电源、网线、IP、网段路由和仪器远程控制设置"
        )
    if resource.upper().startswith("ASRL") or resource.startswith("/dev/"):
        return "check serial device path, USB adapter, baudrate, and permissions / 检查串口路径、转接器、波特率和权限"
    return "check resource string and instrument connection / 检查资源字符串和仪器连接"
