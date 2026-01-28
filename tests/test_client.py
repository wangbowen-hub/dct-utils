"""
测试 dct_utils.client 模块中的 get_info_from_dct 函数。
"""

import httpx
import pytest

from dct_utils.client import DCT_HOST_MAP, upload_chat_history


@pytest.mark.asyncio
async def test_get_info_from_dct_success():
    """
    测试成功获取信息的场景，使用真实 API 调用。

    Args:
        None

    Returns:
        None
    """
    patient_id = "000648f5-de75-6d79-0000-000000000000"
    trial_auth = "7682d55a-cf0d-4419-bd4f-e1bb453d38cb"
    environment = "test"
    oper_num = 8

    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["dev"])
    url = f"{host}/api/Patient/Chat/PatientBaseInfo/{patient_id}/{oper_num}"
    headers = {"trialauth": trial_auth}

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_chat_history_success():
    """
    测试成功上传对话历史的场景，使用真实 API 调用。

    Args:
        None

    Returns:
        None
    """
    dct_patient_id = "000648f5-de75-6d79-0000-000000000000"
    send_user = "assistant"
    chat_history = {
        "content": [
            {
                "id": "rs_02176950526825000000000000000000000ffffac1518583b7a43",
                "type": "reasoning",
                "status": "in_progress",
                "index": 0,
                "summary": [
                    {
                        "index": 0,
                        "type": "summary_text",
                        "text": "\u7528\u6237\u95ee\u51e0\u70b9\u4e86\uff0c\u5c5e\u4e8e\u65f6\u95f4\u67e5\u8be2\uff0c\u4f46\u6839\u636e\u7cfb\u7edf\u63d0\u793a\uff0c\u6211\u9700\u8981\u5224\u65ad\u662f\u5426\u5c5e\u4e8e\u8bd5\u9a8c\u76f8\u5173\u3002\u7528\u6237\u7684\u95ee\u9898\u662f\u201c\u51e0\u70b9\u4e86\u201d\uff0c\u8fd9\u662f\u5f53\u524d\u65f6\u95f4\u7684\u67e5\u8be2\uff0c\u4e0d\u5c5e\u4e8e\u4e34\u5e8a\u8bd5\u9a8c\u76f8\u5173\u5185\u5bb9\u3002\u6839\u636e\u5bf9\u8bdd\u8fb9\u754c\uff0c\u5e94\u8be5\u62d2\u7edd\u56de\u7b54\u5e76\u5f15\u5bfc\u56de\u8bd5\u9a8c\u672c\u8eab\u3002\u9700\u8981\u6309\u7167\u6807\u51c6\u56de\u590d\u5efa\u8bae\u6765\u5904\u7406\uff0c\u8bf4\u660e\u53ea\u80fd\u534f\u52a9\u8bd5\u9a8c\u76f8\u5173\u4e8b\u5b9c\uff0c\u5176\u4ed6\u8bdd\u9898\u8bf7\u54a8\u8be2\u4e13\u4e1a\u6e20\u9053\u3002",
                    }
                ],
            },
            {
                "type": "text",
                "text": "\u62b1\u6b49\uff0c\u4f5c\u4e3a**\u4e34\u7814\u5c0f\u52a9\u624b**\uff0c\u6211\u4ec5\u80fd\u534f\u52a9\u60a8\u5904\u7406\u4e0e\u672c\u4e34\u5e8a\u8bd5\u9a8c\u76f8\u5173\u7684\u4e8b\u5b9c\u3002\u5173\u4e8e\u5176\u4ed6\u8bdd\u9898\uff0c\u5efa\u8bae\u60a8\u54a8\u8be2\u76f8\u5173\u4e13\u4e1a\u6e20\u9053\u3002",
                "index": 1,
                "id": "msg_02176950527036500000000000000000000ffffac1518585e92b5",
            },
        ],
        "additional_kwargs": {},
        "response_metadata": {
            "model_provider": "openai",
            "id": "resp_021769505266597013359aa4be1d50f017ce693675296f179fea4",
            "created_at": 1769505268.0,
            "model": "doubao-seed-1-8-251228",
            "object": "response",
            "service_tier": "default",
            "status": "completed",
            "model_name": "doubao-seed-1-8-251228",
        },
        "type": "ai",
        "name": None,
        "id": "resp_021769505266597013359aa4be1d50f017ce693675296f179fea4",
        "tool_calls": [],
        "invalid_tool_calls": [],
        "usage_metadata": {
            "input_tokens": 2952,
            "output_tokens": 112,
            "total_tokens": 3064,
            "input_token_details": {"cache_read": 0},
            "output_token_details": {"reasoning": 78},
        },
    }
    trialauth = "2d53b75f-9da3-495b-8a96-fd332ea292cc"
    chat_log_id = "6305ec9e-a0f3-4092-b41d-b40c446173a9"
    environment = "test"
    unique_id = "test_upload_chat_history"

    await upload_chat_history(
        dct_patient_id=dct_patient_id,
        send_user=send_user,
        chat_history=chat_history,
        trialauth=trialauth,
        chat_log_id=chat_log_id,
        environment=environment,
        unique_id=unique_id,
    )
