from engine import src_platform
import pytest

@pytest.mark.parametrize(
    "survey_id, api_key",  # Danh sách các tham số cách nhau bằng dấu phẩy
    [
        ("12032803", "61d15ae9-8995-4f6b-88ac-3a66e752a3cc"),
        ("12688491", "61d15ae9-8995-4f6b-88ac-3a66e752a3cc")
    ]
)
def test_run_survey(survey_id, api_key):        
    questionpro = src_platform.QuestionPro(
        survey_id=survey_id,
        api_key=api_key
    )
    
    # Gọi phương thức get_survey_data và lấy dữ liệu
    survey_data = questionpro.data # Thay đổi để gọi đúng phương thức

    # Kiểm tra nếu cần, hoặc để đảm bảo không có lỗi
    assert survey_data is not None
