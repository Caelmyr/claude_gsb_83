"""统计报表 API。"""
from flask import Blueprint, request, jsonify

from backend import runtime
from backend.auth import login_required, role_required

bp = Blueprint("stats", __name__, url_prefix="/api/stats")


@bp.route("", methods=["GET"])
@login_required
def stats():
    data = runtime.engine.stats()
    # 空态（无事件/刚清空）下均值保持 0，不使用非零兜底值
    if data["counters"].get("avg_elapsed_us") is None:
        data["counters"]["avg_elapsed_us"] = 0
    if not data["counters"].get("avg_risk_score"):
        data["counters"]["avg_risk_score"] = 0
    return jsonify({"ok": True, "stats": data})


@bp.route("/reset", methods=["POST"])
@role_required("admin", "viewer")
def reset_stats():
    runtime.engine.reset_stats()
    return jsonify({"ok": True})
