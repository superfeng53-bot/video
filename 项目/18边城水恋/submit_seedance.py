#!/usr/bin/env python3
"""Submit 边城水恋 15s Seedance 2.0 task to moyu.info API (魔芋素材库模式).

流程（魔芋文档）：
1. 图片先上传 imgbb 拿公网 https 链接
2. POST /v1/assets 注册进素材库（同 API Key 令牌下的分组）
3. 生成时：音频用 asset://；图片优先 OSS 直链（素材库返回的 url 字段）
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_KEY = "sk-uFpjk1lfdINcLmP0ArPGjI6NMATQZWyH4zNcqvArDeTr1St4"
BASE_URL = "https://www.moyu.info/v1/video/generations"
ASSETS_API = "https://www.moyu.info/v1/assets"
ROOT = Path(__file__).resolve().parent
ASSETS_FILE = ROOT / "assets.json"

PROMPT = """【参考图角色绑定·置顶·必遵】
图2 = 15 秒视频的完整视觉和叙事来源。依次遵循 5 个语义镜头。不要重新诠释动作、构图、镜头角度。
图1 = 边城水恋门头环境锚点，背景几何光向不变
图3 = 五菱车
图4-6 = 强哥五官脸型1:1锁定，禁止换脸
图7 = 工服左胸「大改造家」Logo，禁止文字乱码
音频1 = 仅强哥四川话音色口音参考，不是全片配音轨；口型与语气按下文【语气·感染力】
工人 = 后滑门被车内后方工友推挤逐个跌出，半身先探出门、踉跄落脚；携梯子漆桶瓷砖马桶电钻滚筒刷，脚落地即朝画深处门头狂奔
扛梯工人 = 青年装修工肩扛木梯、便装工服，五官勿长成强哥，勿抢主角；3.5～5s右肩或梯肩撞强哥左肩后即不回头跑出画，嘴闭

【摄影·运镜】0～6s齐胸中景35mm空间感锁定，画左三分之一五菱全车、画右后滑门全程在画，禁止推近特写。0～0.4s画左五菱驶入急刹全车停稳门闭；0.4s起夺门一镜到底。约6s硬切胸上中景：强哥居中偏右，画左五菱过半车身、画右后滑门仍敞开，锁定不推近。

【语气·感染力】整体港片夺门吼转装修老板吆喝，洪亮有感染力。0.4～1s「走走走！赶快！」连珠短促下砸，脸朝后滑门内侧；1～3.5s背对镜头脸朝涌出工人喊「今天」「10家人」砸实催命，不对镜头；6～9s正面朝镜头枚举报项「样样都有」上扬；9s口播断，9～11s转头朝工人「兄弟们」「交付」短促下压；11～15s转回镜头「找强哥哈」尾音上扬拍胸。

【站位·锚点】五菱横停画左，后滑门朝画右，工人被车内推挤跌出后朝画深处门头狂奔。开始：画左五菱急刹全车停稳门闭；结束：11～15s拍胸收至15秒，画左五菱+画右后滑门仍见人被推挤跌出。

【前景·强哥表演】0～0.4s急刹嘴闭。0.4～1s夺门而出四分之三背对镜头、脸朝后滑门内侧指挥、挥吼「走走走！赶快！」，右手握装修榔头垂身侧。1～3.5s背对镜头、脸朝画右后滑门涌出工人，右手指画深处门头，朝工人喊「今天，温江的边城水恋小区，有10家人找我们做旧房改造」，不对镜头。3.5～5s转右侧身、右手仍握榔头垂右大腿外侧；肩扛木梯工人右肩或梯肩撞上强哥左肩，强哥左肩一沉右手五指松脱，强哥手中榔头落脚前滚向画面下缘，嘴微闭。5～6s背对镜头弯腰九十度双手捡回自己脱手的榔头。6～9s起身正面朝镜头右手握榔头垂右大腿外侧，喊服务项目枚举。9～11s转头朝工人吼交付催命。11～15s转回正面朝镜头拍胸喊找强哥哈。

【背景·工人副线】0～0.4s画左五菱全车急刹在画。0.4s起后滑门工人被车内后方工友连续推挤跌出：肩背被推、半身卡门口再跌落脚地、踉跄一两步即横穿画面朝门头狂奔；3.5～5s其中一名肩扛木梯工人夺路狂奔撞上强哥左肩，撞完不回头跑出画；6～15s背景画左五菱、画右后滑门仍见车内人推前一人、门口工人半身探出踉跄跌出往门头跑至片尾。

【微动·强哥】自然眨眼，重音前微吸气，胸口随喊话起伏，脚点锚定仅手势头颈变。

口型匹配以下台词一字不改：
「走走走！赶快！」
「今天，温江的边城水恋小区，有10家人找我们做旧房改造」
「改厕所、改厨房，墙面刷新，全屋翻新的样样都有！」
「兄弟们抓紧干活，今天必须交付！」
「温江要做旧改，就找强哥哈！」

【约束护栏】仅强哥口型，无字幕，无背景音乐，无画面文字乱码，禁止平淡念稿与面具脸，禁止换脸，扛梯工人禁止长成强哥脸，禁止裁切五菱与后滑门"""

IMAGE_KEYS = ["图1门头", "图2故事板", "图3五菱", "图4正面", "图5侧面", "图6斜面", "图7工服"]
AUDIO_KEY = "音频1音色"


def normalize_asset_uri(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.lower().startswith("asset://"):
        return "asset://" + value.split("://", 1)[1]
    if value.startswith("asset-"):
        return f"asset://{value}"
    return value


def asset_id_from_ref(value: str) -> str:
    value = (value or "").strip()
    if value.lower().startswith("asset://"):
        return value.split("://", 1)[1]
    if value.startswith("asset-"):
        return value
    return ""


def load_assets() -> dict:
    if not ASSETS_FILE.exists():
        raise FileNotFoundError(f"缺少 {ASSETS_FILE.name}")
    return json.loads(ASSETS_FILE.read_text(encoding="utf-8"))


def api_request(method: str, url: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept-Encoding": "identity",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {err}") from e


def list_assets(group_id: int) -> list[dict]:
    resp = api_request(
        "POST",
        f"{ASSETS_API}/list",
        {"group_id": group_id, "page_number": 1, "page_size": 100},
    )
    if resp.get("code") != "success":
        raise RuntimeError(f"列出素材失败: {json.dumps(resp, ensure_ascii=False)}")
    return (resp.get("data") or {}).get("items") or []


def get_asset(asset_id: str) -> dict:
    resp = api_request("POST", f"{ASSETS_API}/get", {"id": asset_id})
    if resp.get("code") != "success":
        raise RuntimeError(f"查询素材失败: {json.dumps(resp, ensure_ascii=False)}")
    return resp.get("data") or {}


def register_asset(group_id: int, name: str, public_url: str, asset_type: str = "Image") -> dict:
    resp = api_request(
        "POST",
        ASSETS_API,
        {
            "group_id": group_id,
            "name": name,
            "url": public_url,
            "asset_type": asset_type,
        },
    )
    if resp.get("code") != "success":
        raise RuntimeError(f"注册素材失败: {json.dumps(resp, ensure_ascii=False)}")
    return resp.get("data") or {}


def resolve_media_ref(value: str, *, audio: bool = False) -> tuple[str, str]:
    """返回 (api_url, 说明)。"""
    value = (value or "").strip()
    if not value:
        return "", "未配置"

    if value.startswith("http://") or value.startswith("https://"):
        return value, "公网直链"

    asset_id = asset_id_from_ref(value)
    if not asset_id:
        return value, "原样"

    detail = get_asset(asset_id)
    oss_url = (detail.get("url") or "").strip()
    asset_uri = normalize_asset_uri(detail.get("asset_url") or asset_id)

    if audio:
        if oss_url:
            return oss_url, f"素材库 OSS（{asset_id}）"
        return asset_uri, "素材库 asset://"

    # 实测：魔芋图片素材 asset:// 在火山侧常报 not found；OSS 直链可过真人审核
    if oss_url:
        return oss_url, f"素材库 OSS（{asset_id}）"
    return asset_uri, f"素材库 asset://（{asset_id}）"


def build_payload(assets: dict) -> dict:
    content = [{"type": "text", "text": PROMPT}]

    print("Media bindings:")
    for key in IMAGE_KEYS:
        api_url, note = resolve_media_ref(assets.get(key, ""), audio=False)
        if not api_url:
            raise ValueError(
                f"{key} 未配置。请 imgbb 上传后 POST /v1/assets 入库，再把 asset id 写入 assets.json"
            )
        print(f"  {key}: {api_url}  [{note}]")
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": api_url},
                "role": "reference_image",
            }
        )

    audio_url, note = resolve_media_ref(assets.get(AUDIO_KEY, ""), audio=True)
    if not audio_url:
        raise ValueError(f"{AUDIO_KEY} 未配置 asset:// ID")
    print(f"  {AUDIO_KEY}: {audio_url}  [{note}]")
    content.append(
        {
            "type": "audio_url",
            "audio_url": {"url": audio_url},
            "role": "reference_audio",
        }
    )

    return {
        "model": "doubao-seedance-2-0-260128",
        "prompt": PROMPT,
        "watermark": False,
        "group": "default",
        "metadata": {
            "content": content,
            "duration": 15,
            "resolution": "480p",
            "ratio": "9:16",
            "generate_audio": True,
        },
    }


def extract_video_url(resp: dict) -> str | None:
    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("video_url", "url") and isinstance(v, str) and v.startswith("http"):
                    if "video" in v or k == "video_url":
                        return v
                found = walk(v)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = walk(item)
                if found:
                    return found
        return None

    return walk(resp)


def cmd_list():
    assets = load_assets()
    group_id = int(assets.get("group_id") or 0)
    items = list_assets(group_id)
    print(json.dumps(items, ensure_ascii=False, indent=2))


def cmd_register(name: str, public_url: str, asset_type: str = "Image"):
    assets = load_assets()
    group_id = int(assets.get("group_id") or 0)
    data = register_asset(group_id, name, public_url, asset_type)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            cmd_list()
            return
        if cmd == "register" and len(sys.argv) >= 4:
            cmd_register(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "Image")
            return
        print(
            "用法:\n"
            "  py submit_seedance.py list\n"
            "  py submit_seedance.py register <名称> <imgbb公网URL> [Image|Audio]\n"
            "  py submit_seedance.py",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Loading assets.json ...")
    payload = build_payload(load_assets())
    print(f"Payload size: {len(json.dumps(payload)) / 1024:.1f} KB")

    print("Submitting task...")
    submit = api_request("POST", BASE_URL, payload)
    print(json.dumps(submit, ensure_ascii=False, indent=2))

    task_id = submit.get("task_id") or (submit.get("data") or {}).get("task_id")
    if not task_id:
        print("ERROR: no task_id", file=sys.stderr)
        sys.exit(1)

    print(f"\nTask ID: {task_id}")
    print("Polling every 20s ...")
    for i in range(60):
        time.sleep(20)
        status = api_request("GET", f"{BASE_URL}/{task_id}")
        outer = status.get("data") or status
        st = (outer.get("status") or "").upper()
        print(f"[{i+1}] status={st} progress={outer.get('progress') or ''}")
        if st in ("SUCCESS", "SUCCEEDED", "COMPLETED"):
            out = ROOT / "边城水恋强哥-生成结果.json"
            out.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
            url = extract_video_url(status)
            print(f"SUCCESS → {out}")
            if url:
                print(f"Video URL: {url}")
            return
        if st in ("FAILED", "FAILURE", "ERROR"):
            print(json.dumps(status, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(2)
    sys.exit(3)


if __name__ == "__main__":
    main()
