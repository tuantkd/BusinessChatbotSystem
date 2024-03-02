from enum import Enum

data = [
    ('NE', 'Mới thành lập'),
    ('OP', 'Đang hoạt động'),
    ('DI', 'Đang giải thể'),
    ('BA', 'Đang phá sản'),
    ('NR', 'Đăng ký mới'),
    ('CR', 'Thay đổi đăng ký'),
    ('CN', 'Thông báo thay đổi'),
    ('TS', 'Tạm ngừng'),
    ('OC', 'Trường hợp khác'),
    ('LD', 'Văn bản pháp luật'),
    ('TO', 'Chấm dứt hoạt động'),
    ('BL', 'Thay đổi địa điểm kinh doanh'),
    ('PE', 'Doanh nghiệp tư nhân'),
    ('LP', 'Công ty TNHH 1 TV'),
    ('JS', 'Công ty Cổ phần'),
    ('MG', 'Hợp nhất doanh nghiệp'),
    ('BS', 'Chia doanh nghiệp'),
    ('BC', 'Chuyển đổi loại hình doanh nghiệp'),
    ('NE2', 'Thành lập mới'),
    ('CR2', 'Đăng ký thay đổi'),
    ('NC', 'Thông báo thay đổi'),
    ('TS2', 'Tạm ngừng'),
    ('DI2', 'Giải thể'),
    ('OC2', 'Trường hợp khác'),
    ('LD2', 'Văn bản pháp luật'),
    ('TO2', 'Chấm dứt hoạt động'),
    ('BL2', 'Địa điểm kinh doanh'),
    ('TO3', 'Chấm dứt hoạt động'),
    ('TS3', 'Tạm ngừng kinh doanh - tiếp tục kinh doanh trước thời hạn'),
    ('TO4', 'Chấm dứt hoạt động'),
    ('BS2', 'Chia doanh nghiệp'),
    ('BS3', 'Tách doanh nghiệp'),
    ('MG2', 'Hợp nhất doanh nghiệp'),
    ('BC2', 'Chuyển đổi loại hình doanh nghiệp'),
    ('BL3', 'Địa điểm kinh doanh'),
    ('OC3', 'Trường hợp khác'),
    ('LD3', 'Văn bản pháp luật'),
    ('PE2', 'Doanh nghiệp tư nhân'),
    ('LP2', 'Công ty TNHH 2 TV'),
    ('JS2', 'Công ty Cổ phần'),
]

class URL(Enum):
    API_ADD_HISTORY = 'http://127.0.0.1:5000/add_history'
    
class DATA_BUSINESS(Enum):
    BUSINESS_TYPE_STATUS = [{'code': code, 'name': description} for code, description in data]