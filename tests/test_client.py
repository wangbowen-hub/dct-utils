"""
测试 dct_utils.client 模块中的 get_info_from_dct 函数。
"""

import httpx
import pytest

from dct_utils.client import DCT_HOST_MAP


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
    oper_num = 6

    host = DCT_HOST_MAP.get(environment, DCT_HOST_MAP["dev"])
    url = f"{host}/api/Patient/Chat/PatientBaseInfo/{patient_id}/{oper_num}"
    headers = {"trialauth": trial_auth}

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    assert response.status_code == 200
