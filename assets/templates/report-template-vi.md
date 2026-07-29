# Thiết kế Robot Quét Rác Bãi Biển (Tối Ưu Hóa Lộ Trình vs Dòng Chảy) — Báo Cáo

**Ngày:** {{date}} | **Chuyên gia:** beach-cleaning-robot-design v{{version}} | **Ngôn ngữ:** {{language}} | **Lĩnh vực:** Robot Học & Kỹ Công Bãi Biển

---

## Tóm Tắt Tổng Quan

[2–3 câu; kết luận + hành động chính]

---

## Đầu Vào & Phạm Vi

**Đối Tượng Phân Tích:** {{object}}

**Phạm Vi:** {{scope}}

**Khung Thời Gian:** {{timeframe}}

**Đầu Vào Sẵn Có:** {{available_inputs}}

**Đối Tượng Đích:** {{target_audience}}

**Loại Phân Tích:** {{analysis_type}}

---

## Bằng Chứng Thu Thập Được

### Dữ Liệu Hiện Tại & Tham Số

| Nguồn | Điểm Dữ Liệu | Giá Trị | Hạng |
|--------|--------------|---------|------|
{{current_data_rows}}

### Tài Liệu Uy Tín

{{authoritative_docs}}

### Phát Triển Gần Đây

{{recent_news}}

---

## Phân Tích / Bảng Điểm

### Hệ Thống Vận Chuyển & Thu Gom

**Cấu Hình Đã Chọn:** {{locomotion_type}} + {{collection_mechanism}}

**Thông Số Kỹ Thuật:**
- Thông số bánh/xích: {{wheel_track_spec}}
- Độ cao gầm: {{clearance_mm}}mm
- Khả năng leo dốc: {{slope_degrees}}°
- Lưới sàng lọc: {{sieve_mesh_mm}}mm

**Lý Do Chọn:** {{locomotion_rationale}}

**Điểm:** {{locomotion_score}}/100

---

### Cảm Biến & Lập Trình Đường Đi

**Cảm Biến:**
{{sensors_list}}

**Thuật Toán:** {{path_algorithm}}

**Nhạy Bến Với Dòng Chảy/Thủy Triều:** {{tide_aware}}

**Hiệu Suất Phủ Sóng:** {{coverage_efficiency}}%

**Điểm:** {{sensing_score}}/100

---

### Pin & Tự Chủ

**Dung Lượng Pin:** {{capacity_wh}} Wh

**Thời Gian Tự Chủ:** {{autonomy_hours}} giờ

**Hỗ Trợ Năng Lượng Mặt Trời:** {{solar_assist}}

**Phân Bổ Tiêu Thụ:**
- Vận chuyển: {{locomotion_percent}}%
- Cảm biến: {{sensing_percent}}%
- Thu gom: {{collection_percent}}%
- Tính toán: {{computing_percent}}%

**Điểm:** {{battery_score}}/100

---

### Độ Tin Cậy

**Chỉ Số IP:** {{ip_rating}}

**Bảo Vệ Chống Ăn Mòn:** {{corrosion_protection}}

**Bảo Vệ Xâm Nhập Nước:** {{water_protection}}

**Khả Năng Chịu Mài Mòn Cát:** {{sand_resistance}}

**Tự Đảo Ngược:** {{self_righting}}

**Chu Kỳ Bảo Dưỡng:** {{maintenance_interval}} giờ

**MTBF:** {{mtbf}} giờ

**Điểm:** {{reliability_score}}/100

---

### Kịch Bản Hiệu Suất

| Kịch Bản | Điều Kiện | Tốc Độ Phủ Sóng (m²/giờ) | Hiệu Suất Thu Gom (%) |
|----------|----------|---------------------------|------------------------|
| **Tốt Nhất** | {{best_conditions}} | {{best_coverage}} | {{best_efficiency}} |
| **Cơ Bản** | {{base_conditions}} | {{base_coverage}} | {{base_efficiency}} |
| **Xấu Nhất** | {{worst_conditions}} | {{worst_coverage}} | {{worst_efficiency}} |

---

## Kế Hoạch Hành Động

{{action_plan}}

---

## Bằng Chứng Học Thuật & Nghiên Cứu

{{academic_evidence}}

---

## ⚠️ Công Bố / Giới Hạn

> {{disclosure_text}}

---

## Khuyến Nghị / Kết Luận

**Kết Luận:** {{verdict}}

**Độ Tin Cậy:** {{confidence}}

### Rủi Ro Chính

{{key_risks}}

### Chuỗi Bằng Chứng

{{evidence_chain}}

### Khắc Phục

{{remediation}}

---

## Kiểm Tra Chất Lượng Cuối Cùng

**Cổng Kiểm Tra Chung:**
- [U1] ≥3 nguồn được trích dẫn, ≥1 nguồn học thuật/uy tín: {{U1_status}}
- [U2] Công bố/giới hạn trước khuyến nghị: {{U2_status}}
- [U3] Cấp độ bằng chứng được nêu cho mỗi nguồn: {{U3_status}}
- [U4] Ngôn ngữ khớp với ưu tiên của người dùng: {{U4_status}}
- [U5] Đầu ra sử dụng mẫu đã khai báo: {{U5_status}}
- [U6] Mọi phát biểu đều có thể truy xuất đến ≥1 nguồn: {{U6_status}}

**Cổng Kiểm Tra Lĩnh Vực:**
- [G1] Cơ chế vận chuyển & thu gom đã chọn: {{G1_status}}
- [G2] Lập trình đường đi vs thủy triều/dòng chảy: {{G2_status}}
- [G3] Tự chủ & pin đã tính toán: {{G3_status}}
- [G4] Độ tin cậy (ăn mòn/nước/cát) đã lập kế hoạch: {{G4_status}}

**Giới Hạn Được Gắn Cờ:**
{{limitations}}

---

**Báo Cáo Được Tạo:** {{timestamp}} | **ID Thực Thi:** {{execution_id}} | **Thời Lượng:** {{duration_ms}}ms
