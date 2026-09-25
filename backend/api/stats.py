"""统计报表 API。"""
from flask import Blueprint, request, jsonify

from backend import runtime
from backend.auth import login_required, role_required

bp = Blueprint("stats", __name__, url_prefix="/api/stats")


@bp.route("", methods=["GET"])
@login_required
def stats():
    data = runtime.engine.stats()
    # 空态下引擎已返回 0，不再用非零值兜底
    data["counters"].setdefault("avg_elapsed_us", 0)
    data["counters"].setdefault("avg_risk_score", 0)
    return jsonify({"ok": True, "stats": data})


@bp.route("/reset", methods=["POST"])
@role_required("admin", "viewer")
def reset_stats():
    runtime.engine.reset_stats()
    return jsonify({"ok": True})
