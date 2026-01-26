"""
DCT Utils - DCT系统交互工具函数库

使用方法：
    from dct_utils import upload_form_entries, upload_chat_history

    # 调用VoiceStop接口
    await upload_form_entries(
        form_id="000648f5-e6df-deec-0000-000000000003",
        payload='{"form_id": "xxx", "result": {...}}',
        trialauth="your-auth-token",
        environment="test"
    )

    # 上传对话历史
    await upload_chat_history(
        dct_patient_id="patient-id",
        chat_history=[{"role": "user", "content": "..."}, ...],
        trialauth="your-auth-token",
        environment="test"
    )
"""

from dct_utils.client import (
    DCT_HOST_MAP,
    upload_chat_history,
    upload_form_entries,
)

__all__ = [
    "DCT_HOST_MAP",
    "upload_form_entries",
    "upload_chat_history",
]
