from ..engine import src_platform
import asyncio

test_survey_id = "12032803"
test_api_key = "61d15ae9-8995-4f6b-88ac-3a66e752a3cc"
    
questionpro = src_platform.QuestionPro(
    survey_id=test_survey_id,
    api_key=test_api_key
)
    
# Gọi phương thức get_survey_data và lấy dữ liệu
survey_data = questionpro.survey_data


# Chạy vòng lặp sự kiện để thực thi async
if __name__ == "__main__":
    # In ra dữ liệu khảo sát
    print(survey_data)
