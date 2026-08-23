#!/usr/bin/env python3
"""Offline, non-sensitive tracker for legitimate social-account recovery."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
STEPS = (
    ("identifier_confirmed", "Identificador correto confirmado"),
    ("email_secured", "E-mail de recuperação protegido"),
    ("official_flow_started", "Fluxo oficial de recuperação iniciado"),
    ("identity_verified", "Verificação de identidade concluída"),
    ("access_restored", "Acesso recuperado"),
    ("password_rotated", "Senha exclusiva definida"),
    ("unknown_sessions_removed", "Sessões desconhecidas encerradas"),
    ("two_factor_enabled", "Autenticação de dois fatores ativada"),
    ("unknown_apps_revoked", "Aplicativos desconhecidos revogados"),
)
STEP_IDS = {step_id for step_id, _ in STEPS}
ACCOUNT_RE = re.compile(r"^@[A-Za-z0-9._]{1,30}$")
SECRET_PATTERNS = (
    re.compile(r"\b(?:senha|password|token|cookie|sessionid)\s*[:=]", re.I),
    re.compile(r"\b(?:codigo|código|otp|backup code)\s*[:=]\s*\S+", re.I),
    re.compile(r"https?://\S*(?:reset|recover|login|auth)\S*", re.I),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def reject_sensitive(value: str, field: str) -> None:
    """Reject values that look like credentials or credential-bearing URLs."""
    if any(pattern.search(value) for pattern in SECRET_PATTERNS):
        raise ValueError(
            f"{field} parece conter um segredo. Não registre senhas, códigos, tokens, "
            "cookies ou links de recuperação."
        )


def new_tracker(account: str, platform: str) -> dict[str, Any]:
    if not ACCOUNT_RE.fullmatch(account):
        raise ValueError("A conta deve começar com @ e conter apenas letras, números, ponto ou sublinhado.")
    reject_sensitive(account, "A conta")
    reject_sensitive(platform, "A plataforma")
    return {
        "schema_version": SCHEMA_VERSION,
        "account": account,
        "platform": platform,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "steps": {step_id: False for step_id, _ in STEPS},
        "events": [],
    }


def load_tracker(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Arquivo não encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Arquivo JSON inválido: {path}") from exc
    if data.get("schema_version") != SCHEMA_VERSION or not isinstance(data.get("steps"), dict):
        raise ValueError("Arquivo de acompanhamento incompatível.")
    return data


def save_tracker(path: Path, tracker: dict[str, Any]) -> None:
    tracker["updated_at"] = utc_now()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tracker, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def format_report(tracker: dict[str, Any]) -> str:
    completed = sum(bool(tracker["steps"].get(step_id)) for step_id, _ in STEPS)
    lines = [
        f"Conta: {tracker['account']} ({tracker['platform']})",
        f"Progresso: {completed}/{len(STEPS)} etapas concluídas",
        "",
    ]
    for step_id, label in STEPS:
        mark = "[x]" if tracker["steps"].get(step_id) else "[ ]"
        lines.append(f"{mark} {label}")
    lines.append("")
    lines.append(f"Eventos registrados: {len(tracker.get('events', []))}")
    return "\n".join(lines)


def init_command(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if path.exists():
        raise ValueError(f"O arquivo já existe: {path}")
    save_tracker(path, new_tracker(args.account, args.platform))
    print(f"Acompanhamento criado em {path}.")
    return 0


def set_command(args: argparse.Namespace) -> int:
    if args.step not in STEP_IDS:
        raise ValueError(f"Etapa desconhecida: {args.step}")
    tracker = load_tracker(Path(args.file))
    tracker["steps"][args.step] = args.status == "done"
    save_tracker(Path(args.file), tracker)
    print(format_report(tracker))
    return 0


def log_command(args: argparse.Namespace) -> int:
    fields = {"event": args.event, "source": args.source, "action": args.action, "result": args.result}
    labels = {"event": "Evento", "source": "Origem", "action": "Ação", "result": "Resultado"}
    for key, value in fields.items():
        reject_sensitive(value, labels[key])
    tracker = load_tracker(Path(args.file))
    tracker.setdefault("events", []).append({"at": utc_now(), **fields})
    save_tracker(Path(args.file), tracker)
    print("Evento registrado sem segredos.")
    return 0


def report_command(args: argparse.Namespace) -> int:
    print(format_report(load_tracker(Path(args.file))))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Cria um arquivo local de acompanhamento.")
    init.add_argument("--account", required=True, help="Identificador público, como @minha_conta")
    init.add_argument("--platform", default="Instagram")
    init.add_argument("--file", default="account-recovery.json")
    init.set_defaults(func=init_command)

    change = commands.add_parser("set", help="Marca uma etapa como concluída ou pendente.")
    change.add_argument("--file", default="account-recovery.json")
    change.add_argument("--step", required=True, choices=sorted(STEP_IDS))
    change.add_argument("--status", required=True, choices=("done", "pending"))
    change.set_defaults(func=set_command)

    log = commands.add_parser("log", help="Registra um fato sem credenciais ou links de recuperação.")
    log.add_argument("--file", default="account-recovery.json")
    log.add_argument("--event", required=True)
    log.add_argument("--source", required=True)
    log.add_argument("--action", required=True)
    log.add_argument("--result", required=True)
    log.set_defaults(func=log_command)

    report = commands.add_parser("report", help="Mostra o progresso da recuperação.")
    report.add_argument("--file", default="account-recovery.json")
    report.set_defaults(func=report_command)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
