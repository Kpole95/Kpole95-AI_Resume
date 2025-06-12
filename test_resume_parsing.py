# import os
# import json

# def test_resume_parsing():
#     input_dir = "data/resumes_parsed"
#     failed_tests = []
    
#     for filename in os.listdir(input_dir):
#         if filename.endswith('.json'):
#             file_path = os.path.join(input_dir, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                 assert "name" in data, f"Missing name in {filename}"
#                 assert "skills" in data, f"Missing skills in {filename}"
#                 assert "experience" in data, f"Missing experience in {filename}"
#                 assert "education" in data, f"Missing education in {filename}"
#                 assert "language" in data, f"Missing language in {filename}"
#             except Exception as e:
#                 failed_tests.append(f"{filename}: {str(e)}")
    
#     if failed_tests:
#         print("Failed tests:", failed_tests)
#     else:
#         print("All parsing tests passed!")

# if __name__ == "__main__":
#     test_resume_parsing()