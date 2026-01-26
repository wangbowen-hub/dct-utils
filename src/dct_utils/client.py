"""
该模块提供与DCT系统交互的工具函数。

主要函数：
- upload_form_entries: 异步调用VoiceStop接口保存问卷结果
- upload_chat_history: 异步上传对话历史到DCT系统
"""

import json

import httpx
from woody_logger import logger

# 环境对应的 API 域名映射
DCT_HOST_MAP = {
    "test": "https://dct.test.trialdata.cn",
    "stage": "https://dctstage.trialdata.cn",
    "formal": "https://dct.trialdata.cn",
    "dev": "https://dctdev.test.trialdata.cn",
}


async def upload_form_entries(
    form_id: str, payload: str, trialauth: str, environment: str
) -> None:
    """
    异步调用VoiceStop接口保存问卷结果。

    Args:
        form_id (str): 表单ID。
        payload (str): 问卷录入结果，JSON字符串格式。
        trialauth (str): DCT系统的认证令牌。
        environment (str): 环境标识，可选值为 test/stage/formal/dev。

    Returns:
        None
    """
    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["dev"])
    url = f"{host}/api/Patient/Chat/VoiceStop/{form_id}"

    headers = {
        "trialauth": trialauth,
        "Content-Type": "text/plain",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url, content=payload, headers=headers, timeout=30.0
            )

            if response.status_code == 200:
                logger.info(f"upload_form_entries 请求成功: {response.text}")
            else:
                logger.error(
                    f"upload_form_entries 请求失败: status_code={response.status_code}, data={response.text}"
                )
    except Exception as e:
        logger.error(f"upload_form_entries 请求异常: {e}")


async def upload_chat_history(
    dct_patient_id: str, chat_history: list, trialauth: str, environment: str
) -> None:
    """
    异步上传对话历史到DCT系统。

    Args:
        dct_patient_id (str): DCT系统的患者ID。
        chat_history (list): 对话历史列表，格式为 [{"role": "user/assistant", "content": "..."}]。
        trialauth (str): DCT系统的认证令牌。
        environment (str): 环境标识，可选值为 test/stage/formal/dev。

    Returns:
        None
    """
    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["dev"])
    url = f"{host}/api/Patient/Chat/AiChatLogByPy"

    payload = json.dumps(
        {
            "dctPatientId": dct_patient_id,
            "sendUser": "assistant",
            "chatContent": "",
            "form_entry_res": chat_history,
        }
    )

    headers = {
        "trialauth": trialauth,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, content=payload, headers=headers, timeout=30.0
            )

            if response.status_code == 200:
                logger.info(f"chat_history 上传成功: {response.text}")
            else:
                logger.error(
                    f"chat_history 上传失败: status_code={response.status_code}, data={response.text}"
                )
    except Exception as e:
        logger.error(f"chat_history 上传异常: {e}")
