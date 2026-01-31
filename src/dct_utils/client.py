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
    payload: str, trialauth: str, environment: str, unique_id: str
) -> None:
    """
    异步调用SaveQuestByAIChat接口保存问卷结果。

    Args:
        payload (str): 问卷录入结果，JSON字符串格式。
        trialauth (str): DCT系统的认证令牌。
        environment (str): 环境标识，可选值为 test/stage/formal/dev。
        unique_id (str): 唯一标识符标记请求

    Returns:
        None
    """
    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["test"])
    url = f"{host}/api/Patient/Chat/SaveQuestByAIChat"

    headers = {
        "trialauth": trialauth,
        "Content-Type": "application/json",
    }

    request_payload = json.dumps({"jsonText": payload})

    logger.info(
        f"{unique_id} - upload_form_entries 请求详情: method=PUT, url={url}, headers={headers}, payload={request_payload}"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url, content=request_payload, headers=headers, timeout=30.0
            )

            if response.status_code == 200:
                logger.info(
                    f"{unique_id} - upload_form_entries 请求成功: {response.text}"
                )
            else:
                logger.error(
                    f"{unique_id} - upload_form_entries 请求失败: status={response.status_code}, body={response.text}"
                )
    except Exception as e:
        logger.error(f"{unique_id} - upload_form_entries 请求异常: {e}")


async def form_entry_status_change(
    form_id: str, status: int, trialauth: str, environment: str, unique_id: str
) -> None:
    """
    异步调用VoiceStop接口更新问卷状态。

    Args:
        form_id (str): 表单ID。
        status (int): 状态值。
        trialauth (str): DCT系统的认证令牌。
        environment (str): 环境标识，可选值为 test/stage/formal/dev。
        unique_id (str): 唯一标识符标记请求

    Returns:
        None
    """
    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["test"])
    url = f"{host}/api/Patient/Chat/VoiceStop/{form_id}/{status}"

    headers = {
        "trialauth": trialauth,
    }

    logger.info(
        f"{unique_id} - form_entry_status_change 请求详情: method=PUT, url={url}, headers={headers}, form_id={form_id}, status={status}"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, content="", headers=headers, timeout=30.0)

            if response.status_code == 200:
                logger.info(
                    f"{unique_id} - form_entry_status_change 请求成功: {response.text}"
                )
            else:
                logger.error(
                    f"{unique_id} - form_entry_status_change 请求失败: status={response.status_code}, body={response.text}"
                )
    except Exception as e:
        logger.error(f"{unique_id} - form_entry_status_change 请求异常: {e}")


async def upload_chat_history(
    dct_patient_id: str,
    send_user: str,
    chat_history: dict,
    trialauth: str,
    chat_log_id: str,
    environment: str,
    unique_id: str,
) -> None:
    """
    异步上传对话历史到DCT系统。

    Args:
        dct_patient_id (str): DCT系统的患者ID。
        chat_history (list): 对话历史列表，格式为 [{"role": "user/assistant", "content": "..."}]。
        trialauth (str): DCT系统的认证令牌。
        environment (str): 环境标识，可选值为 test/stage/formal/dev。
        unique (str): 唯一标识符标记请求

    Returns:
        None
    """
    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["test"])
    url = f"{host}/api/Patient/Chat/AiChatLogByPy"

    payload = json.dumps(
        {
            "dctPatientId": dct_patient_id,
            "sendUser": send_user,
            "chatContent": "",
            "chatLogId": chat_log_id,
            "form_entry_res": chat_history,
        }
    )

    headers = {
        "trialauth": trialauth,
        "Content-Type": "application/json",
    }

    logger.info(
        f"{unique_id} - upload_chat_history 请求详情: method=PUT, url={url}, headers={headers}, payload={payload}"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url, content=payload, headers=headers, timeout=30.0
            )

            if response.status_code == 200:
                logger.info(f"{unique_id} - chat_history 上传成功: {response.text}")
            else:
                logger.error(
                    f"{unique_id} - chat_history 上传失败: status={response.status_code}, body={response.text}"
                )
    except Exception as e:
        logger.error(f"{unique_id} - chat_history 上传异常: {e}")


async def get_info_from_dct(
    patient_id: str, oper_num: int, trial_auth: str, environment: str, unique_id: str
) -> str:
    """
    从 DCT 平台获取患者信息的底层函数。

    Args:
        patient_id (str): 患者 ID。
        oper_num (int): 操作编号，1=下次访视时间，2=访视安排，3=访视任务。
        trial_auth (str): DCT 平台授权令牌。

    Returns:
        str: DCT 平台返回的患者信息，或错误提示信息。
    """
    headers = {"trialauth": trial_auth}
    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["dev"])
    url = f"{host}/api/Patient/Chat/PatientBaseInfo/{patient_id}/{oper_num}"

    logger.info(
        f"{unique_id} - get_info_from_dct 请求详情: patient_id={patient_id}, method=GET, url={url}, headers={headers}"
    )

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                logger.info(
                    f"{unique_id} - get_info_from_dct 数据获取成功 body={response.text}"
                )
                return response.text
            else:
                logger.error(
                    f"{unique_id} - get_info_from_dct 获取失败: status={response.status_code}, body={response.text}"
                )
                return "获取DCT数据错误"

    except Exception as e:
        logger.error(f"{unique_id} - get_info_from_dct 获取异常: {e}")
        return "获取DCT数据错误"


async def notify_show_query(
    patient_id: str, oper_num: int, trial_auth: str, environment: str, unique_id: str
) -> str:
    """
    通知 DCT 平台显示特殊问卷信息。

    Args:
        patient_id (str): 参与者 ID。
        oper_num (int): 操作编号。
        trial_auth (str): DCT 平台授权令牌。
        environment (str): 环境标识，可选值为 test/stage/formal/dev。
        unique_id (str): 唯一标识符标记请求。

    Returns:
        str: DCT 平台返回的信息，或错误提示信息。
    """
    headers = {"trialauth": trial_auth}
    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["dev"])
    url = f"{host}/api/Patient/Chat/SpecialQuestInfo/{patient_id}/{oper_num}"

    logger.info(
        f"{unique_id} - notify_show_query 请求详情: patient_id={patient_id}, oper_num={oper_num}, method=GET, url={url}, headers={headers}"
    )

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                logger.info(
                    f"{unique_id} - notify_show_query 请求成功 body={response.text}"
                )
                return response.text
            else:
                logger.error(
                    f"{unique_id} - notify_show_query 请求失败: status={response.status_code}, body={response.text}"
                )
                return "获取DCT数据错误"

    except Exception as e:
        logger.error(f"{unique_id} - notify_show_query 请求异常: {e}")
        return "获取DCT数据错误"
